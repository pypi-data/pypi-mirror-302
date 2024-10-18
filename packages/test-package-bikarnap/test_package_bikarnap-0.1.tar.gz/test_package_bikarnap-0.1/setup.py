from setuptools import setup, find_packages

setup(
    name="test_package_bikarnap",
    version="0.1",
    author="Bikarna Pokharel",
    description="A test python package",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
)