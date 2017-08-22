# -*- coding: utf-8 -*-

import socket
import ipaddress

def make_host(headers, dst_ip):
    if "Host" in headers:
        return headers["Host"]
    elif "host" in headers:
        return headers["host"]
    else:
        return dst_ip


def make_request_url(host, port, uri):
    if "http://" in host or "https://" in host:
        return "%s%s" % (host, uri)

    if port == 443:
        return "https://%s%s" % (host, uri)

    return "http://%s%s" % (host, uri)
