import ctx
import click
from utils.console import console


@click.command
@ctx.pass_context
def ensure_config(ctx: ctx.Context):
    """Ensures config exists and is valid"""
    config_path = ctx.obj.project_root / "config.yml"
    config_example_path = ctx.obj.project_root / "config.example.yml"
    
    # Fail if the config example file doesn't exist
    if not config_example_path.exists():
        console.error("Config example file doesn't exist in project root... did you delete it?")
        ctx.abort()
    
    # If the config_path is a folder, remove it
    if config_path.is_dir():
        config_path.rmdir()
    
    # If the config file doesn't exist, create it
    if not config_path.exists():
        config_path.write_text(config_example_path.read_text())
        console.info("Wrote to config file")
    else:
        console.debug("Config file exists.")