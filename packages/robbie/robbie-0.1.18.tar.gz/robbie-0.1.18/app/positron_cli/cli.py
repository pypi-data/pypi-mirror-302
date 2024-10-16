import typer
from positron_cli.run import run
from positron_cli.login import login
from positron_cli.set_env import set_env
from positron_cli.configure import configure
from positron_cli.download import download
from positron_common.cli.console import console
from .set_log_level import log_level
import pyfiglet
  
ascii_banner = pyfiglet.figlet_format("Robbie")
console.print(ascii_banner, style='#41a7ff')
app = typer.Typer(help="A CLI tool to help you run your code in the Robbie")

app.callback()(log_level)
app.command()(run)
app.command()(login)
app.command()(set_env)
app.command()(configure)
app.command()(download)

if __name__ == "__main__":
    app()
