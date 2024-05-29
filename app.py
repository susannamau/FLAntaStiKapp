from flask import Flask, render_template, redirect, url_for, request, session
import json
import random
import string

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
            with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'r') as file:
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
            with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'r') as file:
                data = json.load(file)
            data[self.username]['balance'] = self.balance
            with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'w') as file:
                json.dump(data, file)
        return self
        
    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError("You don\'t have enough money")
        else:
            self.balance -= amount
            with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'r') as file:
                data = json.load(file)
            data[self.username]['balance'] = self.balance
            with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'w') as file:
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
    
app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("home.html")

@app.route('/home', methods=['POST', 'GET'])
def home():
    #return request.form.get('submit_button')
    if request.form.get('submit_button') == 'Yes, go to login':
        return render_template("login.html")
    elif request.form.get('submit_button') == 'No, go to registration':
        return render_template("registration.html")
    else:
        print("Error")

@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    #return f"{username} {password}"
    
    with open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'r') as file:
        data = json.load(file)
        user_in_db = False
        for k,v in data.items():
            if k == username and v['password'] == password:
                user = Account(username, password, v['balance'], v['cc'])
                user_in_db = True
                session['user'] = user.serialize()
                print(session['user'])
                return redirect(url_for('dashboard'))
                #return redirect(url_for('success_log'))
        if not user_in_db:
            return redirect(url_for('failure_log'))
        
        
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    username = request.form.get('username')
    password = request.form.get('pass')
    password2 = request.form.get('pass2')
    cifra = request.form.get('deposit-amount')

    if password != password2:
        print("Passwords don't match")
        return redirect(url_for('failure_reg'))
    elif username in json.load(open('/Users/susannamau/Dev/BPER/Python/webapp/data.json', 'r')):
        print("Username already exists")
        return redirect(url_for('failure_reg'))
    else:
        account = Account(username, password, cifra)
        
        account_json = {account.username: {
            'cc': account.cc,
            'password': account.password,
            'balance': account.balance}}
        
        #print('ciao ciao')
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
    return "Login successful!" #"redirect(url_for('dashboard'))

@app.route('/failure_log')
def failure_log():
    return "Login failed!"
    
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    utente = Account.deserialize(session['user'])
    print(utente)
    what = request.form.get('what_to_do')
    if request.method == 'GET' or what is None:
        return render_template("dashboard.html", user=utente)
    if what == 'Deposita':
        u = utente.deposit(float(request.form.get('amount')))
        session['user'] = u.serialize()
        utente = u
        return render_template("dashboard.html", user=utente)  
    elif what == 'Preleva':
        u = utente.withdraw(float(request.form.get('amount')))
        session['user'] = u.serialize()
        utente = u
        return render_template("dashboard.html", user=utente)
    
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user', None)
    return render_template("login.html")


if __name__ == '__main__':
    app.secret_key = 'tettedisusi'
    app.run(use_reloader=True)


    