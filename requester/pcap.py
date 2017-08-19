# -*- coding: utf-8 -*-

from scapy.all import *

SRC_IP = 0
DST_IP = 1
PAYLOAD = 2

class PcapHandler(object):

    __attrs__ = [
        "file_name", "pcap_data", "payload", "request_data", "response_data"
    ]

    def __init__(self, file_name):
        self.file_name = file_name
        self.pcap_data = rdpcap(self.file_name)

        self.payload = []
        self.request_data = []
        self.response_data = []


    def extraction_request(self):
        self.pcap_handler()
        self.write_request_data()


#    def comparison_response(self):
#        self.pcap_handler()


    def seperate_response_and_request(self):
        for data in self.payload:
            src_ip = data[SRC_IP]
            dst_ip = data[DST_IP]
            payload = data[PAYLOAD].strip()

            # Check request start-line
            if payload[:3] != "GET" and payload[:3] != "POST":
                self.response_data.append((src_ip, dst_ip, payload))
                continue

            self.request_data.append((src_ip, dst_ip, payload))


    def pcap_handler(self):
        for packet in self.pcap_data:
            ip_layer = packet.getlayer("IP")

            tcp_layer = packet.getlayer("TCP")
            if tcp_layer == None:
                continue

            if packet.getlayer("Raw"):
                if len(self.payload) == 0:
                    self.payload.append((ip_layer.src, ip_layer.dst, str(tcp_layer.payload)))
                    continue

                pre_src = self.payload[len(self.payload)-1][SRC_IP]
                pre_dst = self.payload[len(self.payload)-1][DST_IP]

                if pre_src == ip_layer.src and pre_dst == ip_layer.dst:
                    pre_payload = self.payload[len(self.payload)-1][PAYLOAD]
                    self.payload[len(self.payload)-1] = (pre_src, pre_dst, pre_payload + str(tcp_layer.payload))
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
