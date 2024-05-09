from flask import Flask, render_template, redirect, url_for, request
import json
import random
import string

class Account:
    def __init__(self, name, password, balance):
        unique_cc = self.__generate_unique_cc()
        self.cc = unique_cc
        self.name = name
        self.password = password
        self.balance = int(balance)

    def __generate_unique_cc(self):
        while True:
            cc = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not self.__check_cc_exists(cc):
                return cc

    def __check_cc_exists(self, cc):
        with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'r') as file:
            data = json.load(file)
            if cc in data:
                return True
            return False
        
    def deposit(self, amount):
        if amount < 0:
            raise ValueError('Amount must be positive')
        else:
            self.balance += amount
        
    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError("You don\'t have enough money")
        else:
            self.balance -= amount

    def __str__(self):
        return f'CC: {self.cc}, name: {self.name}, balance: {self.balance}'
    
app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("home.html")

@app.route('/home', methods=['POST'])
def home():
    #return request.form.get('submit_button')
    if request.form.get('submit_button') == 'Yes, go to login':
        return render_template("login.html")
    elif request.form.get('submit_button') == 'No, go to registration':
        return render_template("registration.html")
    else:
        print("Error")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    #return f"{username} {password}"
    
    with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'r') as file:
        data = json.load(file)
        user_in_db = False
        for k,v in data.items():
            if v['name'] == username and v['password'] == password:
                user_in_db = True
                return redirect(url_for('success_log'))
        if not user_in_db:
            return redirect(url_for('failure_log'))
        
        
@app.route('/registration', methods=['POST'])
def registration():
    username = request.form.get('username')
    password = request.form.get('pass')
    password2 = request.form.get('pass2')
    cifra = request.form.get('deposit-amount')

    if password != password2:
        print("Passwords don't match")
        return redirect(url_for('failure_reg'))
    else:
        account = Account(username, password, cifra)
        
        account_json = {account.cc: {
            'name': account.name,
            'password': account.password,
            'balance': account.balance}}
        
        print('ciao ciao')
        with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'r') as file:
            data = json.load(file)
        data.update(account_json)
        with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'w') as file:
            json.dump(data, file)
        return redirect(url_for('success_reg'))

@app.route('/success_reg')
def success_reg():
    return render_template("login.html")

@app.route('/failure_reg')
def failure_reg():
    return "Registration failed!"

@app.route('/success_log')
def success_log():
    return "Login successful!"

@app.route('/failure_log')
def failure_log():
    return "Login failed!"

if __name__ == '__main__':
    app.run(use_reloader=True)