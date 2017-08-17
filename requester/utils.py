# -*- coding: utf-8 -*-

import socket
import ipaddress

def make_request_url(host, uri):
    request_url = "http://%s%s" % (host, uri)
    return request_url


def convert_hostname_to_ip(host_name):
    try:
        result = socket.getaddrinfo(host_name, 0, 0, 0, socket.IPPROTO_TCP)
    except socket.gaierror:
        print ("Error : The host name is not valid.")
        return None
    else:
        # result example : (2, 1, 6, '', ('192.168.40.245', 80))
        if len(result) < 1 or len(result[0]) < 5 or len(result[0][4]) < 2:
            return None

        return result[0][4][0]


def get_validate_ip_address(host):
    ip = convert_hostname_to_ip(host)

    try:
        ipaddress.ip_address(unicode(ip))
    except ValueError:
        print ("Error : The ip address is not valid.")
        return None

    return ip
