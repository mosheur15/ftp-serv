'''
File: parser.py
Author: mosheur rahman
Description: parsing module for server.py.
'''

from argparse import ArgumentParser
from server import server
from authentication import Auth
from getpass import getpass
from validators import (
    username_validator,
    path_validator,
    port_validator,
    max_con_per_ip,
    max_con,
)

auth = Auth()

def input_(msg='', pswd=False):
    """
    take user input and handle ctrl+c, ctrl+d, esc.
    return input
    """
    try:
        if not pswd:
            data = input(msg)
            return data
        
        data = getpass(msg)
        return data
        
    except (KeyboardInterrupt, EOFError):
        print ('tarminated!')
        exit()

def args_cleaner(args):
    """
    Clean junck from arguments.
    and preapare arguments so it can be passed as kwargs.
    - fo(**args)
    returns dict
    """
    # convert namespace to dict
    args = dict(args._get_kwargs())
    
    # remove handler.
    if args.__contains__('handler'):
        args.pop('handler')
    
    # remove keys with no value (None)
    clean_data = {}
    for key, val in args.items():
        if val: clean_data.update({key:val})
        
    return clean_data


def run_server(args=False):
    """
    Run the server.
    """
    # if args not passed.
    if not args:
        srv = server()
        srv.run()
        return
    
    # if args passed.
    args = args_cleaner(args)
    # (**args) => unpack dict to pass kwarg.
    # foo(**args) => foo(key=val, ...)
    srv = server(**args)
    srv.run()


def create_user(args):
    """
    Create a ftp user.
    - args - Namespace - command line arguments (argparse => parse_args).
    """
    args = args_cleaner(args)
    
    # check if username has been passed.
    if args.get('username'): username = args.get('username')
    else: username = input_(msg='username: ')
    
    # check if username already exists.
    if auth.get_user(username):
        print (f"'{username}' already exists.")
        return
    
    password = input_(msg=f"password for '{username}' (hidden): ", pswd=True)
    
    # create the user.
    created = auth.create_user(username, password)
    if not created:
        print ('Something went wrong. please try again.')
        return
    
    print (f"user '{username}' has been created.")


def update_user(args):
    """
    Update a user.
    - args - Namespace - command line arguments (argparse => parse_args).
    """
    args = args_cleaner(args)
    
    # check if username has been passed.
    if args.get('username'): username = args.get('username')
    else: username = input_(msg='username: ')
    
    # check if user doesn't exists.
    if not auth.get_user(username):
        print (f"user '{username}' does not exists.")
        return
    
    # update the user.
    password = input_(msg=f"password for '{username}' (hidden): ", pswd=True)
    updated = auth.update(username, password)
    if not updated:
        print ('Something went wrong. please try again!')
        return
    
    print (f"'{username}' has been updated.")


def show_user(args):
    """
    show user info.
    - args - command line arguments (argparse => parse_args).
    """
    args = args_cleaner(args)
    
    # check if username has been passed.
    if args.get('username'): username = args.get('username')
    else: username = input_(msg='username: ')
    
    # check if user doesn't exists.
    if not auth.get_user(username):
        print (f"user '{username}' does not exists.")
        return
    
    # print user info
    password_hash = auth.get_user(username).get('password')
    print ('info: ')
    print (f'\tusername: {username}')
    print (f'\tpassword hash: {password_hash}')
    


def delete_user(args):
    """
    delete a user.
    - args - Namespace - command line arguments (argparse => parse_args).
    """
    args = args_cleaner(args)
    
    # check if username passed.
    if args.get('username'): username = args.get('username')
    else: username = input_(msg='username: ')
    
    # check if user doesn't exists.
    if not auth.get_user(username):
        print (f"user '{username}' does not exists")
        return
    
    # delete the user.
    deleted = auth.delete_user(username)
    if not deleted:
        print ('Something went wrong. please try again!')
        return
    
    print (f"user '{username}' has been deleted!")


parser = ArgumentParser()
subparser = parser.add_subparsers()

# handle server arguments.
run = subparser.add_parser('run', help='run the server.')
run.add_argument('-t', '--target',          type=path_validator,    metavar='', help='target dorectory.')
run.add_argument('-p', '--port',            type=port_validator,    metavar='', help='port to run')
run.add_argument('-m', '--max-con',         type=max_con,           metavar='', help='maximum connection.')
run.add_argument('-M', '--max-con-per-ip',  type=max_con_per_ip,    metavar='', help='maximum connection per ip')
run.set_defaults(handler=run_server)

# handle user creation
create = subparser.add_parser('create', help='create a user.')
create.add_argument('-u', '--username', type=username_validator, metavar='', help='username of the user.')
create.set_defaults(handler=create_user)

# handle user update
update = subparser.add_parser('update', help='update a user.')
update.add_argument('-u', '--username', type=username_validator, metavar='', help='username of the user.')
update.set_defaults(handler=update_user)

# handle show user
show = subparser.add_parser('show', help='show user info.')
show.add_argument('-u', '--username', type=username_validator, metavar='', help='show user with this username.')
show.set_defaults(handler=show_user)

# handle delete user.
delete = subparser.add_parser('delete', help='delete a user')
delete.add_argument('-u', '--username', type=username_validator, metavar='', help='username of the user.')
delete.set_defaults(handler=delete_user)

args = parser.parse_args()
if args._get_kwargs():
    args.handler(args)
    exit()
    
run_server()