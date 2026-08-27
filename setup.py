from setuptools import find_packages, setup
from typing import List



file_name='requirements.txt'

def get_requirements()->List[str]:
    List_of_requirements:List[str]=[]
    try:
        with open(file_name,'r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if(requirement and requirement!='-e .'  and not requirement.startswith("#")):
                    List_of_requirements.append(requirement)


    except FileNotFoundError():
        print(" Requirements.txt file not found")

    return List_of_requirements







setup(
    name="networksecurity",
    version="0.0.1",
    author="Shahbaz Khan",
    author_email="shahbazkhan211016@gmail.com",
    description="Machine learning based network security project.",
    packages=find_packages(),
    install_requires=get_requirements()
    
)