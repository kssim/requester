# -*- coding: utf-8 -*-

from scapy.all import (rdpcap, scapy)

from parser import ResponseParser

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
        self.pcap_data = self.read_pcap_file()

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

    def extraction_request(self):
        if self.pcap_data is None:
            return False

        self.pcap_handler()
        self.write_request_data()
        return True

    def prepare_comparison_response(self):
        if self.pcap_data is None:
            return False

        self.pcap_handler()
        self.parse_response_data_in_pcap()
        return True

    def parse_response_data_in_pcap(self):
        for data in self.response_data_raw:
            parser = ResponseParser(data[PAYLOAD])
            parser.run()

            data_tuple = (data[SRC_IP], data[DST_IP],
                          getattr(parser, "start_line", ""),
                          getattr(parser, "headers", {}),
                          getattr(parser, "body", ""))
            self.response_data.append(data_tuple)

    def comparison_response_header(self, first_headers, second_headers):
        first_headers_keys = set(first_headers.keys())
        second_headers_keys = set(second_headers.keys())
        intersection_keys = first_headers_keys.intersection(second_headers_keys)

        if first_headers_keys != intersection_keys or second_headers_keys != intersection_keys:
            return False

        same_value_keys = set(o for o in intersection_keys if first_headers[o] == second_headers[o])
        if intersection_keys != same_value_keys:
            return True if (intersection_keys - same_value_keys) == set(['date']) else False

        return True

    def comparison_response(self, response_data):
        if len(response_data) != len(self.response_data):
            print ("Error : The number of response data does not match.")
            return

        for recived_data, pcap_data in zip(response_data, self.response_data):
            # Response header verification.
            if self.comparison_response_header(recived_data.headers, pcap_data[HEADERS]) is False:
                print ("The value of the response header is different.")

            if pcap_data[BODY].encode("hex") == recived_data.text.encode("utf-8").replace("\r\n", "").encode("hex"):
                print ("The value of the reponse body is same.")
            else:
                print ("The value of the reponse body is different.")

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

    def pcap_handler(self):
        for packet in self.pcap_data:
            ip_layer = packet.getlayer("IP")

            tcp_layer = packet.getlayer("TCP")
            if tcp_layer is None:
                continue

            if packet.getlayer("Raw"):
                if len(self.payload) == 0:
                    self.payload.append((ip_layer.src, ip_layer.dst, str(tcp_layer.payload)))
                    continue

                pre_src = self.payload[len(self.payload) - 1][SRC_IP]
                pre_dst = self.payload[len(self.payload) - 1][DST_IP]

                if pre_src == ip_layer.src and pre_dst == ip_layer.dst:
                    pre_payload = self.payload[len(self.payload) - 1][PAYLOAD]
                    self.payload[len(self.payload) - 1] = (pre_src, pre_dst, pre_payload + str(tcp_layer.payload))
                else:
                    self.payload.append((ip_layer.src, ip_layer.dst, str(tcp_layer.payload)))
        self.seperate_response_and_request()

    def write_request_data(self):
        for idx, data in enumerate(self.request_data):
            payload = data[PAYLOAD]

            file_name = "%s_request_%s" % (self.file_name, idx)
            with open(file_name, "a") as f:
                f.write(payload)

            print ("\"%s\" file has been created." % file_name)
