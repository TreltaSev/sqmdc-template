
import click
from tools import Tool
from rich.rule import Rule
from utils.console import console

@click.group(invoke_without_command=True)
def main():
    """Lists all available tools"""
    tools = Tool.find_all()

    console.print(Rule("Commands", style="dim"))
    for tool in tools:
        if not tool.runner:
            continue
        
        doc = tool.runner.__doc__ or ""

        console.print(f"[bold]{tool.name}[/bold] [dim]\n\t{doc}[/dim]\n")
