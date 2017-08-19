#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser

from session import Session
from parser import RequestFileParser
from utils import (make_request_url, get_validate_ip_address)

def process_with_request_file(options):
    session = Session()
    parser = RequestFileParser(options.file)

    session.update_connection_info(method=getattr(parser, "method", "GET"))
    session.update_headers(getattr(parser, "headers", None))
    session.update_body(getattr(parser, "body", ""))

    request_url = make_request_url(options.host, options.port, getattr(parser, "uri", ""))
    session.send(request_url)


def main():
    option = OptionParser("Usage: %prog ")
    option.add_option("--port", dest="port", type="int", help="port name(default 80)")
    option.add_option("--host", dest="host", type="string", help="host name or ip address")
    option.add_option("-f", "--file", dest="file", type="string", help="request file name(include full path)")

    (options, args) = option.parse_args()

    if options.host is None or options.port is None:
        option.print_help()
        exit(1)

    process_with_request_file(options)


if __name__ == "__main__":
    main()
