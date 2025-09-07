# === Core ===
import click

# === Utils ===
from utils.console import console
from utils.helper.config import Yaml

# === Typing ===
from typing import Optional
from collections.abc import Mapping

from tools import Tool
from ctx import ContextObject


@click.group(invoke_without_command=True)
@click.argument("toolname", required=False)
@click.argument("args", nargs=-1)
@click.option("--dev", is_flag=True)
@click.pass_context
def cli(ctx, toolname: Optional[str], args, dev: bool = False):
    """Cli Entry"""
    tools = Tool.find_all()
    runners: Mapping[str, Tool] = {tool.name: tool for tool in tools}

    if toolname is None:
        console.error(f"You didn't specify a tool, try running [blue]just tool ls[/] to view all possible tools")
        return

    if toolname not in runners:
        console.error(f"Failed to run the tool {toolname}, it wasn't found. Try running [blue]just tool ls[/] to view all possible tools")
        return
    
    context_object = ContextObject()
    context_object.dev = dev
    
    runners[toolname].run(*args, obj=context_object)
    

def main():
    """Setup.py Entry"""
    cli()


# Run Entry
if __name__ == "__main__":
    main()
