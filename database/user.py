import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
from time import strftime
from admin import pullFromDB, pushToDB

def dbConnect():
    return sqlite3.connect('database/main.db')


def isAdmin(username, password):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Users WHERE username='{username}' AND password='{password}' AND role='admin'")
    result = cursor.fetchall()
    connection.close()
    if len(result)>0:
        return result[0][0]
    return False


def isAuthenticated(username, password):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Users WHERE username='{username}' AND password='{password}'")
    result = cursor.fetchall()
    connection.close()
    if len(result)>0:
        return result[0][0]
    return False


def ifUserExists(username):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Users WHERE username='{username}'")
    result = cursor.fetchall()
    connection.close()
    if len(result)>0:
        return True
    return False


def clientRegister(name, address, phone, username, password):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Users(username, password) VALUES('{username}', '{password}')")
    cursor.execute(f"SELECT userID FROM Users WHERE username='{username}'")
    userID = cursor.fetchone()[0]
    cursor.execute(f"INSERT INTO Tenants(name, phone, userID) VALUES('{name}', '{phone}', '{userID}')")
    connection.commit()
    connection.close()
    return 

def getUserID(username):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT userID FROM Users WHERE username='{username}'")
    userID = cursor.fetchone()[0]
    connection.close()
    return userID



def createTicket(uesrID,category,description):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT tenantID FROM Tenants WHERE userID='{uesrID}'")
    uesrID = cursor.fetchone()[0]
    cursor.execute(f"INSERT INTO Tickets(tenantID, category, Description, status) VALUES('{uesrID}', '{category}', '{description}', 'Open')")
    connection.commit()
    connection.close()
    

def getTicketUser(userid):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT username FROM Users WHERE username='{userid}'")
    result = cursor.fetchall()
    connection.close()
    return result


def getTicketUserCount(userid):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM Tickets WHERE tenantID='{userid}'")
    result = cursor.fetchall()
    connection.close()
    return result

def joinReq(name, room, phone, username, password):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO joinReqs(name, roomChoice, phone, username, password) VALUES('{name}', '{room}', '{phone}', '{username}', '{password}')")
    connection.commit()
    connection.close()
    return


def getJoinReqsCount():
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM joinReqs")
    result = cursor.fetchall()[0][0]
    connection.close()
    return result


def getTicketCount(tenantID):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM Tickets WHERE tenantID='{tenantID}' and status='Open'")
    result = cursor.fetchall()[0][0]
    connection.close()
    return result


def getPackage(tenantID):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT roomID FROM Tenants WHERE userID='{tenantID}'")
    roomID = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT type FROM Rooms WHERE roomID='{roomID}'")
    result = cursor.fetchall()[0][0]
    connection.close()
    return result


def getBills(userID):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT tenantID FROM Tenants WHERE userID='{userID}'")
    tenantID = cursor.fetchone()[0]
    cursor.execute(f"SELECT * FROM Payments WHERE tenantID='{tenantID}' AND status='unpaid'")
    result = cursor.fetchall()
    connection.close()
    return result


def payBill(tenantid, pid, tid):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Payments SET status='paid', transactionID='{tid}' WHERE tenantID='{tenantid}' AND paymentID='{pid}'")
    connection.commit()
    connection.close()
    return


def getBillStatus(userID):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT tenantID FROM Tenants WHERE userID='{userID}'")
    tenantID = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM Payments WHERE status='unpaid' AND month='{strftime('%Y-%m')}' AND type='rent' AND tenantID='{tenantID}'")
    result = cursor.fetchall()[0][0]
    connection.close()
    return result==0


def getInternetBillStatus(userID):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT tenantID FROM Tenants WHERE userID='{userID}'")
    tenantID = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM Payments WHERE status='unpaid' AND month='{strftime('%Y-%m')}' AND type='internet' AND tenantID='{tenantID}'")
    result = cursor.fetchall()[0][0]
    connection.close()
    return result==0


def getUtilityBillStatus(userID):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT tenantID FROM Tenants WHERE userID='{userID}'")
    tenantID = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM Payments WHERE status='unpaid' AND month='{strftime('%Y-%m')}' AND type='utility' AND tenantID='{tenantID}'")
    result = cursor.fetchall()[0][0]
    connection.close()
    return result==0