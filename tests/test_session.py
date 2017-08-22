# -*- coding: utf-8 -*-

import pytest

from requester.session import Session


class TestSession(object):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.session = Session()


    @pytest.mark.parametrize("headers, expected", [
        ({"Content-Length":"15"}, {"Content-Length":"15"}),
        ({"Host":"test.com", "Content-Length":"15"}, {"Host":"test.com", "Content-Length":"15"})
    ])
    def test_update_headers_valid(self, headers, expected):
        self.session.update_headers(headers)
        assert getattr(self.session, "request_headers") == expected

    @pytest.mark.parametrize("headers, expected", [
        ({"Content-Length":"15"}, {"content-length":"15"}),
        ({"Host":"test.com", "Content-Length":"15"}, {"host":"test.com ", "content-length":"15"})
    ])
    def test_update_headers_invalid(self, headers, expected):
        self.session.update_headers(headers)
        assert getattr(self.session, "request_headers") != expected


    @pytest.mark.parametrize("body, expected", [
        ("body data", "body data"),
        ("2d2d2d2d2d2d5765624b69", "2d2d2d2d2d2d5765624b69")
    ])
    def test_update_body_valid(self, body, expected):
        self.session.update_body(body)
        assert getattr(self.session, "request_body") == expected

    @pytest.mark.parametrize("body, expected", [
        ("body data", "2d2d2d2d2d2d5765624b69"),
        ("2d2d2d2d2d2d5765624b69", "body data")
    ])
    def test_update_body_invalid(self, body, expected):
        self.session.update_body(body)
        assert getattr(self.session, "request_body") != expected


    @pytest.mark.parametrize("method, expected", [
        ("GET", "GET"),
        ("POST", "POST")
    ])
    def test_update_connection_info_valid(self, method, expected):
        self.session.update_connection_info(method)
        assert getattr(self.session, "method") == expected

    @pytest.mark.parametrize("method, expected", [
        ("GET", "get"),
        ("POST", "post")
    ])
    def test_update_connection_info_invalid(self, method, expected):
        self.session.update_connection_info(method)
        assert getattr(self.session, "method") != expected

    @pytest.mark.parametrize("method, allow_redirects, timeout, expected_method, expected_allow_redirects, expected_timeout", [
        ("GET", False, 30, "GET", False, 30),
        ("POST", True, 10, "POST", True, 10)
    ])
    def test_update_connection_info_valid_expand(self, method, allow_redirects, timeout, expected_method, expected_allow_redirects, expected_timeout):
        self.session.update_connection_info(method, allow_redirects, timeout)
        assert getattr(self.session, "method") == expected_method
        assert getattr(self.session, "allow_redirects") == expected_allow_redirects
        assert getattr(self.session, "timeout") == expected_timeout

    @pytest.mark.parametrize("method, allow_redirects, timeout, expected_method, expected_allow_redirects, expected_timeout", [
        ("GET", False, 30, "get", True, 10),
        ("POST", True, 10, "GET", False, 30)
    ])
    def test_update_connection_info_invalid_expand(self, method, allow_redirects, timeout, expected_method, expected_allow_redirects, expected_timeout):
        self.session.update_connection_info(method, allow_redirects, timeout)
        assert getattr(self.session, "method") != expected_method
        assert getattr(self.session, "allow_redirects") != expected_allow_redirects
        assert getattr(self.session, "timeout") != expected_timeout
