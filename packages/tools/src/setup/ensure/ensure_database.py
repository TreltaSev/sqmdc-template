import ctx
import click
from utils.console import console



@click.command
@ctx.pass_context
def ensure_database(ctx: ctx.Context):
    """Ensures the database init file exists"""
    init_file = ctx.obj.project_root / "packages/database/init.js"
    template_init_file = ctx.obj.project_root / "packages/database/template.init.js"
    template_contents = template_init_file.read_text()
    
    username, password, auth_db = ctx.obj.config.get("database").values()
    tTable = [["username", username], ["password", password], ["auth_db", auth_db]]
    
    for key, value in tTable:
        template_contents = template_contents.replace(f"{{{key}}}", value)
        
    if init_file.is_dir():
        init_file.rmdir()
    
    init_file.write_text(template_contents)
    console.info("Generated [blue]init.js[/blue] file")