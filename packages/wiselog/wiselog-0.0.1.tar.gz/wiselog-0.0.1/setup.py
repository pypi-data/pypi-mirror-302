from setuptools import find_packages, setup

# Setup
setup(
    name="wiselog",
    version="0.0.1",
    description="Wiselog",
    author="MF",
    packages=find_packages(include=["wiselog", "wiselog.*"]),
)
