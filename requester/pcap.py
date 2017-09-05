# -*- coding: utf-8 -*-

"""
This module is responsible for all processing related to the pcap file.
"""

from scapy.all import (rdpcap, scapy)

from parser import ResponseParser
from structures import CaseInsensitiveDict

SRC_IP = 0
DST_IP = 1
PAYLOAD = 2

START_LINE = 2
HEADERS = 3
BODY = 4


class PcapHandler(object):

    __attrs__ = [
        "file_name", "pcap_data", "payload", "request_data", "response_data_raw", "response_data"
    ]

    def __init__(self, file_name):
        self.file_name = file_name
        self.pcap_data = None

        self.payload = []
        self.request_data = []
        self.response_data_raw = []
        self.response_data = []

    def read_pcap_file(self):
        try:
            pcap_data = rdpcap(self.file_name)
        except scapy.error.Scapy_Exception:
            print ("Error : This is not a normal pcap file.")
            return None
        else:
            return pcap_data

    def prepare_process(self):
        self.pcap_data = self.read_pcap_file()
        if self.pcap_data is None:
            return False

        self.get_payload()
        return True

    def parse_response_data_in_pcap(self):
        for data in self.response_data_raw:
            parser = ResponseParser(data[PAYLOAD])
            parser.run()

            data_tuple = (data[SRC_IP], data[DST_IP],
                          getattr(parser, "start_line", []),
                          getattr(parser, "headers", CaseInsensitiveDict()),
                          getattr(parser, "body", ""))
            self.response_data.append(data_tuple)

    def comparison_response_header(self, first_headers, second_headers):
        # Compare the contents of two header values with case-insensitivity.
        first_headers_keys = set([i.lower() for i in first_headers.keys()])
        second_headers_keys = set([i.lower() for i in second_headers.keys()])
        intersection_keys = first_headers_keys.intersection(second_headers_keys)

        if first_headers_keys != intersection_keys or second_headers_keys != intersection_keys:
            return False

        same_value_keys = set(o for o in intersection_keys if first_headers[o] == second_headers[o])
        if intersection_keys == same_value_keys:
            return True

        # The date field is treated as an exception because the data may be different.
        if (intersection_keys - same_value_keys) == set(['date']):
            print ("Info : The value of the date field is different but ignored.")
            return True

        return False

    def comparison_response(self, response_data, verbose=False):
        if len(response_data) != len(self.response_data):
            print ("Error : The number of response data does not match.")
            return False

        for recived_data, pcap_data in zip(response_data, self.response_data):
            # Response header verification.
            if self.comparison_response_header(recived_data[HEADERS], pcap_data[HEADERS]) is False:
                print ("The value of the response header is different.")

            # Response body verification.
            if pcap_data[BODY].encode("hex") == recived_data[BODY].encode("utf-8").replace("\r\n", "").strip().encode("hex"):
                print ("The value of the reponse body is same.")
            else:
                print ("The value of the reponse body is different.")

            if verbose:
                print ("================================== pcap response =================================")
                print (pcap_data[HEADERS])
                print ("")
                print (pcap_data[BODY])
                print ("==================================================================================")

                print ("================================ recieved response ===============================")
                print (recived_data[HEADERS])
                print ("")
                print (recived_data[BODY].encode("utf-8").replace("\r\n", "").strip())
                print ("==================================================================================")

        return True

    def seperate_response_and_request(self):
        for data in self.payload:
            src_ip = data[SRC_IP]
            dst_ip = data[DST_IP]
            payload = data[PAYLOAD].strip()

            # Check request start-line
            if payload[:3] != "GET" and payload[:3] != "POST":
                self.response_data_raw.append((src_ip, dst_ip, payload))
                continue

            self.request_data.append((src_ip, dst_ip, payload))

    def get_payload(self):
        for packet in self.pcap_data:
            ip_layer = packet.getlayer("IP")

            tcp_layer = packet.getlayer("TCP")
            if tcp_layer is None:
                # Do not treat non-tcp.
                continue

            if packet.getlayer("Raw") is None:
                # Do not handle without payload.
                continue

            if len(self.payload) == 0:
                # Before the payload processing, store the source ip and the destination ip.
                self.payload.append((ip_layer.src, ip_layer.dst, str(tcp_layer.payload)))
                continue

            pre_src = self.payload[len(self.payload) - 1][SRC_IP]
            pre_dst = self.payload[len(self.payload) - 1][DST_IP]

            if pre_src != ip_layer.src or pre_dst != ip_layer.dst:
                # Case that was the first session.
                self.payload.append((ip_layer.src, ip_layer.dst, str(tcp_layer.payload)))
                continue

            # Accumulates payloads to the case where there was an existing session.
            pre_payload = self.payload[len(self.payload) - 1][PAYLOAD]
            self.payload[len(self.payload) - 1] = (pre_src, pre_dst, pre_payload + str(tcp_layer.payload))

        # Classify request and response data.
        self.seperate_response_and_request()

    def write_request_data(self):
        for idx, data in enumerate(self.request_data):
            payload = data[PAYLOAD]

            file_name = "%s_request_%s" % (self.file_name, idx)
            with open(file_name, "w") as f:
                f.write(payload)

            print ("\"%s\" file has been created." % file_name)

    def extraction_request(self):
        if self.prepare_process() is False:
            return False

        self.write_request_data()
        return True

    def prepare_comparison_response(self):
        if self.prepare_process() is False:
            return False

        self.parse_response_data_in_pcap()
        return True
