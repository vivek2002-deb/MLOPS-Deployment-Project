from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-Project",
    version="0.1.0",
    author="Vivek Raj",
    packages=find_packages(),
    install_requires=requirements,
)