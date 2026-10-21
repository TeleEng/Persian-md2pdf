#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="persian-md2pdf",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "markdown>=3.5",
    ],
    entry_points={
        "console_scripts": [
            "persian-md2pdf=persian_md2pdf.cli:main",
        ],
    },
)
