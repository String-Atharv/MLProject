## this is used to create the package and upload to pypi
from setuptools import setup,find_packages
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    this function will return the list of requirements
    '''
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [
            req.strip()                        # remove \n and whitespace
            for req in requirements
            if req.strip() and not req.startswith('-e')  # drop empty lines & editable installs
        ]
    return requirements

setup(
    name='ml project',
    author='Atharv',
    author_email='shivaleatharv@gmail.com',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)