#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

pwd = os.path.abspath(os.path.dirname(__file__))

packages = ["requester"]

requires = [
    "requests>=2.4.3",
    "ipaddress>=1.0.18",
    "scapy>=2.3.3"
]

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name = "requester",
    version = "0.5.0",
    description = "Python HTTP/HTTPS Requester.",
    long_description = "",
    author = "kssim",
    author_email = "ksub0912@gmail.com",
    url = "https://github.com/kssim/requester",
    packages = packages,
    packages_data = {},
    package_dir = {},
    include_package_data = True,
    install_requires = requires,
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
