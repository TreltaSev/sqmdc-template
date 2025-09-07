from pathlib import Path

import ctx
import click
from utils.console import console

@click.command
@ctx.pass_context
def ensure_caddy(ctx: ctx.Context):
    """Ensures caddyfile is generated"""
    
    project_root = ctx.obj.project_root
    
    config = ctx.obj.config
    
    host = config.get("host")
    
    # Determine template file
    template_path: Path = project_root / config.get("router.template_file", "Caddyfile.template")
    if ctx.obj.dev:
        template_path: Path = project_root / config.get("router.dev_template_file", "Caddyfile.dev.template")
    
    console.debug(f"Caddyfile: Template Path [dim]{template_path.resolve()}[/dim]")
    
    if not template_path.exists():
        console.error(f"Template file {template_path.resolve()} doesn't exist")
        ctx.abort()
        
    # Determine output file
    config_path: Path = project_root / config.get("router.config_file", None)
    
    console.debug(f"Caddyfile: Config Path [dim]{config_path.resolve()}[/dim]")
    
    if not config_path:
        console.error(f"Config path not specified in config")
    
    template_content = template_path.read_text()
    template_content = template_content.replace("{host}", host)
    
    config_path.write_text(template_content)
    
    
    