import base64
import os
import re
from collections import namedtuple
from itertools import product
from typing import Any, Callable, Optional, TypeVar, cast
from uuid import uuid4

from dotenv import dotenv_values

from bluish import action, process
from bluish.core import ExecutionStatus
from bluish.logging import debug, error, info, warning
from bluish.redacted_string import RedactedString
from bluish.utils import decorate_for_log, safe_string


class CircularDependencyError(Exception):
    pass


TResult = TypeVar("TResult")


class DictAttrs:
    def __init__(self, definition: dict[str, Any]):
        self.__dict__.update(definition)

    def __getattr__(self, name: str) -> Any:
        if name == "_with":
            return getattr(self, "with")
        elif name == "_if":
            return getattr(self, "if")
        else:
            return None

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_with":
            setattr(self, "with", value)
        elif name == "_if":
            setattr(self, "if", value)
        else:
            self.__dict__[name] = value

    def __contains__(self, name: str) -> bool:
        return name in self.__dict__

    def ensure_property(self, name: str, default_value: Any) -> None:
        value = getattr(self, name, None)
        if value is None:
            setattr(self, name, default_value)


class ContextNode:
    def __init__(self, parent: Optional["ContextNode"], definition: dict[str, Any]):
        self.parent = parent
        self.attrs = DictAttrs(definition)

        self.attrs.ensure_property("env", {})
        self.attrs.ensure_property("var", {})

        self.id: str = self.attrs.id
        self.env = dict(self.attrs.env)
        self.var = dict(self.attrs.var)
        self.outputs: dict[str, Any] = {}
        self.result = process.ProcessResult()
        self.failed = False
        self.status: ExecutionStatus = ExecutionStatus.PENDING

        self._expression_parser: Callable[[str], Any] | None = None

    @property
    def step(self) -> Optional["StepContext"]:
        if isinstance(self, StepContext):
            return cast("StepContext", self)
        return None

    @property
    def job(self) -> Optional["JobContext"]:
        if isinstance(self, JobContext):
            return self
        elif isinstance(self, StepContext):
            return cast("JobContext", self.parent)
        return None

    @property
    def workflow(self) -> Optional["WorkflowContext"]:
        if isinstance(self, WorkflowContext):
            return self
        elif isinstance(self, JobContext):
            return cast("WorkflowContext", self.parent)
        elif isinstance(self, StepContext):
            return cast("WorkflowContext", self.parent.parent)  # type: ignore
        return None

    @property
    def display_name(self) -> str:
        return self.attrs.name if self.attrs.name else self.id

    @property
    def expression_parser(self) -> Callable[[str], Any]:
        # HACK This doesn't make me happy
        from bluish.expressions import create_parser

        if not self._expression_parser:
            self._expression_parser = create_parser(self)
        return self._expression_parser

    def dispatch(self) -> process.ProcessResult | None:
        raise NotImplementedError()

    def expand_expr(self, value: Any) -> Any:
        if isinstance(value, str):
            return _expand_expr(self, value)
        else:
            return value

    def get_value(self, name: str, default: Any = None, raw: bool = False) -> Any:
        value = _try_get_value(self, name, raw=raw)
        if value is None and default is None:
            raise ValueError(f"Variable {name} not found")
        return value if value is not None else default

    def set_value(self, name: str, value: Any) -> None:
        if not _try_set_value(self, name, value):
            raise ValueError(f"Invalid variable name: {name}")

    def set_attr(self, name: str, value: Any) -> None:
        setattr(self.attrs, name, value)

    def get_inherited_attr(
        self, name: str, default: TResult | None = None
    ) -> TResult | None:
        result = default
        ctx: ContextNode | None = self
        while ctx is not None:
            if hasattr(ctx, name):
                result = cast(TResult, getattr(ctx, name))
                break
            elif name in ctx.attrs:
                result = cast(TResult, getattr(ctx.attrs, name))
                break
            else:
                ctx = ctx.parent
        return self.expand_expr(result)


class WorkflowContext(ContextNode):
    def __init__(self, definition: dict[str, Any]) -> None:
        super().__init__(None, definition)

        self.attrs.ensure_property("var", {})
        self.attrs.ensure_property("secrets", {})
        self.attrs.ensure_property("jobs", {})

        self.secrets = {
            **self.attrs.secrets,
            **dotenv_values(self.attrs.secrets_file or ".secrets"),
        }

        self.env = {
            **self.attrs.env,
        }

        self.sys_env = {
            **os.environ,
            **dotenv_values(self.attrs.env_file or ".env"),
        }

        self.jobs = {k: JobContext(self, k, v) for k, v in self.attrs.jobs.items()}
        self.var = dict(self.attrs.var)

        self.runs_on_host: dict[str, Any] | None = None

    def dispatch(self) -> process.ProcessResult:
        self.status = ExecutionStatus.RUNNING

        if self.attrs.runs_on:
            self.runs_on_host = process.prepare_host(
                self.expand_expr(self.attrs.runs_on)
            )

        try:
            for job in self.jobs.values():
                result = self.dispatch_job(job, no_deps=False)
                if not result:
                    continue

                self.result = result
                if result.failed and not job.attrs.continue_on_error:
                    self.failed = True
                    break

            return self.result

        finally:
            if self.status == ExecutionStatus.RUNNING:
                self.status = ExecutionStatus.FINISHED
            process.cleanup_host(self.runs_on_host)
            self.runs_on_host = None

    def dispatch_job(
        self, job: "JobContext", no_deps: bool
    ) -> process.ProcessResult | None:
        return self.__dispatch_job(job, no_deps, set())

    def __dispatch_job(
        self, job: "JobContext", no_deps: bool, visited_jobs: set[str]
    ) -> process.ProcessResult | None:
        if job.id in visited_jobs:
            raise CircularDependencyError("Circular reference detected")

        if job.status == ExecutionStatus.FINISHED:
            info(f"Job {job.id} already dispatched and finished")
            return job.result
        elif job.status == ExecutionStatus.SKIPPED:
            info(f"Re-running skipped job {job.id}")

        visited_jobs.add(job.id)

        if not no_deps:
            debug("Getting dependency map...")
            for dependency_id in job.attrs.depends_on or []:
                dep_job = self.jobs.get(dependency_id)
                if not dep_job:
                    raise RuntimeError(f"Invalid dependency job id: {dependency_id}")

                result = self.__dispatch_job(dep_job, no_deps, visited_jobs)
                if result and result.failed:
                    error(f"Dependency {dependency_id} failed")
                    return result

        if job.attrs.matrix:
            for matrix_tuple in product(*job.attrs.matrix.values()):
                job.matrix = {
                    key: self.expand_expr(value)
                    for key, value in zip(job.attrs.matrix.keys(), matrix_tuple)
                }
                result = job.dispatch()
                job.matrix = {}
                if result and result.failed:
                    return result

            return process.ProcessResult()
        else:
            return job.dispatch()


class InputOutputNode(ContextNode):
    def __init__(self, parent: ContextNode, definition: dict[str, Any]):
        super().__init__(parent, definition)

        self.inputs: dict[str, Any] = {}
        self.outputs: dict[str, Any] = {}

        self.sensitive_inputs: set[str] = {"password", "token"}

    def log_inputs(self) -> None:
        if not self.attrs._with:
            return
        info("with:")
        for k, v in self.attrs._with.items():
            v = self.expand_expr(v)
            self.inputs[k] = v
            if k in self.sensitive_inputs:
                info(f"  {k}: ********")
            else:
                info(f"  {k}: {safe_string(v)}")


class JobContext(InputOutputNode):
    def __init__(
        self, parent: WorkflowContext, step_id: str, definition: dict[str, Any]
    ):
        super().__init__(parent, definition)

        self.id = step_id

        self.runs_on_host: dict[str, Any] | None = None

        self.attrs.ensure_property("steps", [])
        self.attrs.ensure_property("continue_on_error", False)

        self.matrix: dict[str, Any] = {}

        self.env = {
            **parent.env,
            **self.attrs.env,
        }

        self.var = {
            **parent.var,
            **self.attrs.var,
        }

        self.steps: dict[str, StepContext] = {}
        for i, step in enumerate(self.attrs.steps):
            if "id" not in step:
                step["id"] = f"step_{i+1}"
            step_id = step["id"]
            step = StepContext(self, step)
            if not step.id:
                step.id = step_id
            self.steps[step_id] = step

    @property
    def workflow(self) -> WorkflowContext:
        return cast(WorkflowContext, self.parent)

    def dispatch(self) -> process.ProcessResult | None:
        self.status = ExecutionStatus.RUNNING

        info(f"** Run job '{self.display_name}'")

        if self.attrs.runs_on:
            self.runs_on_host = process.prepare_host(
                self.expand_expr(self.attrs.runs_on)
            )
        else:
            self.runs_on_host = self.workflow.runs_on_host

        try:
            if self.matrix:
                info("matrix:")
                for k, v in self.matrix.items():
                    info(f"  {k}: {v}")

            if not can_dispatch(self):
                self.status = ExecutionStatus.SKIPPED
                info("Job skipped")
                return None

            for step in self.steps.values():
                result = step.dispatch()
                if not result:
                    continue

                self.result = result

                if result.failed and not step.attrs.continue_on_error:
                    self.failed = True
                    break

        finally:
            if self.status == ExecutionStatus.RUNNING:
                self.status = ExecutionStatus.FINISHED
            process.cleanup_host(self.runs_on_host)
            self.runs_on_host = None

        return self.result

    def read_file(self, file_path: str) -> bytes:
        return _read_file(self, file_path)

    def write_file(self, file_path: str, content: bytes) -> None:
        _write_file(self, file_path, content)

    def exec(
        self,
        command: str,
        context: ContextNode,
        env: dict[str, str] | None = None,
        shell: str | None = None,
        stream_output: bool = False,
    ) -> process.ProcessResult:
        command = context.expand_expr(command).strip()
        if "${{" in command:
            raise ValueError("Command contains unexpanded variables")

        host = self.runs_on_host

        if context.get_inherited_attr("is_sensitive", False):
            stream_output = False

        # Define where to capture the output with the >> operator
        capture_filename = f"/tmp/{uuid4().hex}"
        debug(f"Capture file: {capture_filename}")
        touch_result = process.run(f"touch {capture_filename}", host)
        if touch_result.failed:
            error(
                f"Failed to create capture file {capture_filename}: {touch_result.error}"
            )
            return touch_result

        env = env or {}

        if "BLUISH_OUTPUT" in env:
            warning(
                "BLUISH_OUTPUT is a reserved environment variable. Overwriting it.",
            )

        env["BLUISH_OUTPUT"] = capture_filename

        env_str = "; ".join([f'{k}="{v}"' for k, v in env.items()]).strip()
        if env_str:
            command = f"{env_str}; {command}"

        if shell is None:
            shell = context.get_inherited_attr("shell", process.DEFAULT_SHELL)
        assert shell is not None

        interpreter = process.SHELLS.get(shell, shell)
        if interpreter:
            b64 = base64.b64encode(command.encode()).decode()
            command = f"echo {b64} | base64 -di - | {interpreter}"

        working_dir = context.get_inherited_attr("working_directory")
        if working_dir:
            debug(f"Working dir: {working_dir}")
            debug("Making sure working directory exists...")
            mkdir_result = process.run(f"mkdir -p {working_dir}", host)
            if mkdir_result.failed:
                error(
                    f"Failed to create working directory {working_dir}: {mkdir_result.error}"
                )
                return mkdir_result

            command = f'cd "{working_dir}" && {command}'

        def stdout_handler(line: str) -> None:
            info(decorate_for_log(line.rstrip(), "  > "))

        def stderr_handler(line: str) -> None:
            error(decorate_for_log(line.rstrip(), " ** "))

        run_result = process.run(
            command,
            host_opts=host,
            stdout_handler=stdout_handler if stream_output else None,
            stderr_handler=stderr_handler if stream_output else None,
        )

        # HACK: We should use our own process.read_file here,
        # but it currently causes an infinite recursion
        output_result = process.run(f"cat {capture_filename}", host)
        if output_result.failed:
            error(f"Failed to read capture file: {output_result.error}")
            return output_result

        for line in output_result.stdout.splitlines():
            k, v = line.split("=", maxsplit=1)
            context.outputs[k] = v

        return run_result


class StepContext(InputOutputNode):
    def __init__(self, parent: JobContext, definition: dict[str, Any]):
        super().__init__(parent, definition)

        self.attrs.ensure_property("name", "")
        self.attrs.ensure_property("uses", action.DEFAULT_ACTION)
        self.attrs.ensure_property("continue_on_error", False)
        self.attrs.ensure_property("shell", process.DEFAULT_SHELL)

        self.id = self.attrs.id

    @property
    def job(self) -> JobContext:
        return cast(JobContext, self.parent)

    @property
    def workflow(self) -> WorkflowContext:
        return self.job.workflow

    @property
    def display_name(self) -> str:
        if self.attrs.name:
            return self.attrs.name
        elif self.attrs.uses and self.attrs.uses != action.DEFAULT_ACTION:
            return self.attrs.uses
        elif self.attrs.run:
            return self.attrs.run.split("\n", maxsplit=1)[0]
        else:
            return self.id

    def dispatch(self) -> process.ProcessResult | None:
        info(f"* Run step '{self.display_name}'")

        if not can_dispatch(self):
            self.status = ExecutionStatus.SKIPPED
            info(" >>> Skipped")
            return None

        self.status = ExecutionStatus.RUNNING

        try:
            fn = action.REGISTERED_ACTIONS.get(self.attrs.uses or action.DEFAULT_ACTION)
            if not fn:
                raise ValueError(f"Unknown action: {self.attrs.uses}")

            if self.attrs.uses:
                info(f"Running {self.attrs.uses}")

            self.result = fn(self)
            self.failed = self.result.failed

        finally:
            self.status = ExecutionStatus.FINISHED

        return self.result


class VariableExpandError(Exception):
    pass


EXPR_REGEX = re.compile(r"\$?\$\{\{\s*([a-zA-Z_.][a-zA-Z0-9_.-]*)\s*\}\}")


ValueResult = namedtuple("ValueResult", ["value", "contains_secrets"])


def _try_get_value(ctx: ContextNode, name: str, raw: bool = False) -> Any:
    def prepare_value(value: Any) -> Any:
        if value is None:
            return None
        elif raw or not isinstance(value, str):
            return value
        else:
            return cast(str, _expand_expr(ctx, value))

    if "." not in name:
        # Handle a non-fully qualified variable name and avoid ambiguity
        member_result = _try_get_value(ctx, f".{name}", raw=raw)
        var_result = _try_get_value(ctx, f"var.{name}", raw=raw)

        if var_result and member_result:
            raise ValueError(f"Ambiguous value reference: {name}")
        else:
            return var_result or member_result or None

    root, varname = name.split(".", maxsplit=1)

    if root == "":
        if varname == "stdout":
            return prepare_value(
                "" if ctx.result is None else ctx.result.stdout.strip()
            )
        elif varname == "stderr":
            return prepare_value(
                "" if ctx.result is None else ctx.result.stderr.strip()
            )
        elif varname == "returncode":
            return prepare_value(0 if ctx.result is None else ctx.result.returncode)
    elif root == "env":
        current: ContextNode | None = ctx
        while current:
            for k in ("sys_env", "env"):
                dict_ = getattr(current, k, None)
                if dict_ and varname in dict_:
                    return prepare_value(dict_[varname])
            current = current.parent
    elif root == "var":
        current = ctx
        while current:
            if varname in current.var:
                return prepare_value(current.var[varname])
            current = current.parent
    elif root == "workflow":
        wf = ctx.workflow
        if wf:
            return _try_get_value(wf, varname, raw)
    elif root == "secrets":
        wf = ctx.workflow
        if wf and varname in wf.secrets:
            return prepare_value(
                RedactedString(cast(str, wf.secrets[varname]), "********")
            )
    elif root == "jobs":
        wf = ctx.workflow
        if wf:
            job_id, varname = varname.split(".", maxsplit=1)
            job = wf.jobs.get(job_id)
            if not job:
                raise ValueError(f"Job {job_id} not found")
            return _try_get_value(job, varname, raw)
    elif root == "job":
        job = ctx.job
        if job:
            return _try_get_value(job, varname, raw)
    elif root == "steps":
        job = ctx.job
        if job:
            step_id, varname = varname.split(".", maxsplit=1)
            step = job.steps.get(step_id)
            if not step:
                raise ValueError(f"Step {step_id} not found")
            return _try_get_value(step, varname, raw)
    elif root == "matrix":
        job = ctx.job
        if job and varname in job.matrix:
            return prepare_value(job.matrix[varname])
    elif root == "step":
        step = ctx.step
        if not step:
            raise ValueError("Step reference not found")
        return _try_get_value(step, varname, raw)
    elif root == "inputs":
        node = ctx.step or ctx.job
        if node and varname in node.inputs:
            if varname in node.sensitive_inputs:
                return prepare_value(RedactedString(node.inputs[varname], "********"))
            else:
                return prepare_value(node.inputs[varname])
    elif root == "outputs":
        node = ctx.step or ctx.job
        if node and varname in node.outputs:
            return prepare_value(node.outputs[varname])

    return None


def _try_set_value(ctx: "ContextNode", name: str, value: str) -> bool:
    if "." not in name:
        return False

    name = cast(str, _expand_expr(ctx, name))
    root, varname = name.split(".", maxsplit=1)
    if root == "":
        root, varname = varname.split(".", maxsplit=1)

    if root == "env":
        ctx.env[varname] = value
        return True
    elif root == "var":
        ctx.var[varname] = value
        return True
    elif root == "workflow":
        wf = ctx.workflow
        if wf:
            return _try_set_value(wf, varname, value)
    elif root == "jobs":
        wf = ctx.workflow
        if wf:
            job_id, varname = varname.split(".", maxsplit=1)
            job = wf.jobs.get(job_id)
            if not job:
                raise ValueError(f"Job {job_id} not found")
            return _try_set_value(job, varname, value)
    elif root == "job":
        job = ctx.job
        if job:
            return _try_set_value(job, varname, value)
    elif root == "steps":
        job = ctx.job
        if job:
            step_id, varname = varname.split(".", maxsplit=1)
            step = job.steps.get(step_id)
            if not step:
                raise ValueError(f"Step {step_id} not found")
            return _try_set_value(step, varname, value)
    elif root == "step":
        step = ctx.step
        if step:
            return _try_set_value(step, varname, value)
    elif root == "inputs":
        step = ctx.step
        if step:
            step.inputs[varname] = value
            return True
    elif root == "outputs":
        node = ctx.step or ctx.job
        if node:
            node.outputs[varname] = value
            return True

    return False


TExpandValue = str | dict[str, Any] | list[str]


def _expand_expr(
    ctx: ContextNode, value: TExpandValue | None, _depth: int = 1
) -> TExpandValue:
    if not isinstance(value, str):
        if isinstance(value, dict):
            return {k: _expand_expr(ctx, v, _depth=_depth) for k, v in value.items()}
        elif isinstance(value, list):
            return [cast(str, _expand_expr(ctx, v, _depth=_depth)) for v in value]
        else:
            return value  # type: ignore

    if "${{" not in value:
        return value

    return ctx.expression_parser(value)


def can_dispatch(context: StepContext | JobContext) -> bool:
    if context.attrs._if is None:
        return True

    info(f"Testing {context.attrs._if}")
    if isinstance(context.attrs._if, bool):
        return context.attrs._if
    elif not isinstance(context.attrs._if, str):
        raise ValueError("Condition must be a bool or a string")

    return bool(context.expand_expr(context.attrs._if))


def _read_file(ctx: ContextNode, file_path: str) -> bytes:
    """Reads a file from a host and returns its content as bytes."""

    job = ctx.job
    assert job is not None

    result = job.exec(f"base64 -i '{file_path}'", ctx)
    if result.failed:
        raise IOError(f"Failure reading from {file_path}: {result.error}")

    return base64.b64decode(result.stdout)


def _write_file(ctx: ContextNode, file_path: str, content: bytes) -> None:
    """Writes content to a file on a host."""

    job = ctx.job
    assert job is not None

    b64 = base64.b64encode(content).decode()

    result = job.exec(f"echo {b64} | base64 -di - > {file_path}", ctx)
    if result.failed:
        raise IOError(f"Failure writing to {file_path}: {result.error}")
