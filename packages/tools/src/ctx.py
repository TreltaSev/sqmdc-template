# === Core ===
import os
from re import sub
from tokenize import Triple
import click
import pathlib
import platform
import subprocess

from paramiko import SSHClient
import paramiko

# === Utils ===
from utils.helper.config import Yaml

# === Type ===
import typing as t
import typing_extensions as te

R = t.TypeVar("R")
P = te.ParamSpec("P")

subprocess_output_types = t.Literal[subprocess.PIPE, subprocess.STDOUT, subprocess.DEVNULL]

class ContextObject():
    """
    Context object containing key information on the project itself
    This object is passed through the click context through ctx.obj
    """

    def __init__(self) -> None:
        self.project_root = pathlib.Path("/project/")
        self.host_root = pathlib.Path("/host_home/")
        self.dev: bool = False
    
    @property
    def host_cwd(self) -> pathlib.Path:
        _host_cwd = os.environ.get("HOST_CWD", None)
        if not _host_cwd:
            raise FileNotFoundError("HOST_CWD not set")
        return pathlib.Path(_host_cwd) 
        
    @property
    def config(self) -> Yaml:
        return Yaml("/project/config.yml", lazy=True)
    
    @property
    def os(self) -> None | t.Literal["Linux", "Windows"] | str:
        """
        Operating system of the runner of the script, should always be linux unless you're doing some funky stuff.
        """
        _os = platform.system()
        return _os if _os in ["Linux", "Windows"] else None
    
    def run_on_path(self, cmd: str, cwd: pathlib.Path | str, stdout: t.Optional[int] = None, stderr: t.Optional[int] = None, *, no_output: t.Optional[bool] = None) -> None:
        """
        Runs a command within a given path
        
        # Usage
        ```
        @ctx.pass_context
        def foo(ctx: ctx.Context):
            ctx.obj.run_on_path("ls", "/")
        ```
        """
        
        # Ensure cwd is a valid path object
        if isinstance(cwd, str):
            cwd = pathlib.Path(cwd)
            
        if not cwd.exists():
            raise LookupError(f"cwd {cwd.resolve()} doesn't exist.")
            
        # Abide by no output
        if (no_output is True):
            stdout = subprocess.DEVNULL
            stderr = subprocess.DEVNULL
            
        # Make the call
        subprocess.run(cmd.split(" "), cwd=cwd, stdout=stdout, stderr=stderr)
    
    def run_on_ssh(self, ssh: SSHClient, cmd: str, cwd: pathlib.Path | str | None = None) -> tuple[str, str]:
        """
        Sends a command through an ssh object
        """
        
        if cwd is None:
            cwd = self.host_cwd
        
        # Ensure cwd is a valid path object
        if isinstance(cwd, str):
            cwd = pathlib.Path(cwd)
        
        # change dir to working directory
        cmd = f"cd {cwd.resolve()} && {cmd}"
        
        # Run command
        _in, _out, _err = ssh.exec_command(cmd)        
        _in.close()
        
        return _out.read().decode(), _err.read().decode()
        
    def host_has_command(self, ssh: SSHClient, command: str) -> bool:
        """
        Checks if the host from the ssh connection has a command
        """
        
        _out, _err = self.run_on_ssh(ssh, f"command -v {command}")
        return _out != ""
            
class Context(click.Context):
    """
    Context type helper to type annotate the original click context object,
    to use the :type:`ContextObject` type.
    """
    obj: ContextObject


def pass_context(func: t.Callable[te.Concatenate[Context, P], R]) -> t.Callable[P, R]:
    """
    Method used to replace the regular click.pass_context method, instead of just
    returning a regular click context, return one that is type hinted to include
    the context change.

    # Usage
    ```python
    import ctx

    @ctx.pass_context
    def subcommand(ctx: ctx.Context):
        print(ctx.obj)
    ```
    """
    def decorator(*args, **kwargs):
        ctx = t.cast(Context, click.get_current_context())
        return func(ctx, *args, **kwargs)
    return decorator
