import json
import random
import string
import os


class Account:
    def __init__(self, username, password, balance, cc=None):
        if cc is None:
            unique_cc = self.__generate_unique_cc()
            self.cc = unique_cc
        else:
            self.cc = cc
        self.username = username
        self.password = password
        self.balance = float(balance)

    def __check_cc_exists(self, cc):
        try:
            with open('/Users/susannamau/Dev/BPER/Python/webapp/app/data/user_data.json', 'r') as file:
                data = json.load(file)
                if cc in data:
                    return True
                return False
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("JSON decode error")
        
    def deposit(self, amount):
        if amount < 0:
            raise ValueError('Amount must be positive')
        else:
            self.balance += amount
            with open('/Users/susannamau/Dev/BPER/Python/webapp/app/data/user_data.json', 'r') as file:
                data = json.load(file)
            data[self.username]['balance'] = self.balance
            with open('/Users/susannamau/Dev/BPER/Python/webapp/app/data/user_data.json', 'w') as file:
                json.dump(data, file)
        return self
        
    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError("You don\'t have enough money")
        else:
            self.balance -= amount
            with open('/Users/susannamau/Dev/BPER/Python/webapp/app/data/user_data.json', 'r') as file:
                data = json.load(file)
            data[self.username]['balance'] = self.balance
            with open('/Users/susannamau/Dev/BPER/Python/webapp/app/data/user_data.json', 'w') as file:
                json.dump(data, file)
        return self

    def __str__(self):
        return f'CC: {self.cc}, name: {self.username}, balance: {self.balance}'
    
    def serialize(self):
        return {
            'username': self.username,
            'password': self.password,  # Consider handling password securely
            'balance': self.balance,
            'cc': self.cc
        }

    @classmethod
    def deserialize(cls, data):
        return cls(
            username=data['username'],
            password=data['password'],  # Handle password security here
            balance=data['balance'],
            cc=data.get('cc')  # Use get() to handle missing cc gracefully
        )