import importlib.metadata
import sys
import os

def get_version():
    version = importlib.metadata.version('robbie')
    return version

def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def get_default_workspace_dir():
    cwd = os.getcwd()
    return cwd

# Sentinel object for undefined
undefined = object()
