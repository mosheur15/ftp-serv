#! /usr/bin/python3

'''
File: authentication.py
Author: mosheur rahman
Description: authentication module for server.
'''
from sys import exit
from json import load, dump
from os.path import exists
from bcrypt import hashpw, gensalt, checkpw

class File:
    """
    Handle auth file. (load/read/write/edit)
    filename: auth.json
    format: json
    """
    
    def __init__(self, filename='auth.json'):
        """
        filename: str - name of the aouth file.
        """
        self.filename = filename
        self.default = {
            "AUTH_V": " 1.0"
        }
    
    def create_default(self):
        """
        write default authentication file.
        (auth.json)
        """
        with open(self.filename, 'w') as file:
            dump(self.default, file)
            return True
    
    def write(self, data):
        """
        write data to the file.
        return True if success.
        else return False
        
        data : dict - data to write.
        """
        try:
            with open (self.filename, 'w') as file:
                dump(data, file)
                return True
        except Exception as e:
            return False
            
    def load(self):
        """
        load data from file.
        return data (type: dict) if success.
        else return False
        """
        try:
            # check if file exists or not.
            # if not exists create default.
            # else continue.
            if not (exists(self.filename)):
                self.create_default()
                return self.default
                
            with open(self.filename, 'r') as file:
                data = load(file)
                return data
                
        except Exception as e:
            return False
        
            

class Auth:
    """
    Handle user authentication with CURD.
    (CREATE, RETRIVE, UPDATE, DELETE)
    """
    
    def __init__(self, filename='auth.json'):
        """
        filename: str - name of the auth file.
        """
        self.file = File(filename=filename)
        self.filename = filename
        # existing file data.
        temp = self.file.load()
        if not temp: 
            print ('invalid file')
            return
        self.data = temp
        
    def get_user(self, username):
        """
        Retrive a user. search with username only.
        return user info if user exists.
        else return False.
        
        username: str - username of the user.
        """
        # return False if user list doesn't exists.
        if not "users" in self.data.keys(): return False
        
        for user in self.data.get('users'):
            if user.get('username') == username:
                return user
                
        return False
        
    def hash_password(self, password):
        """
        hash (encrypt) plaintext password.
        encryption type: bcrypt (one way encryption).
        return hash (str) if success.
        else return False
        
        password - str - password to hash.
        """
        password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        return password
        
    def create_user(self, username, password):
        """
        Create a ftp user.
        return True if success
        else return False.
        
        username: str - username of the user.
        password: str - password for the user.
        """
        if self.get_user(username):
            print (f'{username} already exists.')
            return False
        
        password = self.hash_password(password)
        user = {
            "username": username,
            "password": password,
        }
        
        # create list for users if doesn't exists.
        if not 'users' in self.data.keys(): self.data['users'] = []
        
        self.data['users'].append(user)
        written = self.file.write(self.data)
        if written: return True
        return False
        
    def get_users(self):
        """
        Get all the users.
        return users list.
        """
        if self.data.get('users'):
            return self.data.get('users')
        return []
        
    def update(self, username, password):
        """
        Update password for a existing user.
        return True if success.
        else return False.
        
        username: str - username of the user.
        password: str - password of the user.
        """
        if not self.get_user(username):
            print (f"user '{username}' not found.")
            return False
        
        password = self.hash_password(password)
        index = 0
        for user in self.data["users"]:
            if user.get('username') == username:
                break
            index += 1 
            
        self.data['users'][index]['password'] = password
        return True
        
    def delete_user(self, username):
        """
        delete a user.
        return True if success.
        else return false.
        
        username - str - username of the user.
        """
        if not self.get_user(username):
            print(f"user {username} not found!")
            return False
        
        # remove user.
        index = 0
        for user in self.data.get('users'):
            if user.get('username') == username:
                del self.data['users'][index]
                self.file.write(self.data)
                return True
            index += 1
            
        return False
        
        
    def login(self, username, password):
        if not self.get_user(username):
            return False
            
        user_pass = self.get_user(username).get('password')
        match = checkpw(password.encode('utf-8'), user_pass.encode('utf-8'))
        return match
        