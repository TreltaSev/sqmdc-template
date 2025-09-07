import ctx
import click
from utils.console import console

from .ensure_caddy import ensure_caddy
from .ensure_certs import ensure_certs
from .ensure_config import ensure_config
from .ensure_database import ensure_database
from .ensure_ssh import ensure_ssh

@click.group(invoke_without_command=True)
@ctx.pass_context
def ensure(ctx: ctx.Context):
    """Exposes ensure-ables throughout the project"""
    if ctx.invoked_subcommand:
        return

    console.debug("Invoking all ensuring scripts")
    
    ctx.invoke(ensure_config)
    ctx.invoke(ensure_ssh)
    ctx.invoke(ensure_caddy)
    ctx.invoke(ensure_certs)
    ctx.invoke(ensure_database)
    
ensure.add_command(ensure_caddy, name="caddy")
ensure.add_command(ensure_config, name="config")
ensure.add_command(ensure_certs, name="certs")
ensure.add_command(ensure_database, name="database")
ensure.add_command(ensure_ssh, name="ssh")