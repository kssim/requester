# -*- coding: utf-8 -*-

import pytest
import os

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

    invalid_response_stream = (b"HTTP/1.1 404 Not Found\r\n"
                             b"Date: Tue, 22 Aug 2017 07:57:39 GMT\r\n"
                             b"Server: Apache/2.2.22 (Debian)\r\n"
                             b"Vary: Accept-Encoding\r\n"
                             b"Content-Type: text/html; charset=UTF-8"
                             b"<html><head></head><body>Hello World~!!!</body></html>")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.response_parser = ResponseParser(self.invalid_response_stream)

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
        assert getattr(self.response_parser, "stream") == self.invalid_response_stream


class TestRequestParserWithoutRequest(object):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.request_parser = RequestParser()

    def test_run(self):
        self.request_parser.run()

        assert getattr(self.request_parser, "start_line") == []
        assert getattr(self.request_parser, "headers") == {}
        assert getattr(self.request_parser, "method") == ""
        assert getattr(self.request_parser, "uri") == ""
        assert getattr(self.request_parser, "version") == ""
        assert getattr(self.request_parser, "body") == ""
        assert getattr(self.request_parser, "stream") == ""


class TestRequestParserWithValidGetRequestAndNoBody(object):

    valid_request_stream = (b"GET / HTTP/1.1\r\n"
                            b"Host: 8.8.8.8\r\n"
                            b"Connection: keep-alive\r\n"
                            b"Cache-Control: max-age=0\r\n"
                            b"Upgrade-Insecure-Requests: 1\r\n"
                            b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                            b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                            b"Accept-Encoding: gzip, deflate\r\n"
                            b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.request_parser = RequestParser(self.valid_request_stream)

    def test_run(self):
        self.request_parser.run()

        start_line = ["GET", "/", "HTTP/1.1"]
        headers = {
            "host" : "8.8.8.8",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "GET"
        uri = "/"
        version = "HTTP/1.1"
        body = ""

        assert getattr(self.request_parser, "start_line") == start_line
        assert getattr(self.request_parser, "headers") == headers
        assert getattr(self.request_parser, "method") == method
        assert getattr(self.request_parser, "uri") == uri
        assert getattr(self.request_parser, "version") == version
        assert getattr(self.request_parser, "body") == body
        assert getattr(self.request_parser, "stream") == self.valid_request_stream


class TestRequestParserWithValidGetRequestHttp1_0(object):

    valid_request_stream = (b"GET / HTTP/1.0\r\n"
                            b"Host: 8.8.8.8\r\n"
                            b"Connection: keep-alive\r\n"
                            b"Cache-Control: max-age=0\r\n"
                            b"Upgrade-Insecure-Requests: 1\r\n"
                            b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                            b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                            b"Accept-Encoding: gzip, deflate\r\n"
                            b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.request_parser = RequestParser(self.valid_request_stream)

    def test_run(self):
        self.request_parser.run()

        start_line = ["GET", "/", "HTTP/1.0"]
        headers = {
            "host" : "8.8.8.8",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "GET"
        uri = "/"
        version = "HTTP/1.0"
        body = ""

        assert getattr(self.request_parser, "start_line") == start_line
        assert getattr(self.request_parser, "headers") == headers
        assert getattr(self.request_parser, "method") == method
        assert getattr(self.request_parser, "uri") == uri
        assert getattr(self.request_parser, "version") == version
        assert getattr(self.request_parser, "body") == body
        assert getattr(self.request_parser, "stream") == self.valid_request_stream


class TestRequestParserWithValidPostRequestAndNoBody(object):

    valid_request_stream = (b"POST /login HTTP/1.1\r\n"
                            b"Host: 8.8.8.8\r\n"
                            b"Connection: keep-alive\r\n"
                            b"Cache-Control: max-age=0\r\n"
                            b"Upgrade-Insecure-Requests: 1\r\n"
                            b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                            b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                            b"Accept-Encoding: gzip, deflate\r\n"
                            b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.request_parser = RequestParser(self.valid_request_stream)

    def test_run(self):
        self.request_parser.run()

        start_line = ["POST", "/login", "HTTP/1.1"]
        headers = {
            "host" : "8.8.8.8",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "POST"
        uri = "/login"
        version = "HTTP/1.1"
        body = ""

        assert getattr(self.request_parser, "start_line") == start_line
        assert getattr(self.request_parser, "headers") == headers
        assert getattr(self.request_parser, "method") == method
        assert getattr(self.request_parser, "uri") == uri
        assert getattr(self.request_parser, "version") == version
        assert getattr(self.request_parser, "body") == body
        assert getattr(self.request_parser, "stream") == self.valid_request_stream


class TestRequestParserWithValidPostRequestAndBody(object):

    valid_request_stream = (b"POST /login HTTP/1.1\r\n"
                            b"Host: 8.8.8.8\r\n"
                            b"Connection: keep-alive\r\n"
                            b"Cache-Control: max-age=0\r\n"
                            b"Content-Lengh: 10\r\n"
                            b"Upgrade-Insecure-Requests: 1\r\n"
                            b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                            b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                            b"Accept-Encoding: gzip, deflate\r\n"
                            b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n"
                            b"\r\n"
                            b"2d2d2d2d2d2d5765624b69")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.request_parser = RequestParser(self.valid_request_stream)

    def test_run(self):
        self.request_parser.run()

        start_line = ["POST", "/login", "HTTP/1.1"]
        headers = {
            "host" : "8.8.8.8",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "content-lengh" : "10",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "POST"
        uri = "/login"
        version = "HTTP/1.1"
        body = "2d2d2d2d2d2d5765624b69".decode("hex")

        assert getattr(self.request_parser, "start_line") == start_line
        assert getattr(self.request_parser, "headers") == headers
        assert getattr(self.request_parser, "method") == method
        assert getattr(self.request_parser, "uri") == uri
        assert getattr(self.request_parser, "version") == version
        assert getattr(self.request_parser, "body") == body
        assert getattr(self.request_parser, "stream") == self.valid_request_stream


class TestRequestParserWithInValidGetRequestAndNoBody(object):

   invalid_request_stream = (b"GET / HTTP/1.0 \r\n"
                             b"Host: 8.8.8.8\r\n"
                             b"Connection: keep-alive\r\n"
                             b"Cache-Control: max-age=0\r\n"
                             b"Upgrade-Insecure-Requests: 1\r\n"
                             b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                             b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                             b"Accept-Encoding: gzip, deflate\r\n"
                             b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n")

   @pytest.fixture(autouse=True)
   def setup(self):
       self.request_parser = RequestParser(self.invalid_request_stream)

   def test_run(self):
       self.request_parser.run()

       start_line = ["GET", "/", "HTTP/1.0"]
       headers = {
           "Host" : "8.8.8.8",
           "connection" : "keep-alive",
           "cache-control" : "max-age=0",
           "upgrade-insecure-requests" : "10",
           "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
           "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "accept-encoding" : "gzip, deflate",
           "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
       }
       method = "get"
       uri = "/ "
       version = "HTTP/1.0"
       body = ""

       assert getattr(self.request_parser, "start_line") != start_line
       assert getattr(self.request_parser, "headers") != headers
       assert getattr(self.request_parser, "method") != method
       assert getattr(self.request_parser, "uri") != uri
       assert getattr(self.request_parser, "version") != version
       assert getattr(self.request_parser, "body") == body
       assert getattr(self.request_parser, "stream") == self.invalid_request_stream


class TestRequestParserWithInValidPostRequestAndNoBody(object):

    invalid_request_stream = (b"post /login http/1.1\r\n"
                              b"Host: 8.8.8.8\r\n"
                              b"Connection: keep-alive\r\n"
                              b"Cache-Control: max-age=0\r\n"
                              b"Upgrade-Insecure-Requests: 1\r\n"
                              b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                              b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                              b"Accept-Encoding: gzip, deflate\r\n"
                              b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n"
                              b"\r\n")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.request_parser = RequestParser(self.invalid_request_stream)

    def test_run(self):
        self.request_parser.run()

        start_line = ["POST", " /login", "HTTP/1.1"]
        headers = {
            "host" : "8.8.8.4",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "POST"
        uri = "/login "
        version = "HTTP/1.1 "
        body = ""

        assert getattr(self.request_parser, "start_line") != start_line
        assert getattr(self.request_parser, "headers") != headers
        assert getattr(self.request_parser, "method") != method
        assert getattr(self.request_parser, "uri") != uri
        assert getattr(self.request_parser, "version") != version
        assert getattr(self.request_parser, "body") == body
        assert getattr(self.request_parser, "stream") == self.invalid_request_stream


class TestRequestParserWithInValidPostRequestAndInValidBody(object):

    invalid_request_stream = (b"POST /login HTTP/1.1\r\n"
                              b"Host: 8.8.8.8\r\n"
                              b"Connection: keep-alive\r\n"
                              b"Cache-Control: max-age=0\r\n"
                              b"Content-Lengh: 10\r\n"
                              b"Upgrade-Insecure-Requests: 1\r\n"
                              b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                              b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                              b"Accept-Encoding: gzip, deflate\r\n"
                              b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n"
                              b"2d2d2d2d2d2d5765624b69")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.request_parser = RequestParser(self.invalid_request_stream)

    def test_run(self):
        self.request_parser.run()

        start_line = ["post", "/login ", "http/1.1"]
        headers = {
            "Host" : "8.8.8.8",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "content-lengh" : "10",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "post"
        uri = "/"
        version = "HTTP/1.1 "
        body = "2d2d2d2d2d2d5765624b69".decode("hex")

        assert getattr(self.request_parser, "start_line") != start_line
        assert getattr(self.request_parser, "headers") != headers
        assert getattr(self.request_parser, "method") != method
        assert getattr(self.request_parser, "uri") != uri
        assert getattr(self.request_parser, "version") != version
        assert getattr(self.request_parser, "body") != body
        assert getattr(self.request_parser, "stream") == self.invalid_request_stream


class TestRequestParserWithInValidPostRequestAndValidBody(object):

    invalid_request_stream = (b"POST /login HTTP/1.1\r\n"
                              b"Host: 8.8.8.8\r\n"
                              b"Connection: keep-alive\r\n"
                              b"Cache-Control: max-age=0\r\n"
                              b"Content-Lengh: 10\r\n"
                              b"Upgrade-Insecure-Requests: 1\r\n"
                              b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                              b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                              b"Accept-Encoding: gzip, deflate\r\n"
                              b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n"
                              b"\r\n"
                              b"------WebKit")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.request_parser = RequestParser(self.invalid_request_stream)

    def test_run(self):
        self.request_parser.run()

        start_line = ["post", "/login ", "http/1.1"]
        headers = {
            "Host" : "8.8.8.9",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "content-lengh" : "10",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "post"
        uri = "/"
        version = "HTTP/1.1 "
        body = "2d2d2d2d2d2d5765624b69".decode("hex")

        assert getattr(self.request_parser, "start_line") != start_line
        assert getattr(self.request_parser, "headers") != headers
        assert getattr(self.request_parser, "method") != method
        assert getattr(self.request_parser, "uri") != uri
        assert getattr(self.request_parser, "version") != version
        assert getattr(self.request_parser, "body") != body
        assert getattr(self.request_parser, "stream") == self.invalid_request_stream


class TestRequestFileParserWithoutFileName(object):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.request_file_parser = RequestFileParser("")

    def test_run(self):
        self.request_file_parser.run()

        assert getattr(self.request_file_parser, "start_line") == []
        assert getattr(self.request_file_parser, "headers") == {}
        assert getattr(self.request_file_parser, "method") == ""
        assert getattr(self.request_file_parser, "uri") == ""
        assert getattr(self.request_file_parser, "version") == ""
        assert getattr(self.request_file_parser, "body") == ""
        assert getattr(self.request_file_parser, "stream") == ""
        assert getattr(self.request_file_parser, "file_name") == ""


class TestRequestFileParserWithFileNameAndValidStreamAndNoBody(object):

    temporary_request_file = "temporary_request_file"
    valid_request_stream = (b"GET / HTTP/1.1\r\n"
                            b"Host: 8.8.8.8\r\n"
                            b"Connection: keep-alive\r\n"
                            b"Cache-Control: max-age=0\r\n"
                            b"Upgrade-Insecure-Requests: 1\r\n"
                            b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                            b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                            b"Accept-Encoding: gzip, deflate\r\n"
                            b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n")

    @pytest.fixture(autouse=True)
    def setup(self):
        with open(self.temporary_request_file, "w") as f:
            f.write(self.valid_request_stream)

        self.request_file_parser = RequestFileParser(self.temporary_request_file)

    def test_run(self):
        self.request_file_parser.run()

        start_line = ["GET", "/", "HTTP/1.1"]
        headers = {
            "host" : "8.8.8.8",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "GET"
        uri = "/"
        version = "HTTP/1.1"
        body = ""

        assert getattr(self.request_file_parser, "start_line") == start_line
        assert getattr(self.request_file_parser, "headers") == headers
        assert getattr(self.request_file_parser, "method") == method
        assert getattr(self.request_file_parser, "uri") == uri
        assert getattr(self.request_file_parser, "version") == version
        assert getattr(self.request_file_parser, "body") == body
        assert getattr(self.request_file_parser, "stream") == ""

        # teardown
        try:
            os.remove(self.temporary_request_file)
        except OSError, e:
            print ("Error : %s is not removed.\n%s" % (self.temporary_request_file, e))


class TestRequestFileParserWithFileNameAndValidStreamAndBody(object):

    temporary_request_file = "temporary_request_file"
    valid_request_stream = (b"POST /login HTTP/1.1\r\n"
                              b"Host: 8.8.8.8\r\n"
                              b"Connection: keep-alive\r\n"
                              b"Cache-Control: max-age=0\r\n"
                              b"Content-Lengh: 10\r\n"
                              b"Upgrade-Insecure-Requests: 1\r\n"
                              b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                              b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                              b"Accept-Encoding: gzip, deflate\r\n"
                              b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n"
                              b"\r\n"
                              b"2d2d2d2d2d2d5765624b69")

    @pytest.fixture(autouse=True)
    def setup(self):
        with open(self.temporary_request_file, "w") as f:
            f.write(self.valid_request_stream)

        self.request_file_parser = RequestFileParser(self.temporary_request_file)

    def test_run(self):
        self.request_file_parser.run()

        start_line = ["POST", "/login", "HTTP/1.1"]
        headers = {
            "host" : "8.8.8.8",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "content-lengh" : "10",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "POST"
        uri = "/login"
        version = "HTTP/1.1"
        body = "2d2d2d2d2d2d5765624b69".decode("hex")

        assert getattr(self.request_file_parser, "start_line") == start_line
        assert getattr(self.request_file_parser, "headers") == headers
        assert getattr(self.request_file_parser, "method") == method
        assert getattr(self.request_file_parser, "uri") == uri
        assert getattr(self.request_file_parser, "version") == version
        assert getattr(self.request_file_parser, "body") == body
        assert getattr(self.request_file_parser, "stream") == ""

        # teardown
        try:
            os.remove(self.temporary_request_file)
        except OSError, e:
            print ("Error : %s is not removed.\n%s" % (self.temporary_request_file, e))


class TestRequestFileParserWithFileNameAndInValidStreamAndBody(object):

    temporary_request_file = "temporary_request_file"
    valid_request_stream = (b"post / HTTP/1.0\r\n"
                              b"Host: 8.8.8.8\r\n"
                              b"Connection: keep-alive\r\n"
                              b"Cache-Control: max-age=0\r\n"
                              b"Upgrade-Insecure-Requests: 1\r\n"
                              b"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n"
                              b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
                              b"Accept-Encoding: gzip, deflate\r\n"
                              b"Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n"
                              b"\r\n"
                              b"------WebKit")

    @pytest.fixture(autouse=True)
    def setup(self):
        with open(self.temporary_request_file, "w") as f:
            f.write(self.valid_request_stream)

        self.request_file_parser = RequestFileParser(self.temporary_request_file)

    def test_run(self):
        self.request_file_parser.run()

        start_line = ["POST", "/login", "HTTP/1.1"]
        headers = {
            "host" : "8.8.8.8",
            "connection" : "keep-alive",
            "cache-control" : "max-age=0",
            "content-lengh" : "10",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding" : "gzip, deflate",
            "accept-language" : "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4"
        }
        method = "POST"
        uri = "/login"
        version = "HTTP/1.1"
        body = "2d2d2d2d2d2d5765624b69".decode("hex")

        assert getattr(self.request_file_parser, "start_line") != start_line
        assert getattr(self.request_file_parser, "headers") != headers
        assert getattr(self.request_file_parser, "method") != method
        assert getattr(self.request_file_parser, "uri") != uri
        assert getattr(self.request_file_parser, "version") != version
        assert getattr(self.request_file_parser, "body") != body
        assert getattr(self.request_file_parser, "stream") == ""

        # teardown
        try:
            os.remove(self.temporary_request_file)
        except OSError, e:
            print ("Error : %s is not removed.\n%s" % (self.temporary_request_file, e))
