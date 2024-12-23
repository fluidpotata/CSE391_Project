from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from dotenv import load_dotenv
load_dotenv()
from database import *



load_dotenv()

app = Flask(__name__)
app.secret_key = "AstrongSEcretKey"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        adminStat = isAdmin(username, password)
        userStat = isAuthenticated(username, password)
        if adminStat:
            return redirect(url_for('admin'))
        elif userStat:
            session['user'] = username
            return redirect(url_for('customer'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if 'username' in session:
            if isAdmin(session['username']):
                return redirect(url_for('admin'))
            return redirect(url_for('dashboard'))
        else:
            return render_template('signup.html')
    elif request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']
        cpassword = request.form['confirm_password']
        if password != cpassword:
            return render_template('signup.html', error="Password doesn't match")   
        if ifUserExists(username):
            return render_template('signup.html', error="Username taken! Try another username.")
        clientRegister(name, address, phone, username, password)
        return redirect(url_for('login'))


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if isAdmin():
        if request.method == 'POST':
            pass
        else:
            info = getTickets()
            return render_template('ticketadmin.html', info=info)
    else:
        if request.method == 'GET':
            return render_template('ticket.html', info=getTicketUser(session.get('username')))
        
        if request.method == 'POST':
            pass

if __name__ == '__main__':
    app.run(debug=True)