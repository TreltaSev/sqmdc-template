from pathlib import Path

import ctx
import click
from utils.console import console

@click.command
@ctx.pass_context
def ensure_ssh(ctx: ctx.Context):
    """Ensure ssh key files exist"""
    
    config = ctx.obj.config
    
    ssh_identity = config.get("tool.ssh_identity", None)
    ssh_file_out = config.get("tool.ssh_file_out", None)
    
    host_ssh_authorized_keys_path = ctx.obj.host_root / ".ssh/authorized_keys"
    host_ssh_authorized_keys_contents = host_ssh_authorized_keys_path.read_text()
    
    if not ssh_identity:
        raise KeyError(f"Missing ssh_identity in tool config")
    
    if not ssh_file_out:
        raise KeyError(f"Missing ssh_file_out in tool config")
    
    ssh_file_out: Path = ctx.obj.project_root / ssh_file_out    
    ssh_file_out_pub: Path = ssh_file_out.with_suffix(ssh_file_out.suffix + ".pub")
    
    project_root = ctx.obj.project_root
    ssh_folder = project_root / "packages/tools/ssh"
    
    # Remove ssh if its a file
    if ssh_folder.is_file():
        ssh_folder.unlink()
    
    # Ensure folder exists
    if not ssh_folder.exists():
        ssh_folder.mkdir()
        
    console.info("Checking if tool already has acceptable ssh-key")
    
    key_exists = f'"{ssh_identity}"' in host_ssh_authorized_keys_contents
    
    if key_exists:
        console.log(f"Identity key [red]{ssh_identity}[/red] already exists in authorized keys, skipping...")
    else:
        # Remove files if they don't exist
        ssh_file_out.unlink(missing_ok=True)
        ssh_file_out_pub.unlink(missing_ok=True)   
        
        # Generate pair
        ctx.obj.run_on_path(f'ssh-keygen -t ed25519 -C "{ssh_identity}" -N  -f {ssh_file_out.resolve()}', "/project", no_output=True)
        console.log("Generated identity pair")
        
        # Save to authorized keys
        with host_ssh_authorized_keys_path.open("a+") as authorized_keys:
            authorized_keys.write(ssh_file_out_pub.read_text())
            console.log("Updated host's authorized keys")
    
    
    
    
    