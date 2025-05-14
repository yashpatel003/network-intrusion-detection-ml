from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    '''
    This function reads the requirements from a file and returns them as a list.
    '''
    try:
        with open(file_path, 'r') as file_object:
            requirements = file_object.readlines()
            requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("-e")]
            return requirements
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

setup(
    name="network-intrusion-detection-ml",
    version="0.1.0",
    description="network traffic analysis, intrusion detection, and anomaly detection",
    author="Yash Patel",
    author_email="yashjpatel2003@example.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)