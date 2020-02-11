from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="doc_tour",
    version="0.1.4",
    author="raynardj",
    author_email="raynard@rasenn.com",
    description="A web UI for detailed python coding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = find_packages(),
    include_package_data=True,
    py_modules=['doctour',],
    scripts = ['doctour/doctour', ],
    package_data={'doctour':['app/templates/*',
                            'app/static/appbuilder/*/*',
                            'app/static/appbuilder/*/*/*',
                            'app/static/templates/*',
                            'app/static/js/*', 
                            'app/static/js/*/*',
                            'app/static/js/*/*/*',
                            ]},
    install_requires = [
        "flask",
        "flask_appbuilder==2.2.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)