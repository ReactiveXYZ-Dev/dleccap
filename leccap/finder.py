from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import input
from builtins import object
import os
import sys
import wget
import json
import time
from .utils import *
from .constants import *
from bs4 import BeautifulSoup

"""
Lecture search procedure

@Version 2.0.0
"""
class Finder(object):

    def __init__(self):
        self._authenticator = None

    def set_auth(self, auth):
        """
        Inject authenticator
        
        Arguments:
            auth {Authenticator}
        """
        self._authenticator = auth

    def get_auth(self):
        """
        Retrieve the authenticator
        
        Returns:
            Authenticator
        """
        return self._authenticator

    def requires_auth(self):
        """
        Whether this finder requires authentication
        
        Returns:
            bool
        """
        return True
    
    def search(self, subject, year=None):
        # normalize subject
        subject = self.normalize(subject)
        url = self._web_url(year)
        return self._find_site_url(subject, url)
    
    """
    Helpers
    """
    def _web_url(self, year):
        return WEB_BASE_URL + str(year) if year else WEB_BASE_URL

    def normalize(self, s):
        return s.strip().replace(' ', '').lower()
    
    def _find_site_url(self, subject, web_url):
        # visit the webpage
        r = self._authenticator.session().get(web_url)
        html = BeautifulSoup(r.text, "html.parser")
        # find recording section
        div = html.find(id="recordings")
        if not div:
            return None
        for a in div.contents:
            if subject in self.normalize(a.string):
                return "%ssite/%s" % (WEB_BASE_URL, a['href'].split('/')[-1])
        return None
    
        