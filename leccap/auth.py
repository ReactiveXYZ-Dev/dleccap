from __future__ import absolute_import
from builtins import input
from builtins import object
import os
import sys
import json
import requests
from getpass import getpass
from .utils import *
from .constants import *

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
        Whether the user has authenticated

        TODO: buggy if cookie expired, but usually fine
        """
        return bool(self._session.cookies.get("cosign-weblogin"))

    def session(self):
        """
        Get the underlining requests session
        """
        return self._session

    """
    Helpers
    """
    def _authenticate_service(self, service_type):
        # load login page to get cookie
        self._session.get(AUTH_PAGE_URL)
        # post to login
        self._session.post(AUTH_URL, {
            "service": service_type,
            "required": "",
            "login": self._username,
            "password": self._password
        })

