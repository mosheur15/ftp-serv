#! /usr/bin/python3

'''
File: server.py
Author: mosheur rahman
Description: a simple ftp server
'''

from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from authentication import Auth
from os import getcwd

class Login_authorizer(DummyAuthorizer):
    """
    Handle ftp logins.
    """
    def __init__(self, login_func):
        """
        login_func: func - function which will take username, password and 
        return login status. (bool - True/False).
        """
        self.login = login_func
        # call init for DummyAuthorizer
        super().__init__()
        
    def validate_authentication(self, username, password, handler):
        """
        validate user authentication.
        if login fails, it will raise validation error.
        """
        if not self.has_user(username):
            if username == 'anonymous':
                raise AuthenticationFailed('anonymous login is not allowed.')
            raise AuthenticationFailed
            
        if username != 'anonymous':
            if not self.login(username, password):
                raise AuthenticationFailed


class server:
    """
    Handle the server.
    """
    def __init__(self, target=getcwd(), port=2121, max_con=20, max_con_per_ip=5):
        """
        port :          server port.
        max_con:        maximum connection.
        max_con_per_ip: maximum connection per client.
        """
        
        self.target         = target
        self.port           = port
        self.max_con        = max_con
        self.max_con_per_ip = max_con_per_ip
        self.auth           = Auth()
        
    def run(self):
        
        authorizer = Login_authorizer(self.auth.login)
        # load users.
        users = self.auth.get_users()
        for user in users:
            username = user.get('username')
            password = user.get('password')
            if username and password:
                authorizer.add_user(username, password, self.target, perm='elradfmwMT')
        
        
        
        handler = FTPHandler
        handler.authorizer = authorizer
        address = ('', self.port)
        server = FTPServer(address, handler)
        server.max_con = self.max_con
        server.max_con_per_ip = self.max_con_per_ip
        server.serve_forever()
        