import time
import signal
import json
import os
import sys
from rich.text import Text
from rich.spinner import Spinner
from rich.live import Live
from rich.prompt import Confirm
from positron_common.exceptions import RemoteCallException
from positron_common.env_config import env
from positron_common.config import PositronJob
from positron_common.cli_args import args as cli_args
from positron_common.print import print_robbie_configuration_banner, print_job_details_banner, print_job_complete_banner, print_known_error
from positron_common.cli.console import console, ROBBIE_BLUE, SPINNER
from positron_common.constants import temp_path
from positron_common.compression import create_workspace_tar
from positron_common.cli.logging_config import logger
from positron_common.job_api.stream_logs import start_stdout_stream
from positron_common.job_api.get_job import get_job
from positron_common.job_api.start_job import start_job
from positron_common.job_api.terminate_job import terminate_job
from positron_common.job_api.create_job import create_job
from positron_common.utils import get_default_workspace_dir
from positron_common.aws.s3_presigned_handler import S3PresignedHandler
from positron_cli.download import download_results

#sys.exit() codes
SUCCESS=0
FAILURE=1

# number of seconds to poll when monitoring job status
POLLING_SEC=1

# for the the deep link
PORTAL_BASE = env.API_BASE.rstrip('/api')
    
# Cloud deployment definition
def positron_deploy(job_config: PositronJob):
    signal.signal(signal.SIGINT, handle_sigint)
    logger.debug(env)
    
    try:
        logger.debug(f'Job Config: {job_config}')
        job_config.validate_values()

        # TODO: We should not be creating a job before we let the user run it, we need defaults in the DBs that we can query
        logger.debug(job_config.create_runtime_env())
        job = create_job(job_config=job_config)
        logger.debug(json.dumps(job, indent=4))
        
        # print the configuration banner
        print_robbie_configuration_banner(job, job_config)
    
        # prompt the user if they don't pass the -y option
        if not cli_args.skip_prompts:
            user_input = input("Run job with these settings? ([y]/n)")
            if not user_input in ["yes", "y", "Yes", "Y", ""]:
                terminate_job(job["id"], "User declined from CLI")
                console.print("[yellow]See you soon![/yellow]")
                return

        # tell people we are on the local machine
        console.print("[bold]Local Machine: [/bold]", style=ROBBIE_BLUE)    

        workspace_dir = (job_config.workspace_dir if job_config.workspace_dir else get_default_workspace_dir())
        logger.debug(f'Workspace directory: {workspace_dir}')
        
        if os.path.exists(workspace_dir):
            console.print(f'Workspace directory: {workspace_dir}')
        else:
            console.print(f"[bold red] ERROR: Workspace directory does not exist: {workspace_dir}")
            return

        # show the spinner as we compress the workspace
        with Live(Spinner(SPINNER, text=Text("Compressing workspace...(1 of 3)", style=ROBBIE_BLUE)),refresh_per_second=20, console=console, transient=True):
            file_count = create_workspace_tar(workspace_dir=workspace_dir)
            console.print("[green]✔[/green] Workspace compression complete (1 of 3)")

        if file_count == 0:
            Confirm.ask("No files were found in the workspace directory. Would you like to continue anyway?", default=False)
    
        # show the spinner as we upload
        with Live(Spinner(SPINNER, text=Text("Uploading compressed workspace to Robbie...(2 of 3)", style=ROBBIE_BLUE)),refresh_per_second=20, console=console, transient=True):
            S3PresignedHandler.upload_file_to_job_folder(f"{temp_path}/{env.COMPRESSED_WS_NAME}", job['id'], env.COMPRESSED_WS_NAME)
            console.print("[green]✔[/green] Workspace uploaded to Robbie (2 of 3)")
        
        if cli_args.create_only:
            console.print(f"[green]✔[/green] Job created successfully. (3 of 3)")
            console.print(f"JOB_ID: {job.get('id')}")
            return

        # spin while submitting job
        with Live(Spinner(SPINNER, text=Text("Submitting job to Robbie...(3 of 3)", style=ROBBIE_BLUE)),refresh_per_second=20, console=console, transient=True):
            start_job(job_id=job['id'], data=job_config.create_runtime_env())
            console.print(f"[green]✔[/green] Successfully submitted job to Robbie. (3 of 3)")

        start = time.perf_counter()
        print_job_details_banner(job)

        # Are we streaming stdout or just showing the status changes.
        if cli_args.stream_stdout:
            # tell people we are on the remote machine
            console.print("[bold]Remote Machine Status: [/bold]", style=ROBBIE_BLUE)  
            start_stdout_stream(job['id'])
            # job is done now, diplay final results.    
            final_get_job = get_job(job['id'])
            print_job_complete_banner(final_get_job, start)
            if cli_args.download:
                # download the results
                download_results(final_get_job['id'])
            
            if _was_job_a_success(final_get_job):
                sys.exit(SUCCESS)
            else:
                sys.exit(FAILURE)
            
        else:
            if cli_args.monitor_status:
                # lets track and display the status updates
                console.print(f"You can also monitor job status in the Robbie portal at: {PORTAL_BASE}/portal/app/my-runs?jobId={job['id']}\n", style=ROBBIE_BLUE) 
                
                # tell people we are on the remote machine
                console.print("[bold]Remote Machine Status: [/bold]", style=ROBBIE_BLUE)  
                last_status_change = "Starting..."
                final_get_job = None
        
                with Live(Spinner(SPINNER, text=Text("Processing...", style=ROBBIE_BLUE)),refresh_per_second=20, console=console):    
                    while True:
                        job_result = get_job(job['id'])
                        # are we in a final state?
                        if(_is_job_done(job_result)):
                            break
                        if(job_result['status'] != last_status_change):
                            # there has been a status change
                            time1 = time.strftime("%H:%M:%S")
                            console.print(f"\t{time1}: {job_result['status']}")
                            last_status_change = job_result['status']
                        time.sleep(POLLING_SEC)
                # job is down now, diplay final results.    
                final_get_job = get_job(job['id'])
                print_job_complete_banner(final_get_job, start)
                if cli_args.download:
                    # download the results
                    download_results(final_get_job['id'])
                
                if _was_job_a_success(final_get_job):
                    sys.exit(SUCCESS)
                else:
                    sys.exit(FAILURE)
            else:
                console.print(f"You can monitor job status in the Robbie portal at: {PORTAL_BASE}/portal/app/my-runs?jobId={job['id']}", style=ROBBIE_BLUE) 
                sys.exit(SUCCESS)
    except RemoteCallException as e:
            """For known errors we dont print exceptions, we just print the user friendly message"""
            print_known_error(e)
            sys.exit(FAILURE)
    except Exception as e:
        # don't let this propogate up, we want to catch all exceptions
        logger.exception(e)
        print(e)
        sys.exit(FAILURE)

def _is_job_done(job) -> bool:
    return job['status'] == "terminated" or job['status'] == "complete" or job['status'] == "failed" or job['status'] == "execution_error"

def _was_job_a_success(job) -> bool:
    return job['status'] == "complete"

def handle_sigint(signum, frame):
    console.print('Terminating gracefully...')
    # TODO: we should actually close open connections
    sys.exit(FAILURE)
