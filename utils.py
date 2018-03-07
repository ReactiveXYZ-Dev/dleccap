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

def print_success(text):
    s = Fore.GREEN + text
    s += Style.RESET_ALL
    print s

def print_error(text):
    s = Fore.RED + text
    s += Style.RESET_ALL
    print s

def print_warning(text):
    s = Fore.YELLOW + text
    s += Style.RESET_ALL
    print s
