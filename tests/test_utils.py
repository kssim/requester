# -*- coding: utf-8 -*-

import pytest

from requester.utils import (
    make_host, make_request_url, make_dumy_body, make_ellipsis
)


class TestMakeHost(object):

    @pytest.mark.parametrize("headers, dst_ip, expected", [
            ({}, "8.8.8.8", "8.8.8.8"),
            ({"Host":"http://test.com"}, "8.8.8.8", "http://test.com"),
            ({"host":"http://test.com"}, "8.8.8.8", "http://test.com")
        ])
    def test_make_valid_host(self, headers, dst_ip, expected):
        assert make_host(headers, dst_ip) is expected

    @pytest.mark.parametrize("headers, dst_ip, expected", [
            ({}, "8.8.8.8", "8.8.8.9"),
            ({"Host":"http://test.com"}, "8.8.8.8", "8.8.8.8"),
            ({"host":"http://test.com"}, "8.8.8.8", "8.8.8.8"),
            ({"Host1":"http://test.com"}, "8.8.8.8", "http://test.com"),
            ({"HOST":"http://test.com"}, "8.8.8.8", "http://test.com"),
            ({"host1":"http://test.com"}, "8.8.8.8", "http://test.com")
        ])
    def test_make_invalid_host(self, headers, dst_ip, expected):
        assert make_host(headers, dst_ip) is not expected


class TestMakeRequestUrl(object):

    @pytest.mark.parametrize("host, port, url, expected", [
        ("http://test.com", 80, "/", "http://test.com/"),
        ("http://test.com", 443, "/", "http://test.com/"),
        ("https://test.com", 80, "/", "https://test.com/"),
        ("https://test.com", 443, "/", "https://test.com/"),
        ("test.com", 80, "/", "http://test.com/"),
        ("test.com", 443, "/", "https://test.com/"),
        ("http://test.com", 80, "/abc", "http://test.com/abc"),
        ("http://test.com", 443, "/abc", "http://test.com/abc"),
        ("https://test.com", 80, "/123", "https://test.com/123"),
        ("https://test.com", 443, "/123", "https://test.com/123"),
        ("test.com", 80, "/abc123", "http://test.com/abc123"),
        ("test.com", 443, "/abc123", "https://test.com/abc123")
    ])
    def test_make_valid_request_url(self, host, port, url, expected):
        assert make_request_url(host, port, url) == expected

    @pytest.mark.parametrize("host, port, url, expected", [
        ("http://test.com", 80, "/", "http://test.com"),
        ("http://test.com", 443, "/", "https://test.com/"),
        ("https://test.com", 80, "/", "http://test.com/"),
        ("https://test.com", 443, "/", "https://test.com"),
        ("test.com", 80, "/", "http://test.com:80"),
        ("test.com", 443, "/", "https://test.com:443"),
        ("test.com", 80, "/", "http://test.com:80/"),
        ("test.com", 443, "/", "https://test.com:443/"),
        ("http://test.com", 80, "/abc", "http://test.com/abcd"),
        ("http://test.com", 443, "/abc", "http://test.com/abcd"),
        ("https://test.com", 80, "/123", "http://test.com/123"),
        ("https://test.com", 443, "/123", "http://test.com/123"),
        ("test.com", 80, "/abc123", "http://test.com/abc"),
        ("test.com", 443, "/abc123", "https://test.com/abc"),
        ("test.com", 80, "/abc123", "test.com/abc123"),
        ("test.com", 443, "/abc123", "test.com/abc123")
    ])
    def test_make_invalid_request_url(self, host, port, url, expected):
        assert make_request_url(host, port, url) != expected


class TestMakeDumyBody(object):

    @pytest.mark.parametrize("byte, expected", [
        (1, "\x00"),
        (5, "\x00\x00\x00\x00\x00"),
        (10, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
        (None, ""),
        (-1, "")
    ])
    def test_make_dumy_body(self, byte, expected):
        assert make_dumy_body(byte) == expected


class TestMakeEllipsis(object):

    @pytest.mark.parametrize("text, max_len, expected", [
        ("123456", 3, "123..."),
        ("1234567890123", 10, "1234567890..."),
        ("123", 5, "123"),
        ("123", -1, "123"),
        ("123", 0, "123")
    ])
    def test_make_ellipsis(self, text, max_len, expected):
        assert make_ellipsis(text, max_len) == expected
