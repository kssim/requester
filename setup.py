#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

packages = ["requester"]

requires = [
    "requests>=2.4.3",
    "scapy>=2.3.3",
    "pytest>=3.2.1",
    "pytest-cov>=2.5.1",
    "urllib3>=1.22"
]

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name = "requester",
    version = "0.6.1",
    description = "Python HTTP/HTTPS Requester.",
    long_description = readme,
    author = "kssim",
    author_email = "ksub0912@gmail.com",
    url = "https://github.com/kssim/requester",
    packages = packages,
    packages_data = {},
    package_dir = {},
    include_package_data = True,
    install_requires = requires,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    license = "MIT",
    zip_safe = False,
    scripts = ["bin/requester"],
    classifiers = (
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Testing"
    ),
)
