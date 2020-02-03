from setuptools import setup
from setuptools import find_packages

setup(
    name="doctour",
    version="0.1.0",
    author="raynardj",
    author_email="raynard@rasenn.com",
    description="A web UI for detailed python coding",
    packages = find_packages(),
    include_package_data=True,
    py_modules=['doctour',],
    scripts = ['doctour/doctour', ],
    package_data={'doctour':['./doctour/templates/*','./doctour/static/*']},
    install_requires = [
        "flask",
        "flask_appbuilder",
    ],
)