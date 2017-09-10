# -*- coding: utf-8 -*-

import pytest
import os

from requester.pcap import (PcapHandler, SRC_IP, DST_IP, START_LINE, HEADERS, BODY)


class TestNormalHttpPcapHandler(object):

    pcap_file = "tests/test_files/http.pcapng"
    extract_file_name = "tests/test_files/http.pcapng_request_0"
    client_ip = "192.168.0.4"
    server_ip = "103.22.220.133"
    response_start_line = ["HTTP/1.1", "200", "OK"]
    response_headers = {"content-length": "2989", "content-type": "text/html; charset=utf-8", "date": "Fri, 25 Aug 2017 08:50:17 GMT", "server": "lighttpd/1.4.28"}
    response_body = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<title>Index of /</title>
<style type="text/css">
a, a:active {text-decoration: none; color: blue;}
a:visited {color: #48468F;}
a:hover, a:focus {text-decoration: underline; color: red;}
body {background-color: #F5F5F5;}
h2 {margin-bottom: 12px;}
table {margin-left: 12px;}
th, td { font: 90% monospace; text-align: left;}
th { font-weight: bold; padding-right: 14px; padding-bottom: 3px;}
td {padding-right: 14px;}
td.s, th.s {text-align: right;}
div.list { background-color: white; border-top: 1px solid #646464; border-bottom: 1px solid #646464; padding-top: 10px; padding-bottom: 14px;}
div.foot { font: 90% monospace; color: #787878; padding-top: 4px;}
</style>
</head>
<body>
<h2>Index of /</h2>
<div class="list">
<table summary="Directory Listing" cellpadding="0" cellspacing="0">
<thead><tr><th class="n">Name</th><th class="m">Last Modified</th><th class="s">Size</th><th class="t">Type</th></tr></thead>
<tbody>
<tr><td class="n"><a href="../">Parent Directory</a>/</td><td class="m">&nbsp;</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="debian/">debian</a>/</td><td class="m">2017-Aug-25 15:57:49</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="debian-archive/">debian-archive</a>/</td><td class="m">2017-Feb-24 18:31:43</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="debian-backports/">debian-backports</a>/</td><td class="m">2016-May-13 22:09:11</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="debian-cd/">debian-cd</a>/</td><td class="m">2017-Aug-23 09:30:16</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="debian-multimedia/">debian-multimedia</a>/</td><td class="m">2017-Feb-01 09:52:10</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="debian-ports/">debian-ports</a>/</td><td class="m">2017-Aug-25 09:45:39</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="debian-security/">debian-security</a>/</td><td class="m">2017-Aug-24 10:33:39</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="debian-volatile/">debian-volatile</a>/</td><td class="m">2012-Feb-23 10:36:44</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="HEADER.html">HEADER.html</a></td><td class="m">2008-May-19 02:14:19</td><td class="s">0.2K</td><td class="t">text/html</td></tr>
<tr><td class="n"><a href="robots.txt">robots.txt</a></td><td class="m">2011-Jul-24 18:39:41</td><td class="s">0.1K</td><td class="t">text/plain</td></tr>
</tbody>
</table>
</div>
<div class="foot">lighttpd/1.4.28</div>
</body>
</html>"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.pcap_handler = PcapHandler(self.pcap_file)

    def tear_down(self):
        try:
            os.remove(self.extract_file_name)
        except OSError, e:
            print ("Error : %s is not removed.\n%s" % (self.temporary_request_file, e))

    def test_read_pcap_file(self):
        assert self.pcap_handler.read_pcap_file() is not None

    def test_prepare_process(self):
        assert self.pcap_handler.payload == []
        assert self.pcap_handler.response_data_raw == []
        assert self.pcap_handler.request_data == []

        assert self.pcap_handler.prepare_process() is True

        assert self.pcap_handler.payload != []
        assert self.pcap_handler.response_data_raw != []
        assert self.pcap_handler.request_data != []
        assert len(self.pcap_handler.payload) == 2
        assert len(self.pcap_handler.response_data_raw) == 1
        assert len(self.pcap_handler.request_data) == 1

        assert self.pcap_handler.request_data[0][SRC_IP] == self.client_ip
        assert self.pcap_handler.request_data[0][DST_IP] == self.server_ip
        assert self.pcap_handler.response_data_raw[0][SRC_IP] == self.server_ip
        assert self.pcap_handler.response_data_raw[0][DST_IP] == self.client_ip

    def test_parse_response_data_in_pcap(self):
        assert self.pcap_handler.response_data == []

        self.pcap_handler.prepare_process()
        self.pcap_handler.parse_response_data_in_pcap()

        assert self.pcap_handler.response_data != []
        assert len(self.pcap_handler.response_data) == 1

        data_tuple = self.pcap_handler.response_data[0]
        assert data_tuple[SRC_IP] == self.server_ip
        assert data_tuple[DST_IP] == self.client_ip
        assert data_tuple[START_LINE] == self.response_start_line
        assert data_tuple[HEADERS] == self.response_headers
        assert data_tuple[BODY] == self.response_body

    def test_comparison_response_header(self):
        assert self.pcap_handler.comparison_response_header(self.response_headers, self.response_headers) is True

    def test_comparison_response(self):
        self.pcap_handler.prepare_process()
        self.pcap_handler.parse_response_data_in_pcap()

        response_data = [(self.server_ip, self.client_ip, self.response_start_line, self.response_headers, self.response_body)]
        assert self.pcap_handler.comparison_response(response_data)

    def test_request_data(self):
        self.pcap_handler.prepare_process()

        assert os.path.isfile(self.extract_file_name) is False
        self.pcap_handler.write_request_data()
        assert os.path.isfile(self.extract_file_name) is True

        self.tear_down()

    def test_extraction_request(self):
        assert self.pcap_handler.extraction_request() is True

        self.tear_down()

    def test_prepare_comparison_response(self):
        assert self.pcap_handler.prepare_comparison_response() is True

