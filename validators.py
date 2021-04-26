'''
File: validators.py
Author: mosheur rahman
Description: validators for parser.
'''
from argparse import ArgumentTypeError
from os.path import exists
from string import (
    ascii_uppercase,
    ascii_lowercase,
    digits,
)

def path_validator(path):
    """
    check if path exists or not.
    if doesn't exists raise argparse.ArgumentTypeError.
    else return path.
    """
    if not exists(path):
        raise ArgumentTypeError(f"Invalid target. path => '{path}' not found.")
    return path
    
    
def int_validator(num):
    """
    check if string can be converted to integer.
    example:
        int ('20')
    if success return int.
    else raise argparse.ArgumentTypeError
    """
    try:
        num = int(num)
    except:
        raise ArgumentTypeError(f"Invalid number '{num}'.")
        
    if num < 0:
        raise ArgumentTypeError(f"Invalid number '{num}'.")
        
    return num
    
    
def port_validator(port):
    """
    check if port is valid and 4 digit long.
    if valid return port -> int.
    else raise argparse.ArgumentTypeError
    """
    port = int_validator(port)
    if len(str(port)) < 4:
        raise ArgumentTypeError("port number must be at least 4 digit long")
    if port > 35550:
        raise ArgumentTypeError(f"'{port}' is a Invalid port, max port number is 35550")
        
    return port
    
    
def max_con (con):
    """
    check if maximum connection is valid.
    return con -> int if valid.
    else raise argparse.ArgumentTypeError
    """
    con = int_validator(con)
    if con < 1:
        raise ArgumentTypeError('max connection cannot be less than 1')
    
    if con > 255:
        raise ArgumentTypeError('max connection cannot be greater than 255')
        
    return con
    
def max_con_per_ip(con):
    """
    check if maximum connection per client is valid.
    return con -> int if valid.
    else raise argparse.ArgumentTypeError
    """
    con = int_validator(con)
    if con < 1:
        raise ArgumentTypeError('max connection cannot be less than 1')
    
    if con > 10:
        raise ArgumentTypeError('max connection cannot be greater than 10')
    return con
    
def username_validator(username):
    """
    check if username contains invalid char.
    return username if valid.
    else raise argparse.ArgumentTypeError
    """
    if not all([(i in ascii_lowercase+ascii_uppercase+digits) for i in username]):
        raise ArgumentTypeError('Invalid username, username can only contains letters amd numbers.')
    return username
    
    