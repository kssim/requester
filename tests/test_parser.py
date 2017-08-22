# -*- coding: utf-8 -*-

import pytest

from requester.parser import (
    ResponseParser, RequestParser, RequestFileParser
)


class TestResponseParserWithoutStream(object):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.response_parser = ResponseParser("")

    def test_run(self):
        self.response_parser.run()

        assert getattr(self.response_parser, "start_line") == []
        assert getattr(self.response_parser, "headers") == {}
        assert getattr(self.response_parser, "body") == ""
        assert getattr(self.response_parser, "stream") == ""


class TestResponseParserWithValidStream(object):

    valid_response_stream = (b"HTTP/1.1 200 OK\r\n"
                             b"Date: Tue, 22 Aug 2017 07:57:39 GMT\r\n"
                             b"Server: Apache/2.2.22 (Debian)\r\n"
                             b"Vary: Accept-Encoding\r\n"
                             b"Content-Length: 54\r\n"
                             b"Content-Type: text/html; charset=UTF-8\r\n"
                             b"\r\n"
                             b"<html><head></head><body>Hello World~!!!</body></html>")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.response_parser = ResponseParser(self.valid_response_stream)

    def test_run(self):
        self.response_parser.run()

        start_line = ["HTTP/1.1", "200", "OK"]
        headers = {
            "date" : "Tue, 22 Aug 2017 07:57:39 GMT",
            "server" : "Apache/2.2.22 (Debian)",
            "vary" : "Accept-Encoding",
            "content-length" : "54",
            "content-type" : "text/html; charset=UTF-8"
        }
        body = "<html><head></head><body>Hello World~!!!</body></html>"

        assert getattr(self.response_parser, "start_line") == start_line
        assert getattr(self.response_parser, "headers") == headers
        assert getattr(self.response_parser, "body") == body
        assert getattr(self.response_parser, "stream") == self.valid_response_stream


class TestResponseParserWithInValidStream(object):

    valid_response_stream = (b"HTTP/1.1 404 Not Found\r\n"
                             b"Date: Tue, 22 Aug 2017 07:57:39 GMT\r\n"
                             b"Server: Apache/2.2.22 (Debian)\r\n"
                             b"Vary: Accept-Encoding\r\n"
                             b"Content-Type: text/html; charset=UTF-8"
                             b"<html><head></head><body>Hello World~!!!</body></html>")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.response_parser = ResponseParser(self.valid_response_stream)

    def test_run(self):
        self.response_parser.run()

        start_line = ["HTTP/1.1", "404", "NOT"]
        headers = {
            "date" : "Tue, 22 Aug 2017 09:37:39 GMT",
            "Server" : "Apache/2.2.22 (Debian)",
            "Vary" : "Accept-Encoding",
            "content-length" : "54",
            "Content-Type" : "text/html; charset=UTF-8"
        }
        body = "<html><head></head><body>Hello World~!!!\r\n</body></html>"

        assert getattr(self.response_parser, "start_line") != start_line
        assert getattr(self.response_parser, "headers") != headers
        assert getattr(self.response_parser, "body") != body
        assert getattr(self.response_parser, "stream") == self.valid_response_stream
