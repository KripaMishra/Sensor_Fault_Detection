from setuptools import find_packages, setup
from typing import List

#variables

PROJECT_NAME = "Sensor Fault Detetection"
AUTHOR_NAME = "Kripa Mishra"
AURTHOR_EMAIL = "kripa5661@gmail.com"
VERSION = "0.0.1"


HYPEN_E_DOT= '-e .'


def get_packages()->List[str]:
    '''
    This function takes the requirements.txt and returns a list of strings, which will later be used to install all the requied packages
    '''

    requirements:List[str] =[]
    
    file_path = 'requirements.txt'

    with open(file_path, 'r') as file_obj:
        requirements= file_obj.readlines()
        requirements= [req.replace("/n", "") for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements


setup(
    name=PROJECT_NAME,
    version= VERSION,
    author=AUTHOR_NAME,
    author_email=AURTHOR_EMAIL,
    packages= find_packages(),
    install_requires= get_packages(),
    
)
    
