# -*- coding: utf-8 -*-

"""
This module is the front-end processing module for user input.
"""

from optparse import OptionParser

from session import Session
from pcap import (PcapHandler, SRC_IP, DST_IP, PAYLOAD)
from parser import (RequestParser, RequestFileParser)
from utils import (make_request_url, make_host, make_dumy_body)
from structures import CaseInsensitiveDict


def process_with_request_file(options):
    session = Session()

    if options.file is None:
        method = "GET"
        headers = None
        body = ""
        uri = ""
    else:
        parser = RequestFileParser(options.file)
        if parser.run() is False:
            return 1

        method = getattr(parser, "method", "GET")
        headers = getattr(parser, "headers", CaseInsensitiveDict())
        body = getattr(parser, "body", "")
        uri = getattr(parser, "uri", "")

    # If dumy_body_byte is present, add dumy data.
    body += make_dumy_body(options.dumy_body_byte)

    session.update_connection_info(method=method)
    session.update_headers(headers)
    session.update_body(body)

    request_url = make_request_url(options.host, options.port, uri)
    session.send(request_url, verbose_detail=options.verbose)
    return 0


def process_with_pcap_file(options):
    pcap = PcapHandler(options.pcap)
    ret = pcap.prepare_comparison_response()
    if ret is False:
        return 1

    response_data = []
    for stream in getattr(pcap, "request_data", []):
        parser = RequestParser(stream[PAYLOAD])
        if parser.run() is False:
            return 1

        session = Session()
        session.update_connection_info(method=getattr(parser, "method", "GET"))
        headers = getattr(parser, "headers", CaseInsensitiveDict())
        session.update_headers(headers)
        session.update_body(getattr(parser, "body", ""))

        host = make_host(headers, stream[DST_IP])
        request_url = make_request_url(host, 80, getattr(parser, "uri", ""))
        if session.send(request_url, verbose=False) is False:
            continue

        response = getattr(session, "response", None)
        start_line = ["HTTP/1.1", response.status_code]
        start_line += response.reason.split(" ")
        response_data.append((stream[DST_IP], stream[SRC_IP], start_line, response.headers, response.text))

    pcap.comparison_response(response_data, options.verbose)
    return 0


def main():
    option = OptionParser("Usage: %prog ")
    option.add_option("--port", dest="port", type="int", help="port name(default 80)")
    option.add_option("--host", dest="host", type="string", help="host name or ip address")
    option.add_option("-f", "--file", dest="file", type="string", help="request file name(include full path)")
    option.add_option("--pcap", dest="pcap", type="string", help="packet dump file name(include full path)")
    option.add_option("-e", "--extraction", dest="extra_mode", action="store_true", help="Extract http request from packet dump file.")
    option.add_option("-c", "--check", dest="check_mode", action="store_true", help="Send an http request in the packet dump and compare the response.")
    option.add_option("--dumy-body", dest="dumy_body_byte", type="int", help="Dummy data is added to request body for the set number of bytes.")
    option.add_option("--verbose", dest="verbose", action="store_true", help="Show all related information without omissions.")

    (options, _) = option.parse_args()

    # Misuse.
    if options.pcap and options.dumy_body_byte:
        print ("The two options are mutually exclusive.")
        return 1

    # Request extraction mode in packet dump.
    if options.extra_mode and options.pcap:
        pcap = PcapHandler(options.pcap)
        ret = pcap.extraction_request()
        return 0 if ret is True else 1

    # Request extraction and response comparison mode in packetdump.
    if options.check_mode and options.pcap:
        return process_with_pcap_file(options)

    # Basic request transfer mode.
    if (options.host and options.port)                                      \
            and (options.extra_mode is None and options.check_mode is None) \
            and (options.pcap is None):
        return process_with_request_file(options)

    # Misuse.
    option.print_help()
    return 1


if __name__ == "__main__":
    exit(main())
