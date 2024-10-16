import os
import typer
from typing_extensions import Annotated
from typing import Optional
from positron_common.deploy import positron_deploy
from positron_common.config import parse_job_config, PositronJobConfig, PositronJob
from positron_common.cli_args import args
from positron_common.cli.console import console, ROBBIE_DEFAULT, ROBBIE_BLUE, SPINNER
from positron_common.constants import JOB_CONF_YAML_PATH
from positron_common.cli.interactive import prompt_and_build_positron_job_config
from positron_common.cli.logging_config import logger
from positron_common.enums import JobRunType
from pipreqs.pipreqs import init
from logging import _nameToLevel
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from rich.text import Text
from rich.spinner import Spinner
from rich.live import Live


def run(
  name: Annotated[str, typer.Option("--name", help="Name of the run")] = None,
  commands: Annotated[Optional[str], typer.Argument(help='String of shell commands, a .py file, or a .ipynb file.')] = None,
  tail: Annotated[bool, typer.Option("--tail", help='Tail the run\'s stdout back to your CLI.')] = False,
  status: Annotated[bool, typer.Option("--s", help='Monitor run status in your CLI.')] = False,
  skip_prompts: Annotated[bool, typer.Option("--y", help='Bypass the prompts and execute the run immediately.')] = False,
  interactive: Annotated[bool, typer.Option("--i", help="Interactively choose your run configuration.")] = False,
  download: Annotated[bool, typer.Option("--download", help="Downloads the run results to your local machine.")] = False,
  create_only: Annotated[bool, typer.Option("--create-only", help="Only create the run, do not execute it. [Robbie internal use only]")] = False,
  auto_capture_deps: Annotated[bool, typer.Option("--auto-dep", help='(EXPERIMENTAL) Automatically resolve Python dependencies.')] = None
) -> None:
    """
    Run shell commands, a Python file, or Jupyter notebook as a batch run in Robbie

    You can optionally specify shell commands, a python file (.py), or Jupyter notebook (.ipynb) file to run.
    If no commands are specified, commands will be taken from the job_config.yaml file in the current directory.
    """

    # we can either stream or monitor status but not both at the same time
    if tail and status:
        console.print('[red]Error: Choose either the -logs and -s option.')
        return
    
    if (download and not tail and not status):    
        console.print('[red]Error: The --download option can only be used with the --tail or --s option.')
        return

    # initialize the argument singleton
    args.init(
        name=name,
        stream_stdout=tail,
        skip_prompts=skip_prompts,
        monitor_status=status,
        commands_to_run=commands,
        interactive=interactive,
        create_only=create_only,
        download=download,
        auto_capture_deps=auto_capture_deps
    )

    # first-level sanity checks
    if commands and interactive:
        console.print("[red]Sorry: Please specify command line or use the interactive mode.")
        return

    # need to readin the job_config.yaml file if it exists
    job_config = None
    if os.path.exists(JOB_CONF_YAML_PATH):
        console.print(f'Found run configuration file: {JOB_CONF_YAML_PATH}')
        job_config = parse_job_config(JOB_CONF_YAML_PATH)
        if not job_config:
            console.print('[red]Error parsing job_config.yaml file. See the documentation for more information.')
            return

    job_config.job_type = JobRunType.BASH_COMMAND_RUNNER
    # There are three possible scenarios:
    # 1. User types: robbie run - commands are run from the job_config.yaml file
    # 2. User types: robbie run "command" - commands override the job_config.yaml file
    # 3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created

    # Scenerio 1: User types: robbie run
    if not commands and not interactive:
        if not job_config:
            console.print('[red]Error: No job_config.yaml file found. Please specify commands to run.')
            return
        if not job_config.commands:
            console.print('[red]Error: No commands found in job_config.yaml file.')
            return

    # Scenerio 2. User types: robbie run "command" - commands override the job_config.yaml file 
    if commands:
        # Is there a job_config.yaml file?
        if not job_config:
            console.print('No job_config.yaml file found, using defaults.')
            job_config = PositronJob()
        
        # If commands are already there we are overriding them
        if job_config and job_config.commands:
            console.print('Overriding commands in job_config.yaml file.')
        
        job_config.commands = []
        job_config.commands.append(commands)

        # write out the updated job configuration file
        PositronJobConfig(version="1.0", python_job=job_config).write_to_file(filename=JOB_CONF_YAML_PATH)
        
    # Scenerio 3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created
    elif interactive:
        if os.path.exists(JOB_CONF_YAML_PATH):
            overwrite = prompt('A job_config.yaml file already exist, do you want to overwrite it? [y/[n]]:', style=Style.from_dict({'prompt': 'yellow'}))
            if overwrite in ["no", "n", "No", "N", ""]:
                console.print("[yellow]See you soon![/yellow]")
                return
        # lets prompt the user 
        console.print(f"Please follow the prompts to configure your run ([{ROBBIE_DEFAULT}][] = default[/{ROBBIE_DEFAULT}], <tab> for options)")
        cfg = prompt_and_build_positron_job_config()
        logger.debug("interactive cfg: ", cfg)
        if cfg == None:
            console.print(f"[red]Sorry, failed to create a file {JOB_CONF_YAML_PATH}")
            return
        if cfg.python_job.commands == None:
            console.print("[red]Error: You did not specify any commands to run.")
            return
        cfg.write_to_file(filename=JOB_CONF_YAML_PATH)
        job_config = cfg.python_job

    # Handle auto capturing dependencies for non-Conda environments
    # this comes in two forms:
    # 1. User types: robbie run --auto-dep
    # 2. job_config.yaml file has dependencies: auto-capture
    overwrite_reqs = False
    if auto_capture_deps or job_config.dependencies == "auto-capture":
        if os.path.exists("./requirements.txt"):
            if args.skip_prompts == False:
                overwrite_reqs = prompt('A requirement.txt file already exist, do you want to overwrite it? [y/N]:', style=Style.from_dict({'prompt': 'yellow'}))
                if overwrite_reqs in ["no", "n", "No", "N", ""]:
                    console.print("[yellow]See you soon![/yellow]")
                    return
            else:
                overwrite_reqs = True
            
        # arguments for pipreqs package - https://github.com/bndr/pipreqs
        pipreq_args = {
            "<path>": ".",
            "--print": False,
            "--savepath": None,
            "--pypi-server": None,
            "--proxy": None,
            "--use-local": False,
            "--diff": None,
            "--clean": None,
            "--mode": None,
            "--scan-notebooks": True,
            "--force": False
        }
        if overwrite_reqs:
            pipreq_args["--force"] = True

        with Live(Spinner(SPINNER, text=Text("Analyzing Python (.py) and Notebook (.ipynb) files for dependencies", style=ROBBIE_BLUE)),refresh_per_second=20, console=console, transient=True):
            init(pipreq_args) # this is the pipreqs call    
            console.print("[green]✔[/green] Dependency analysis complete, requirements.txt file created.")
        job_config.dependencies = "./requirements.txt"

    positron_deploy(job_config)



