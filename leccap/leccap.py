#!/usr/bin/python
from __future__ import absolute_import
import os
import sys
from .utils import *
from .constants import *
from .auth import Authenticator
from .config import ConfigParser
from .download import Downloader

"""
University Of Michigan Lecture Videos Downloader 

@Authored By: Maxim Aleksa maximal@umich.edu
@Updated By: Jackie Zhang jackierw@umich.edu
@Version: 2.0.0

Usage: 
leccap dl url
leccap reset [logins|path|concurrency|all]
leccap config [login.username|login.password|concurrency] [$value]
"""

def download(config, url):
    # extract dest path
    dest_path = config.get('dest_path')
    if dest_path == '.':
        dest_path = os.getcwd()
    downloader = Downloader(url, dest_path)
    # set concurrency``
    concurrency = config.get('concurrency')
    downloader.set_concurrency(concurrency)
    # check authentication
    if downloader.requires_auth():
        auth = Authenticator()
        # check for saved credentials
        username = config.get('logins.username')
        password = config.get('logins.password')
        if username and password:
            print_info("Using saved credentials...")
            auth.ask_for_credentials(username=username, password=password)
        else:
            print_warning("Needs authentication. But you can save your credentials using ./leccap config! ")
            auth.ask_for_credentials()
        downloader.set_auth(auth)
        if not downloader.get_auth().is_authenticated():
            print_info("Authenticating...")
            downloader.get_auth().authenticate()
    # start download
    downloader.start()

def reset_config(config, key):
    if key == 'all':
        # reset all
        config.set('logins', {'username': DEFAULT_MSG, 'password': DEFAULT_MSG})
        config.set('concurrency', DEFAULT_CONCURRENCY)
        config.set('dest_path', DEFAULT_DIR)
    else:
        # reset parts
        if key == 'logins.username' or key == 'logins.password':
            config.set(key, DEFAULT_MSG)
        elif key == 'concurrency':
            config.set(key, DEFAULT_CONCURRENCY)
        elif key == 'dest_path':
            config.set(key, DEFAULT_DIR)
        else:
            print_error("Key does not exist!")
            return
    config.save()
    print_success("Config has been reset!")

def update_config(config, key, value):
    try:
        config.set(key, value)
        config.save()
    except Exception as e:
        print_error(e.message)
    else:
        print_success("Config updated and saved!")

def main():
    """
    Parse cli args and launch the program
    """
    init_terminal()
    cmd = sys.argv[1]
    config = ConfigParser()
    if cmd == 'dl':
        download(config, sys.argv[2])
    elif cmd == 'reset':
        reset_config(config, sys.argv[2])
    elif cmd == 'config':
        update_config(config, sys.argv[2], sys.argv[3])
    else:
        print_error("Command unrecognized!")

if __name__ == '__main__':
    main()
