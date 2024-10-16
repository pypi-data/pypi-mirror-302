from pydantic import BaseModel
from typing import List, Optional

class PositronCLIArgs(BaseModel):
    """
    Positron CLI command line arguments.
    """
    is_init: bool = False
    name: Optional[str] = None
    local: bool = False
    deploy: bool = False
    stream_stdout: bool = False
    job_args: Optional[List[str]] = None
    skip_prompts: bool = False
    monitor_status: bool = False
    commands_to_run: Optional[str] = None
    interactive: bool = False
    create_only: bool = False
    results_from_job_id: str = ""
    download: bool = False
    auto_capture_deps: bool = False


    def init(self,
        name: Optional[str] = None,
        local: bool = False,
        deploy: bool = False,
        stream_stdout: bool = False,
        job_args: Optional[List[str]] = None,
        skip_prompts: bool = False,
        monitor_status: bool = False,
        commands_to_run: Optional[str] = None,
        interactive: bool = False,
        create_only: bool = False,
        results_from_job_id: str = "",
        download: bool = False,
        auto_capture_deps: bool = False
    ):
        if self.is_init:
            raise ValueError('CLI Args already initialized')
        
        self.name = name
        self.local = local
        self.deploy = deploy
        self.stream_stdout = stream_stdout
        self.job_args = job_args
        self.is_init = True
        self.skip_prompts=skip_prompts
        self.monitor_status=monitor_status
        self.commands_to_run = commands_to_run
        self.interactive = interactive
        self.create_only = create_only
        self.results_from_job_id = results_from_job_id
        self.download = download
        self.auto_capture_deps = auto_capture_deps


#
# Export global (singleton)
#
args = PositronCLIArgs()
"""
Global CLI arguments singleton, make sure you call init() before using it.
"""
