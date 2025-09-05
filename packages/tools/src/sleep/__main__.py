
import click
from time import sleep

from utils.console import console

@click.group(invoke_without_command=True)
def main():
    """Runs sleep"""
    
    console.debug("TOOL:SLEEP Sleeping")
    
    sleep(10**4)
