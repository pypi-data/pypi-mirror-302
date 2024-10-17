from setuptools import find_packages, setup

# Setup
setup(
    name="wiselink",
    version="0.0.1",
    description="Wiselink",
    author="MF",
    packages=find_packages(include=["wiselink", "wiselink.*"]),
)
