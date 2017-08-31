# -*- coding: utf-8 -*-

"""
This module parses the request/response header and body.
"""

from os.path import exists
from structures import CaseInsensitiveDict


class ResponseParser(object):

    __attrs__ = [
        "start_line", "headers", "body", "stream"
    ]

    def __init__(self, stream):
        self.start_line = []
        self.headers = CaseInsensitiveDict()

        self.body = ""
        self.stream = stream

    def parse_start_line(self):
        if len(self.start_line) < 3:
            print ("Error : It does not fit the start-line format.")
            return

    def parser(self):
        # HTTP response start-line.
        self.start_line = self.stream.splitlines()[:1][0].split(" ")
        end_header = False

        for line in self.stream.splitlines()[1:]:
            if end_header is False and line == "":
                end_header = True
                continue

            if end_header is False:
                # HTTP response header field.
                key = line.split(":")[0]
                self.headers[key] = line[len(key) + 1:].replace("\n", "").strip()
            else:
                # HTTP response body.
                self.body += line.strip() + "\n"

        self.body = self.body.strip()

    def run(self):
        if self.stream == "":
            print ("Error : Response stream is empty.")
            return

        self.parser()
        self.parse_start_line()


class RequestParser(object):

    __attrs__ = [
        "start_line", "headers", "method", "uri", "version", "body", "stream"
    ]

    def __init__(self, stream=""):
        self.start_line = []
        self.headers = CaseInsensitiveDict()

        self.method = ""
        self.uri = ""
        self.version = ""
        self.body = ""
        self.stream = stream

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

    def parse(self):
        # HTTP request start-line.
        self.start_line = self.stream.splitlines()[:1][0].split(" ")
        end_header = False

        for line in self.stream.splitlines()[1:]:
            if end_header is False and line == "":
                end_header = True
                continue

            if end_header is False:
                # HTTP request header fields.
                key = line.split(":")[0]
                self.headers[key] = line[len(key) + 1:].replace("\n", "").strip()
            else:
                # HTTP request body.
                try:
                    self.body += line.strip().decode("hex")
                except Exception:
                    self.body += line.strip()
                    break

    def run(self):
        if self.stream == "":
            print ("Error : Request stream is empty.")
            return

        self.parse()
        self.parse_start_line()


class RequestFileParser(RequestParser):

    __attrs__ = [
        "file_name"
    ]

    def __init__(self, file_name):
        RequestParser.__init__(self)
        self.file_name = file_name

    def parse(self):
        if exists(str(self.file_name)) is False:
            print ("Error : The request file could not be accessed.")
            return False

        with open(str(self.file_name)) as f:
            # HTTP request start-line.
            self.start_line = f.readline().strip().split(" ")
            end_header = False

            for line in f:
                if end_header is False and (line == "\r\n" or line == "\n"):
                    end_header = True
                    continue

                if end_header is False:
                    # HTTP request header fields.
                    key = line.split(":")[0]
                    self.headers[key] = line[len(key) + 1:].replace("\n", "").strip()
                else:
                    # HTTP request body.
                    try:
                        self.body += line.strip().decode("hex")
                    except Exception:
                        self.body += line.strip()
                        break
        return True

    def run(self):
        if self.file_name == "":
            print ("Error : File name not entered.")
            return False

        if self.parse() is False:
            return False

        RequestParser.parse_start_line(self)
        return True
