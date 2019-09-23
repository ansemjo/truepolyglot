#!/usr/bin/env python

from os import environ
from subprocess import check_output as cmd
from setuptools import setup, find_packages

# package metadata
name = "truepolyglot"
environ['REVISION_SEPERATOR'] = '.post'
version = cmd(['sh', './version.sh','version']).strip().decode()
author = "ben"
email = "truepolyglot@hackade.org"
git = "https://git.hackade.org/%s.git" % name

setup(
    name=name,
    version=version,
    author=author,
    author_email=email,
    url=git,
    scripts=[name, "pdfzip"],
    packages=find_packages(),
    python_requires='>3',
    install_requires=["pypdf2 >= 1.26.0"],
)
