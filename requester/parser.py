# -*- coding: utf-8 -*-

class RequestFileParser(object):

    __attrs__ = [
        "file_name", "start_line", "headers", "method", "uri", "version", "body"
    ]

    def __init__(self, file_name):
        if file_name is None:
            return

        self.file_name = file_name

        self.start_line = []
        self.headers = {}

        self.body = ""
        self.method = ""
        self.uri = ""
        self.version = ""

        self.parse()
        self.parse_start_line()


    def parse(self):
        with open(str(self.file_name)) as f:
            # HTTP request start-line.
            self.start_line = f.readline().split(" ")
            end_header = False

            for line in f:
                if end_header == False and (line == "\r\n" or line == "\n"):
                    end_header = True
                    continue

                if end_header == False:
                    # HTTP request header fields.
                    key = line.split(":")[0]
                    self.headers[key] = line[len(key)+1:].replace("\n", "").strip()
                else:
                    # HTTP request body (Only hex values can be input.)
                    try:
                        self.body += line.strip().decode("hex")
                    except:
                        print ("Error : The request body only supports hex values.")
                        self.body = ""
                        break


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
