from setuptools import find_packages,setup
from typing import List


def get_requirements()->List[str]:
    " This Function returns the list of requirements"
    requirement_list:List[str]=[]

    try:
        with open('requirements.txt','r') as file:
            #read lines from the file
            lines=file.readlines()
            #Process the lines
            for line in lines:
                requirement=line.strip()
                # ignoring empty lines and -e .
                if requirement and requirement!='-e .':
                    requirement_list.append(requirement)
    
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_list

print(get_requirements())


setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Shahbaz Khan",
    author_email="shahbazkhan211016@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)



