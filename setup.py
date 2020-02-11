from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="doc_tour",
    version="0.1.1",
    author="raynardj",
    author_email="raynard@rasenn.com",
    description="A web UI for detailed python coding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = find_packages(),
    include_package_data=True,
    py_modules=['doctour',],
    scripts = ['doctour/doctour', ],
    package_data={'doctour':['./doctour/app/templates/*','./doctour/app/static/*']},
    install_requires = [
        "flask",
        "flask_appbuilder",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)