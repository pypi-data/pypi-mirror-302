from setuptools import find_packages, setup

# Setup
setup(
    name="wiseutil",
    version="0.0.1",
    description="Wiseutil",
    author="MF",
    packages=find_packages(include=["wiseutil", "wiseutil.*"]),
)
