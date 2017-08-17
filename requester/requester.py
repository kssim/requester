#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser

from session import Session
from parser import RequestFileParser
from utils import (make_request_url, get_validate_ip_address)

def process_with_request_file(options):
    session = Session()
    parser = RequestFileParser(options.file)

    session.update_connection_info(method=getattr(parser, "method", ""))
    session.update_headers(getattr(parser, "headers", {}))

    ip = get_validate_ip_address(options.host)
    if ip is None:
        return False

    request_url = make_request_url(ip, getattr(parser, "uri", ""))
    session.send(request_url)


def main():
    parser = OptionParser("Usage: %prog ")
    parser.add_option("--port", dest="port", type="int", help="port name(default 80)")
    parser.add_option("--host", dest="host", type="string", help="host name or ip address")
    parser.add_option("-f", "--file", dest="file", type="string", help="request file name(include full path)")

    (options, args) = parser.parse_args()

    if options.port is None or options.host is None:
        parser.print_help()
        exit(1)

    if options.file is None:
        print ("Error : Not implement.")
        exit(1)

    process_with_request_file(options)


if __name__ == "__main__":
    main()
