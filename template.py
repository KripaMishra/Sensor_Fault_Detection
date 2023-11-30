import os
from pathlib import Path 
import logging

project_name = "sensor"
list_of_files = [ 
    ".github/workflow/.gitkeep",
    f"{project_name}/cloud_storage/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/data_access/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/ml/__init__.py",
    f"{project_name}/__init__.py",
    f"{project_name}/exception.py",
    f"{project_name}/logger.py",
    "main.py",
    "setup.py",
    f"{project_name}/Dockerfile",
    "requirements.txt",
    f"{project_name}/research/trials.ipynb",


]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename= os.path.split(filepath)

    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        
    if(not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath, "w") as f:
            pass 
    
    