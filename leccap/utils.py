from __future__ import print_function
from builtins import range
from colorama import init, Fore, Style

"""
Utility functions

@Version 2.0.0
"""

def init_terminal():
    """
    Initialize terminal color settings
    """
    init()

def print_info(text, ret=False):
    s = Fore.CYAN + text
    s += Style.RESET_ALL
    if ret:
        return s
    else:
        print(s)

def print_success(text, ret=False):
    s = Fore.GREEN + text
    s += Style.RESET_ALL
    if ret:
        return s
    else:
        print(s)

def print_error(text, ret=False):
    s = Fore.RED + text
    s += Style.RESET_ALL
    if ret:
        return s
    else:
        print(s)

def print_warning(text, ret=False):
    s = Fore.YELLOW + text
    s += Style.RESET_ALL
    if ret:
        return s
    else:
        print(s)

def chunks(l, n):
    """
    Slice list into chunks
    
    Arguments:
        l {list}
        n {int} -- Num items per chunk
    """

    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]
