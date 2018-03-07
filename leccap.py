#!/usr/bin/python

import sys
from utils import *
from config import ConfigParser

"""
University Of Michigan Lecture Videos Downloader 

@Authored By: Maxim Aleksa maximal@umich.edu
@Updated By: Jackie Zhang jackierw@umich.edu
@Version: 2.0.0

Usage: 
leccap dl url
leccap reset [logins|path|concurrency|all]
leccap config [login.username|login.password|concurrecy] [$value]
"""

def download(config, url):
    pass

def reset_config(config, key):
    if key == 'all':
        # reset all
        config.set('logins', {'username': "", 'password': ""})
        config.set('concurrency', 5)
        config.set('dest_path', '.')
    else:
        # reset parts
        if key == 'logins.username' or key == 'logins.password':
            config.set(key, "")
        elif key == 'concurrency':
            config.set(key, 5)
        elif key == 'dest_path':
            config.set(key, '.')
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
    cmd = sys.argv[1]
    config = ConfigParser()
    if cmd == 'dl':
        download(config, sys.argv[2])
    elif cmd == 'reset':
        reset_config(config, sys.argv[2])
    elif cmd == 'config':
        update_config(config, sys.argv[2], sys.argv[3])
    else:
        print_error("Please use the correct command!")

if __name__ == '__main__':
    main()
