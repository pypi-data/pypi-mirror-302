#!/usr/bin/env python

import os
from typing import Iterator

from setuptools import find_packages, setup


def read(*file_path_parts):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    fp = os.path.join(this_dir, *file_path_parts)
    with open(fp) as f:
        return f.read()


def get_requirements() -> Iterator[str]:
    for line in read("requirements.txt").splitlines():
        line = line.strip()
        if line and not line.startswith("--") and not line.startswith("#"):
            yield line


long_description = read("README.md")

setup(
    name="younameit",
    use_scm_version={
        "write_to": "younameit/__version__.py",
    },
    setup_requires=["setuptools-scm"],
    author="Michał Kaczmarczyk",
    author_email="michal.s.kaczmarczyk@gmail.com",
    maintainer="Michał Kaczmarczyk",
    maintainer_email="michal.s.kaczmarczyk@gmail.com",
    license="Custom MIT license",
    url="https://gitlab.com/kamichal/younameit",
    description="Pseudo random word generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    package_data={"younameit": ["books/*.yaml"]},
    requires=[],
    install_requires=list(get_requirements()),
    keywords="random word generator hash translator naming labeler",
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python",
        "Topic :: Database :: Front-Ends",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": ["younameit = younameit.__main__:cli_main"],
    },
)
