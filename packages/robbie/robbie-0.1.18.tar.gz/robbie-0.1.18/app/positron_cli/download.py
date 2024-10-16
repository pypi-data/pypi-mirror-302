import os
import shutil
import requests
import tarfile
import tqdm
from positron_common.job_api.list_jobs import list_jobs
from positron_common.job_api.get_job import get_job
from positron_common.cli.console import console
from positron_common.exceptions import RobbieException
from positron_common.cli.console import console, ROBBIE_BLUE, SPINNER
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.tree import Tree
from positron_common.cli.console import console
from positron_common.cli.logging_config import logger

# Prompts the user for FGs, environmetns, etc.
# Queries the backend for the FundingSources and Environments.
def download():
    """
    Download the artifacts from a previous Robbie run.

    """
    jobs = Jobs.load()
    jobs_choice = prompt('Choose a job to download: <tab for menu>: ', completer=WordCompleter(jobs.menu_items()))
    if jobs_choice == "":
        console.print("No job selected. Exiting.")
        return
    download_results(jobs.id_from_menu_item(jobs_choice))
    
def download_results(job_id: str):
    # download the results from the job
    job = get_job(job_id)

    if(job["resultsPresignedBucketInfo"] == None):
        raise RobbieException(f"No resultsPresignedBucketInfo for job {job_id}")

    logger.debug(f'Downloading results for: {job["name"]}')

    response = requests.get(job["resultsPresignedBucketInfo"],stream=True) 
    if response.status_code != 200:
        logger.debug(f'Failed to download URL, http code: {response.status_code} \n {response.text}')
        raise RobbieException('Sorry, run has no results to download.') 
    else:
        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        console.print(f'Download results for: {job["name"]}')
        with tqdm.tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open("./result.tar.gz", "wb") as file:
                logger.debug(f'Successfull opened ./result.tar.gz')
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

        if total_size != 0 and progress_bar.n != total_size:
            raise RobbieException(f'failed to download file')
    
        if os.path.exists("./job-execution") and os.path.isdir("./job-execution"):
            console.print("[green]✔[/green] Removed old job-execution directory.")
            shutil.rmtree("./job-execution")

        _decompress(tar_file="./result.tar.gz", path=".")
        # get rid of it
        os.remove("./result.tar.gz") 
        console.print("[green]✔[/green] Results now available.")

def _decompress(tar_file, path):
    """
    Extracts `tar_file` and puts the `members` to `path`.
    If members is None, all members on `tar_file` will be extracted.
    """
    tree = Tree("Remote files copied to Local Machine")

    tar = tarfile.open(tar_file, mode="r:gz")
    for member in tar.getmembers():
        logger.debug(f'Extracting {member.name}')
        tar.extract(member, path=path)
        tree.add(f"[yellow]{member.name}, size: {member.size} bytes[/yellow]")
    console.print(tree)
    tar.close()

# Naming
JOB_ID="id"
JOB_NAME="name"
JOB_MENU="menu"

# singleton builds a list of tuples from the DB results
class Jobs: 
    is_init: bool = False
    my_jobs: dict

    def __init__(self, jobs_arg: dict):
        if self.is_init:
            raise ValueError('Jobs.load() already initialized')
        else:
            self.init = True
            self.my_jobs= jobs_arg

    @staticmethod
    def load():
        jobs = list_jobs()
        if len(jobs) == 0:
            return None
        # Loop through and add a customer "menu" item to each dict (but only if the job actually ran)
        for key, val in jobs.items(): 
            if val["durationMs"] != None:
                val[JOB_MENU] = f'{val[JOB_NAME]} (Duration: {val["durationMs"]/1000} seconds)'
        return Jobs(jobs)
        
    # Prompt toolkit needs a list of strings to display in the menu 
    def menu_items(self) -> list: 
        ret_list: list = []
        for key, val in self.my_jobs.items():
            # just show names
            if val["durationMs"] != None:
                ret_list.append(val[JOB_MENU])
        return ret_list
    
    def id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_jobs.items():
            if val["durationMs"] != None and val[JOB_MENU] == menu_item:
                return val[JOB_ID]
        return None