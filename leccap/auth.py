from __future__ import absolute_import
from builtins import input
from builtins import object
import re
import os
import sys
import json
import requests
import urllib
from getpass import getpass
from .utils import *
from .constants import *
from bs4 import BeautifulSoup

"""
Lecture authentication procedures

@Version 2.0.0

"""
class Authenticator(object):

    def __init__(self):
        """
        Inject username & password to the authenticator
        
        Arguments:
            username {str} -- Umich uniqname
            password {str} -- Uniqname password
        """
        self._service_types = ["cosign-ctools", "cosign-shibboleth.umich.edu", "cosign-leccap.engin"]
        self._session = requests.Session()
        self._username = None
        self._password = None
    
    def authenticate(self, service=None):
        """
        Authenticating various umich services
        Credits to Maxim The Man

        Keyword Arguments:
            service {str} -- Service Type (default: {None})
        """
        if not service:
            for st in self._service_types:
                self._authenticate_service(st)
        else:
            self._authenticate_service(service)
    
    def ask_for_credentials(self, username=None, password=None):
        """
        Retrieve the credentials
        
        Keyword Arguments:
            username {str} -- login username (default: {None})
            password {str} -- login password (default: {None})
        """
        if username and password:
            self._username = username
            self._password = password
        else:
            # ask for raw input
            self._username = input("Your uniqname: ")
            self._password = getpass("Your password: ")       

    def is_authenticated(self):
        """
        Check whether the user has authenticated
        """
        headers = self._session.get(AUTH_PAGE_URL).headers
        return 'Set-Cookie' in headers and 'cosign=' in headers['Set-Cookie']

    def session(self):
        """
        Get the underlining requests session
        """
        return self._session

    """
    Helpers
    """
    # def _authenticate_service(self, service_type):
    #     # load login page to get cookie
    #     self._session.get(AUTH_PAGE_URL)
    #     # post to login
    #     self._session.post(AUTH_URL, {
    #         "service": service_type,
    #         "required": "",
    #         "login": self._username,
    #         "password": self._password
    #     })
    
    """
    New authentication scheme:
    Construct session:

    - GET login page for cosign session cookie
    - POST https://weblogin.umich.edu/cosign-bin/cosign.cgi with login/password for sig_request(extracted from html) which is then splited into tx and APP
    - POST api-d9c5afcf.duosecurity.com/frame/web/v1/auth with tx/parent/v for sid(extracted from html)
    - POST /frame/prompt?sid=sid with sid/device/factor for txid
    - POST /frame/status?sid=sid with sid/txid for sending status
    - POST /frame/status?sid=sid with sid/txid for polling result url
    - POST /frame/status/Result_URL for cookie
    - POST /cosign-bin/cosign.cgi with required:mtoken and duo_sig_response:cookie+:+APP
    - (Authenticated) cosign-weblogin cookie should exist now
    """
    def _authenticate_service(self, service_type):
        # get session cookie
        self._session.get(AUTH_PAGE_URL)
        # pass username/password check
        html = self._session.post(AUTH_URL, {
            "service": service_type,
            "required": "",
            "login": self._username,
            "password": self._password
        }).text
        
        try:
            # extract duo signatures/host/post_args from html
            tx, app, host, post_arg = self._extract_duo_info(html)
            # post to duo's iframe
            html = self._session.post("https://%s/frame/web/v1/auth?%s" % (
                    host, urllib.parse.urlencode({
                        'tx': tx, 'parent': "https%3A%2F%2Fweblogin.umich.edu%2Fcosign-bin%2Fcosign.cgi", 'v': '2.6'
                    })
                )
            ).text
            # extract sid and 2fa methods
            sid, devices, methods = self._extract_duo_2fa_details(html)
            

        except Exception as e:
            print_error(str(e))
    
    def _extract_duo_info(self, html):
        tx, app = self._match_duo_config(html, 'sig_request')
        host = self._match_duo_config(html, 'host')
        post_arg = self._match_duo_config(html, 'post_argument')
        return tx, app, host, post_arg
    
    def _match_duo_config(self, html, key):
        result = re.search("'%s':\s*'[^']+'" % key, html)
        if not result:
            raise Error("Could not find Duo Info. Maybe username/password is wrong?")
        content = result[0]
        value = content.replace("'", "").split()[1]
        if key == 'sig_request':
            tx, app = value.split(':')
            return tx, app
        return value

    def _extract_duo_2fa_details(self, html):
        html = BeautifulSoup(html, 'html.parser')
        # find sid input
        sid_input = html.find(attrs={"name": "sid"})
        # find devices inputs
        device_methods = html.find_all(lambda tag : tag.has_attr('data-device-index'))
        print(device_methods)
        # find methods inputs


