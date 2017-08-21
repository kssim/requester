#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser

from session import Session
from pcap import (PcapHandler, DST_IP, PAYLOAD)
from parser import (RequestParser, RequestFileParser)
from utils import (make_request_url, make_host)

def process_with_request_file(options):
    session = Session()
    parser = RequestFileParser(options.file)
    parser.run()

    session.update_connection_info(method=getattr(parser, "method", "GET"))
    session.update_headers(getattr(parser, "headers", None))
    session.update_body(getattr(parser, "body", ""))

    request_url = make_request_url(options.host, options.port, getattr(parser, "uri", ""))
    session.send(request_url)


def process_with_pcap_file(options):
    pcap = PcapHandler(options.pcap)
    ret = pcap.prepare_comparison_response()
    if ret == False:
        return 1

    response_data = []
    for stream in getattr(pcap, "request_data", []):
        parser = RequestParser(stream[PAYLOAD])
        parser.run()

        session = Session()
        session.update_connection_info(method=getattr(parser, "method", "GET"))
        headers = getattr(parser, "headers", None)
        session.update_headers(headers)
        session.update_body(getattr(parser, "body", ""))

        host = make_host(headers, stream[DST_IP])
        request_url = make_request_url(host, 80, getattr(parser, "uri", ""))
        session.send(request_url, verbose=False)

        response_data.append(getattr(session, "response", None))

    pcap.comparison_response(response_data)
    return 0


def main():
    option = OptionParser("Usage: %prog ")
    option.add_option("--port", dest="port", type="int", help="port name(default 80)")
    option.add_option("--host", dest="host", type="string", help="host name or ip address")
    option.add_option("-f", "--file", dest="file", type="string", help="request file name(include full path)")
    option.add_option("--pcap", dest="pcap", type="string", help="packet dump file name(include full path)")
    option.add_option("-e", "--extraction", dest="extra_mode", action="store_true", help="Extract http request from packet dump file.")
    option.add_option("-c", "--check", dest="check_mode", action="store_true", help="Send an http request in the packet dump and compare the response.")

    (options, args) = option.parse_args()

    # Request extraction mode in packet dump.
    if options.extra_mode and options.pcap:
        pcap = PcapHandler(options.pcap)
        ret = pcap.extraction_request()
        return 0 if ret == True else 1


    # Request extraction and response comparison mode in packetdump.
    if options.check_mode and options.pcap:
        return process_with_pcap_file(options)


    # Basic request transfer mode.
    if (options.host and options.port)                                  \
        and (options.extra_mode is None and options.check_mode is None) \
        and (options.pcap is None):
        process_with_request_file(options)
        return 0


    # Misuse.
    option.print_help()
    return 1


if __name__ == "__main__":
    exit(main())
