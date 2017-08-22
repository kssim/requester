# -*- coding: utf-8 -*-


class ResponseParser(object):

    __attrs__ = [
        "start_line", "headers", "body", "stream"
    ]

    def __init__(self, stream):
        self.start_line = []
        self.headers = {}

        self.body = ""
        self.stream = stream


    def run(self):
        if self.stream == "":
            print ("Error : Response stream is empty.")
            return

        self.parser()
        self.parser_start_line()


    def parser_start_line(self):
        if len(self.start_line) < 3:
            print ("Error : It does not fit the start-line format.")
            return


    def parser(self):
        self.start_line = self.stream.splitlines()[:1][0].split(" ")
        end_header = False

        for line in self.stream.splitlines()[1:]:
            if end_header == False and line == "":
                end_header = True
                continue

            if end_header == False:
                key = line.split(":")[0].lower()
                self.headers[key] = line[len(key)+1:].replace("\n", "").strip()
            else:
                self.body += line.strip() + "\n"

        self.body = self.body.strip()


class RequestParser(object):

    __attrs__ = [
        "start_line", "headers", "method", "uri", "version", "body", "stream"
    ]

    def __init__(self, stream=""):
        self.start_line = []
        self.headers = {}

        self.method = ""
        self.uri = ""
        self.version = ""
        self.body = ""
        self.stream = stream


    def run(self):
        if self.stream == "":
            print ("Error : Request stream is empty.")
            return

        self.parse()
        self.parse_start_line()


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
        self.start_line = self.stream.splitlines()[:1][0].split(" ")
        end_header = False

        for line in self.stream.splitlines()[1:]:
            if end_header == False and line == "":
                end_header = True
                continue

            if end_header == False:
                # HTTP request header fields.
                key = line.split(":")[0].lower()
                self.headers[key] = line[len(key)+1:].replace("\n", "").strip()
            else:
                # HTTP request body (Only hex values can be input.)
                try:
                    self.body += line.strip().decode("hex")
                except:
                    print ("Error : The request body only supports hex values.")
                    self.body = ""
                    break


class RequestFileParser(RequestParser):

    __attrs__ = [
        "file_name"
    ]

    def __init__(self, file_name):
        RequestParser.__init__(self)
        self.file_name = file_name


    def run(self):
        if self.file_name == "":
            print ("Error : File name not entered.")
            return

        self.parse()
        RequestParser.parse_start_line(self)


    def parse(self):
        with open(str(self.file_name)) as f:
            # HTTP request start-line.
            self.start_line = f.readline().strip().split(" ")
            end_header = False

            for line in f:
                if end_header == False and (line == "\r\n" or line == "\n"):
                    end_header = True
                    continue

                if end_header == False:
                    # HTTP request header fields.
                    key = line.split(":")[0].lower()
                    self.headers[key] = line[len(key)+1:].replace("\n", "").strip()
                else:
                    # HTTP request body (Only hex values can be input.)
                    try:
                        self.body += line.strip().decode("hex")
                    except:
                        print ("Error : The request body only supports hex values.")
                        self.body = ""
                        break
