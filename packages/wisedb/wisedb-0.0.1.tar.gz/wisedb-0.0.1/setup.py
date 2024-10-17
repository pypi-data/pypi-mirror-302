from setuptools import find_packages, setup

# Setup
setup(
    name="wisedb",
    version="0.0.1",
    description="Wisedb",
    author="MF",
    packages=find_packages(include=["wisedb", "wisedb.*"]),
)
