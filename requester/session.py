# -*- coding: utf-8 -*-

import requests

class Session(object):

    __attrs__ = [
        "session", "request_headers", "method", "allow_redirects", "timeout"
    ]


    def __init__(self):
        self.session = requests.Session()
        self.allow_redirects = False
        self.timeout = 10


    def update_headers(self, headers):
        self.request_headers = headers
        self.session.headers.update(self.request_headers)


    def update_connection_info(self,
            method = None, allow_redirects = False, timeout = 10):
        self.method = method
        self.allow_redirects = False
        self.timeout = timeout


    def send(self, url, verbose=True):
        response = []

        if self.method == "GET":
            response = self.session.get(url, allow_redirects = self.allow_redirects, timeout = self.timeout)
        else:
            print ("Error : The HTTP method is not valid")
            return False

        if verbose == True:
            self.show_request()
            print ("\n\n")
            self.show_response(response)

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


    def show_response(self, response):
        print ("** RESPONSE **")
        print ("======================================================")
        print ("Status code : %s" % response.status_code)
        print ("Status reasone : %s" % response.reason)
        print ("======================================================")
        print ("= Response header =")
        for key, value in response.headers.items():
            print ("%s : %s" % (key, value))
        print ("======================================================")
        print ("= Response body =")
        print (response.text)
        print ("======================================================")
