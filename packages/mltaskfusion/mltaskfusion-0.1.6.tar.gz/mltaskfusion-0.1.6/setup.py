#!/usr/bin/env python

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

with open("requirements.txt", encoding="utf-8") as f:
    requireds = f.read().splitlines()

setup(
    name="mltaskfusion",
    version="0.1.6",
    long_description=open("README.md", encoding="utf-8").read().strip(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["mltaskfusion", "mltaskfusion.*"]),
    install_requires=requireds,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={"console_scripts": ["mltaskfusion-cli=mltaskfusion.cmd.cli:main"]},
)
