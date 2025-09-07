import ctx
import click
from utils.console import console

from .ensure import ensure


# setup #
@click.group(invoke_without_command=True)
@ctx.pass_context
def main(ctx: ctx.Context):
    """Exposes setup scripts used for this project"""
    if ctx.invoked_subcommand:
        return

    console.debug("Invoking all setup subcommands")

    ctx.invoke(ensure)

main.add_command(ensure, name="ensure")

