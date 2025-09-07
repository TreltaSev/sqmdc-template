from pathlib import Path
import os
import ctx
import click
import paramiko
from utils.console import console

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

@click.command
@ctx.pass_context
def ensure_certs(ctx: ctx.Context):
    """Ensures caddy certs for local development"""
    host_user = os.environ.get("HOST_USER", "root")
    
    config = ctx.obj.config

    host: str | None = config.get("host")
    ssh_file_out: Path = ctx.obj.project_root / config.get("tool.ssh_file_out")
    
    
    
    path_certs: Path = ctx.obj.project_root / "certs"
    
    # Ensure certs folder exists
    if not path_certs.exists():
        path_certs.mkdir()
        
    for file in path_certs.glob("*.pem"):
        file.unlink()
    
    # Get extra subdomains from config
    extra_subdomains: list[str] = ctx.obj.config.get("router.extra_subdomains") or []
    if not isinstance(extra_subdomains, list):
        console.error(f"CONFIG: extra_subdomains isn't a valid list, is [red]{type(extra_subdomains).__name__}[/red] instead")        
        ctx.abort()
    
    # Generated host list
    expected_certs = [host, *[f"{sub}.{host}" for sub in extra_subdomains]]
    
    # Connect to host via ssh
    ssh.connect(
        hostname="host.docker.internal",
        username=host_user,
        key_filename=str(ssh_file_out.resolve())
    )
    
    
    if not ctx.obj.host_has_command(ssh, "mkcert"):
        console.error("This command requires mkcert to be installed on the host machine")
        ctx.abort()
    
    # Make cert files
    console.info(f"Installing local ca in system trust store in {(ctx.obj.host_cwd / 'certs').absolute()}")
    ctx.obj.run_on_ssh(ssh, cmd="mkcert -install", cwd=ctx.obj.host_cwd / "certs")
    
    for cert in expected_certs:
        console.info(f"Generating certfile for [blue]{cert}[/blue] on {path_certs.resolve()}")
        ctx.obj.run_on_ssh(ssh, cmd=f"mkcert {cert}", cwd=ctx.obj.host_cwd / "certs")
    
    ssh.close()