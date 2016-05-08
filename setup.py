import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "tdm",
    version = "2.0.0",
    author = "Simon Doppler",
    author_email = "dopsi@member.fsf.org",
    description = ("Display manager-like console program"),
    license = "MIT",
    keywords = "console display manager",
    url = "http://github.com/dopsi/tdm",
    packages=['tdm'],
    data_files=[
        ('share/man/man1', ['data/man/tdm.1']),
        ('share/zsh/site-functions', ['data/completion/_tdmctl']),
        ('share/bash-completion/completions', ['data/completion/tdmctl']),
        ('share/tdm', ['data/scripts/tdminit', 'data/scripts/tdmexit'])
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
