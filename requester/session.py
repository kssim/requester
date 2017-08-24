# -*- coding: utf-8 -*-

import requests


class Session(object):

    __attrs__ = [
        "session", "request_headers", "request_body", "method",
        "allow_redirects", "timeout", "response"
    ]

    def __init__(self):
        self.session = requests.Session()
        self.allow_redirects = False
        self.timeout = 30

        self.request_headers = {}
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

    def send(self, url, verbose=True):
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

        if verbose is True:
            self.show_request()
            print ("\n\n")
            self.show_response()

        return True

    def show_request(self):
        print ("** REQUEST **")
        print ("======================================================")
        print ("Method : %s" % self.method)
        print ("======================================================")
        print ("= Request header =")
        for key, value in self.request_headers.items():
            print ("%s : %s" % (key, value))
        print ("======================================================")
        print ("= Request body =")
        print (self.request_body)
        print ("======================================================")

    def show_response(self):
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
        print (self.response.text.encode("utf-8"))
        print ("======================================================")
