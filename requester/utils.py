# -*- coding: utf-8 -*-

"""
This module provides the utilities used by the requester.
"""


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


def make_dumy_body(byte):
    dumy_body = ""

    if byte is None or byte <= 0:
        return dumy_body

    for i in range(byte):
        dumy_body += "\x00"

    return dumy_body


def make_ellipsis(text, max_len=1000):
    if max_len <= 0 or len(text) < max_len:
        return text

    return text[:max_len] + "\n(ellipsised...)"
