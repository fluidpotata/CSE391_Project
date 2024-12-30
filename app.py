from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from dotenv import load_dotenv
load_dotenv()

from database import *

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
            session['user'] = username
            session['role'] = 'admin'
            session['id'] = adminStat
            return redirect(url_for('admin'))
        elif userStat:
            session['user'] = username
            session['role'] = 'user'
            session['id'] = userStat
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
        phone = request.form['phone']
        password = request.form['password']
        cpassword = request.form['confirm_password']
        room = request.form['room_type']
        if password != cpassword:
            return render_template('signup.html', error="Password doesn't match")   
        if ifUserExists(username):
            return render_template('signup.html', error="Username taken! Try another username.")
        joinReq(name, room, phone, username, password)
        return redirect(url_for('login'))


@app.route('/admin')
def admin():
    flash = session.get('flash')
    session['flash'] = None
    return render_template('admin.html', data={'tickets':getTickets(), 'count':getCountTickets(), 'flash': flash, 'joinreqs':getJoinReqsCount()})


@app.route('/customer')
def customer():
    userID = session['id']
    data = {'username': session['user'],'package':getPackage(userID),'bill': getBillStatus(userID),'internetbill':getInternetBillStatus(userID), 'utilitybill': getUtilityBillStatus(userID), 'ticketCount':getTicketCount(userID)}
    return render_template('customer.html', data=data)


@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if session['user']=='admin':
        return redirect(url_for('ticketadmin'))
    if request.method == 'GET':
        return render_template('ticket.html', info=getTicketUser(session.get('user')))
    
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        createTicket(getUserID(session.get('user')), category, description)
        return redirect(url_for('ticket'))


@app.route('/seeapps', methods=['GET', 'POST'])
def seeApps():
    if session['user']=='admin':
        if request.method == 'POST':
            req_id = request.form['req_id']
            room_id = request.form['room_id']
            name = request.form['name']
            phone = request.form['phone']
            username = request.form['username']
            password = request.form['password']
            allocateUser(username, password, req_id, phone, room_id, name)
            return redirect(url_for('seeApps'))
        else:
            data = getJoinReqs()
            available_rooms = getAvailableRooms()
            return render_template('applications.html', data=data, available_rooms=available_rooms)
    else:
        return redirect(url_for('customer'))


@app.route('/ticketadmin', methods=['GET', 'POST'])
def ticketadmin():
    if session['user']=='admin':
        if request.method == 'POST':
            reportID = request.form['ticket_id']
            closeTicket(reportID)
            return redirect(url_for('ticketadmin'))
        else:
            info = getTickets()
            return render_template('ticketadmin.html', tickets=info)
    else:
        return redirect(url_for('ticket'))



@app.route('/generatebill')
def generatebill():
    generateBill()
    return redirect(url_for('admin'))


@app.route('/paybill', methods=['GET', 'POST'])
def paybill():
    if request.method == 'POST':
        tenantid = request.form['tenantid']
        bill = request.form['bill']
        tid = request.form['tID']
        payBill(tenantid, bill, tid)
        return redirect(url_for('paybill'))
    else:
        return render_template('billpay.html', data=getBills(session.get('id')))






@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)