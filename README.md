# Requester

[![PyPI version](https://badge.fury.io/py/requester.svg)](https://github.com/kssim/requester)
[![Build Status](https://travis-ci.org/kssim/requester.svg?branch=master)](https://github.com/kssim/requester)
[![codecov](https://codecov.io/gh/kssim/requester/branch/master/graph/badge.svg)](https://github.com/kssim/requester)
[![Code Health](https://landscape.io/github/kssim/requester/master/landscape.svg?style=flat)](https://github.com/kssim/requester)
[![Python](https://img.shields.io/badge/python-2.7-brightgreen.svg?style=flat)](https://github.com/kssim/requester)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/kssim/requester)

Requester is a python based HTTP / HTTPS request simulator.  
Basically, you create a request statement, send the request as it is, and check the response.  
In addition, it extracts the request from the pcap file, or sends the extracted request and compares the response with the response of the pcap file.  


# Installation
To install Requester, simply:
```bash
$ pip install requester
```


# Usage
* Basic Argument Description

```bash
$ requester
Usage: requester

Options:
  -h, --help            show this help message and exit
  --port=PORT           port name(default 80)
  --host=HOST           host name or ip address
  -f FILE, --file=FILE  request file name(include full path)
  --pcap=PCAP           packet dump file name(include full path)
  -e, --extraction      Extract http request from packet dump file.
  -c, --check           Send an http request in the packet dump and compare
                        the response.
```


* Simple Usage without request file.

```bash
$ requester --host [website] --port [port]
```


* Simple usage with request file.

```bash
$ requester --host [website] --port [port] --file [request file full path]
```


* Extract request file from packet dump.

```bash
$ requester -e --pcap [pcap file full path]
```


* Sends the contents extracted from the request file in the packet dump and compares the response.

```bash
$ requester -c --pcap [pcap file full path]
```


# Documentation
I'll be writing soon.



# Contribute
If you have an idea or issue, feel free to open an issue or make pull request.  
I'll create and share a structured process to contribute soon.
