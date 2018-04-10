#!/usr/bin/python
from __future__ import absolute_import
import os
import sys
from .actions import *

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
def main():
    """
    Parse cli args and launch the program
    """
    init_terminal()
    cmd = sys.argv[1]
    config = ConfigParser()
    if cmd == 'dl':
        download(config, sys.argv[2])
    if cmd == 'search':
        if len(sys.argv) > 3:
            search(config, sys.argv[2], sys.argv[3])
        else:
            search(config, sys.argv[2])
    elif cmd == 'reset':
        reset_config(config, sys.argv[2])
    elif cmd == 'config':
        update_config(config, sys.argv[2], sys.argv[3])
    else:
        print_error("Command unrecognized!")

if __name__ == '__main__':
    main()
