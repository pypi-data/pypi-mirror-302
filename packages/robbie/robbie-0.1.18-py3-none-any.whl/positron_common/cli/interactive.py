
import os
from positron_common.job_api.funding_envs_images import list_environments, list_funding_sources, list_images
from positron_common.cli.console import console, ROBBIE_BLUE, ROBBIE_DEFAULT
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from positron_common.config import PositronJob
from positron_common.config import PositronJobConfig


# Prompts the user for FGs, environmetns, etc.
# Queries the backend for the FundingSources and Environments.
def prompt_and_build_positron_job_config(
) -> PositronJobConfig:

    try:
        pj = PositronJob()

        style = Style.from_dict({
            'completion-menu.completion': 'bg:#008888 #ffffff',
            'completion-menu.completion.current': 'bg:#00aaaa #000000',
        })
        # user can enter a name

        message = [
            (ROBBIE_BLUE, "Please enter a custom run name ["),
            (ROBBIE_DEFAULT, "let Robbie choose"),
            (ROBBIE_BLUE, "]:" ),
        ]
        name_choice = prompt(message=message, style=style)
        if len(name_choice):
            pj.name = name_choice

        # fetch the names and ids
        fs = FundingSources.load()

        message = [ 
            (ROBBIE_BLUE, "Select how to bill your job ["),
            (ROBBIE_DEFAULT, "Personal tokens"),
            (ROBBIE_BLUE, "]:" ),
        ]
        fs_choice = prompt(message=message, completer=WordCompleter(fs.menu_items()), style=style)

        if len(fs_choice):
            fs_id = fs.id_from_menu_item(fs_choice)
        else:
            fs_id = fs.default_funding_source_id()
            
        pj.funding_group_id = fs_id

        #
        # Envrionments
        #
        # are there any environments in this funding source?
        envs = Environments.load(pj.funding_group_id)
        if envs:
            message = [ 
                (ROBBIE_BLUE, "Select your preferred hardware ["),
                (ROBBIE_DEFAULT, "None" if not fs.default_env_name_from_fs_id(fs_id) else fs.default_env_name_from_fs_id(fs_id)), # this is null for personal
                (ROBBIE_BLUE, "]:" ),
            ]
            env_choice = prompt(message=message, completer=WordCompleter(envs.menu_items()), style=style)
        else:
            # no environments for the user oh well
            console.print(f"[red]Error your funding sources: {fs_choice} has no approved hardware, please contact 'support@robbie.run'")
            return None

        if len(env_choice):
            pj.environment_id = envs.id_from_menu_item(env_choice)
        else:
            # choose the default, if available
            if fs.default_env_id_from_fs_id(fs_id) == None:
                console.print(f"[red] Error funding source: {fs_choice} has no default hardware and you didn't specify any.")
                return None
            else:
                pj.environment_id = fs.default_env_id_from_fs_id(fs_id)

        #
        # Images
        #
        images = Images.load(pj.funding_group_id, pj.environment_id)

        # Prompt the user with default and coloring
        message = [ 
                (ROBBIE_BLUE, "Select your preferred image["),
                (ROBBIE_DEFAULT, "None" if not fs.default_image_name(fs_id) else fs.default_image_name(fs_id)),
                (ROBBIE_BLUE, "]:" ),
            ]
        image_choice = prompt(message=message, completer=WordCompleter(images.menu_items()), style=style)

        if len(image_choice):
            pj.image = images.name_from_menu_item(image_choice)
        else:
            # choose the default, if available
            if fs.default_image_name(fs_id) == None:
                console.print(f"[red] Error funding source: {fs_choice} has no default hardware and you didn't specify any.")
                return None
            else:
                pj.image = fs.default_image_name(fs_id)

        message = [ 
                (ROBBIE_BLUE, "Dependencies["),
                (ROBBIE_DEFAULT, "none"),
                (ROBBIE_BLUE, "]:" ),
            ]
        deps = prompt(message=message, completer=WordCompleter(["auto-capture", "./requirements.txt" ]), style=style)
        if len(deps):
            pj.dependencies = deps

        message = [ 
                (ROBBIE_BLUE, "Max tokens ["),
                (ROBBIE_DEFAULT, "none"),
                (ROBBIE_BLUE, "]:" ),
            ]
        text = prompt(message=message, style=style)
        if len(text):
            pj.max_tokens = text
        
        message = [ 
                (ROBBIE_BLUE, "Max time in HH:MM format ["),
                (ROBBIE_DEFAULT, "none"),
                (ROBBIE_BLUE, "]:" ),
            ]
        text = prompt(message=message,style=style)
        if len(text):
            pj.max_tokens = text

        message = [ 
                (ROBBIE_BLUE, "Specify the directory contents to send to the remote machine ["),
                (ROBBIE_DEFAULT, os.getcwd()),
                (ROBBIE_BLUE, "]:" ),
            ]
        text = prompt(message=message, style=style)
        if len(text):
            pj.workspace_dir = text
        else:
            pj.workspace_dir = os.getcwd()

        # environment variables are part of a nested dict
        first_pass = True
        while True:
            var_name = prompt('Environment variable name <return to exit>:',style=Style.from_dict({'prompt': ROBBIE_BLUE}))
            if not var_name:
                break
            var_value = prompt(f'Value for {var_name} (hint=hit <return> to use local machine value):', style=style)
            if first_pass:
                pj.env = {}
                first_pass = False
            pj.env[var_name] = var_value

        # loop through and create a big string of commands
        first_pass = True
        while True:
            cmd = prompt('Enter command to run <return to exit>:', style=Style.from_dict({'prompt': ROBBIE_BLUE}))
            if not cmd:
                break
            if first_pass:
                pj.commands = []
                first_pass = False
            pj.commands.append(cmd)

        return PositronJobConfig(version="1.0", python_job=pj)
    
    except Exception as e:
       print(f"Error: {e}")
       return None



# Naming
FS_ID="id"
FS_NAME="name"
FS_TOKENS="userTokens"
FS_MENU="menu"
FS_TYPE="type"
FS_DEFAULT_IMAGE_NAME="defaultImageName"
FS_DEFAULT_IMAGE_ID="defaultImageId"
FS_DEF_ENV_NAME="defaultEnvironmentName"
FS_DEF_ENV_ID="defaultEnvironmentId"
FS_PERSONAL_NAME="Personal"
FS_PERSONAL_TYPE="PERSONAL"


# Class and singleton builds a list of tuples from the DB results
class FundingSources: 
    is_init: bool = False
    my_fs: dict

    def __init__(self, fs_arg: dict):
        if self.is_init:
            raise ValueError('FundingSources.load() already initialized')
        else:
            self.init = True
            self.my_fs= fs_arg

    @staticmethod
    def load():
        fs = list_funding_sources()
        if len(fs) == 0:
            return None
        # Loop through and add a customer "menu" item to each dict 
        for key, val in fs.items(): 
                val[FS_MENU] = f'{val[FS_NAME]} ({val[FS_TOKENS]} tokens available)'
        return FundingSources(fs)
        
    # Prompt toolkit needs a list of strings to display in the menu 
    def menu_items(self) -> list: 
        ret_list: list = []
        for key, val in self.my_fs.items():
            # just show names
            ret_list.append(val[FS_MENU])
        return ret_list

    # Return 'funding_group_id' using the val returned from session.prompt() 
    def id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val.get(FS_ID)
        return None

    def default_env_id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val.get(FS_DEF_ENV_ID)
        return None
    
    def default_env_name_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val.get(FS_DEF_ENV_NAME)
        return None
    
    def default_env_name_from_fs_id(self, id: str) -> str:
        for key, val in self.my_fs.items():
                if (val[FS_ID] == id):
                    return val.get(FS_DEF_ENV_NAME)
        return None
    
    def default_env_id_from_fs_id(self, id: str) -> str:
        for key, val in self.my_fs.items():
                if (val[FS_ID] == id):
                    return val.get(FS_DEF_ENV_ID)
        return None
    
    def default_env_id(self) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return val.get(FS_DEF_ENV_ID)
        return None
    
    def default_funding_source_id(self) -> str: 
        for key, val in self.my_fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return val.get(FS_ID)
        return None
    
    def default_image_name(self, id: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_ID] == id):
                return val.get(FS_DEFAULT_IMAGE_NAME)
        return None
    
    def default_image_id(self, id: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_ID] == id):
                return val.get(FS_DEFAULT_IMAGE_ID)
        return None
    


# offsets for the list of tuples
ENV_NAME="environmentName"
ENV_ID="id"
ENV_TPH="tokensPerHour"
ENV_MENU_ITEM="menu"

# singleton for Environments
class Environments: 
    is_init: bool = False
    my_envs: dict

    def __init__(self, env_arg):
         if self.is_init:
            raise ValueError('Environments.load() already initialized')
         else:
            self.my_envs = env_arg
            self.is_init = True

    @staticmethod
    def load(fs_id: str):
        envs = list_environments(fs_id)
        if len(envs) == 0:
            return None
        for key, val in envs.items():
            val[ENV_MENU_ITEM] = f"{val['environmentName']} ({val['tokensPerHour']} Tokens/Hour)" # shows in menu
        return Environments(envs)

    def menu_items(self) -> list: 
        menu_list = []
        for key, val in self.my_envs.items():
            menu_list.append(val[ENV_MENU_ITEM])
        return menu_list

    def id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_envs.items():
            if (val[ENV_MENU_ITEM] == menu_item):
                return val.get(ENV_ID)
        return None

    def tokens_per_hour(self, env_id: str) -> str:
        for key, val in self.my_envs.items():
            if (val[ENV_ID] == env_id):
                return val.get(ENV_TPH)
        return None
        


# offsets for the list of tuples
IMAGE_NAME="imageName"
IMAGE_ID="id"
IMAGE_MENU_ITEM="menu"

# singleton for Environments
class Images: 
    is_init: bool = False
    my_images: dict

    def __init__(self, image_arg):
         if self.is_init:
            raise ValueError('Images.load() already initialized')
         else:
            self.my_images = image_arg
            self.is_init = True

    @staticmethod
    def load(fs_id: str, env_id: str):
        images = list_images(fs_id, env_id)
        if len(images) == 0:
            return None
        for key, val in images.items():
            val[IMAGE_MENU_ITEM] = f"{val[IMAGE_NAME]}" # shows in menu
        return Images(images)

    def menu_items(self) -> list: 
        menu_list = []
        for key, val in self.my_images.items():
            menu_list.append(val[IMAGE_MENU_ITEM])
        return menu_list

    def name_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_images.items():
            if (val[IMAGE_MENU_ITEM] == menu_item):
                return val.get(IMAGE_NAME)
        return None
        
