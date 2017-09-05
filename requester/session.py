# -*- coding: utf-8 -*-

"""
This module is responsible for the session-related logic.
"""

import requests

from utils import make_ellipsis
from structures import CaseInsensitiveDict


class RequestsSession(requests.Session):
    """
    In the requests library, if there is data in the body,
    the content-length is computed with the size of the actual body

    I wrote the following code to send to the content-length
    you entered in the request statement.
    """
    def __init__(self):
        requests.Session.__init__(self)

    def prepare_request(self, request):
        p = requests.Session.prepare_request(self, request)

        if "content-length" in self.headers:
            p.headers["content-length"] = self.headers["content-length"]

        return p


class Session(object):

    __attrs__ = [
        "session", "request_headers", "request_body", "method",
        "allow_redirects", "timeout", "response"
    ]

    def __init__(self):
        self.session = RequestsSession()
        self.allow_redirects = False
        self.timeout = 30

        self.request_headers = CaseInsensitiveDict()
        self.request_body = ""
        self.response = None

    def update_headers(self, headers):
        if headers is None:
            self.request_headers = getattr(self.session, "headers")
        else:
            self.request_headers = headers

        self.session.headers.update(self.request_headers)

    def update_body(self, body):
        self.request_body = body

    def update_connection_info(self, method, allow_redirects=False, timeout=30):
        self.method = method
        self.allow_redirects = allow_redirects
        self.timeout = timeout

    def send(self, url, verbose=True, verbose_detail=False):
        try:
            if self.method == "GET":
                self.response = self.session.get(url, allow_redirects=self.allow_redirects, timeout=self.timeout)
            elif self.method == "POST":
                self.response = self.session.post(url, allow_redirects=self.allow_redirects, timeout=self.timeout, data=self.request_body)
            else:
                print ("Error : The HTTP method is not valid")
                return False
        except requests.exceptions.ConnectionError:
            print ("Error : The host(%s) is not reachable" % url)
            return False

        if verbose is False:
            return True

        self.show_request(verbose_detail)
        print ("\n\n")
        self.show_response(verbose_detail)

        return True

    def show_request(self, verbose):
        print ("** REQUEST **")
        print ("======================================================")
        print ("Method : %s" % self.method)
        print ("======================================================")
        print ("= Request header =")
        for key, value in self.request_headers.items():
            print ("%s : %s" % (key, value))
        print ("======================================================")
        print ("= Request body =")
        body = self.request_body if verbose else make_ellipsis(self.request_body)
        print (body)
        print ("======================================================")

    def show_response(self, verbose):
        print ("** RESPONSE **")
        print ("======================================================")
        print ("Status code : %s" % self.response.status_code)
        print ("Status reasone : %s" % self.response.reason)
        print ("======================================================")
        print ("= Response header =")
        for key, value in self.response.headers.items():
            print ("%s : %s" % (key, value))
        print ("======================================================")
        print ("= Response body =")
        body = self.response.text.encode("utf-8") if verbose else make_ellipsis(self.response.text.encode("utf-8"))
        print (body)
        print ("======================================================")
