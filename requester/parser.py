# -*- coding: utf-8 -*-

class RequestFileParser(object):

    __attrs__ = [
        'file_name', 'start_line', 'headers', 'method', 'uri', 'version'
    ]

    def __init__(self, file_name):
        self.file_name = file_name

        self.start_line = []
        self.headers = {}

        self.method = ""
        self.uri = ""
        self.version = ""

        self.parse()
        self.parse_start_line()


    def parse(self):
        with open(str(self.file_name)) as f:
            for line in f:
                if isinstance(line, unicode):
                    line = line.encode("utf-8")

                # HTTP request start-line.
                if ":" not in line:
                    self.start_line = line.split(" ")
                    continue

                # HTTP header fields.
                header = line.split(":")
                self.headers[header[0]] = header[1].replace('\n', '').strip()


    def parse_start_line(self):
        if len(self.start_line) != 3:
            print ("Error : It does not fit the start-line format.")
            return

        self.method = self.start_line[0]
        self.uri = self.start_line[1]
        self.version = self.start_line[2]

        if "HTTP/1.0" in self.version:
            print ("Error : This program does not cover the HTTP/1.0 version.")
            return
