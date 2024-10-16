import platform
from rich.console import Console

# Website colors
ROBBIE_BLUE='#41a7ff'
ROBBIE_DEFAULT='#ced7bd'
ROBBIE_ORANGE='#ff3a24'
ROBBIE_GREY='#f2f2f2'
SPINNER = "line" if platform.system() == "Windows" else "dots"

# Used to print nice message to the end user, this is not a logger. See `logging_config.py` for logging.
console = Console()
