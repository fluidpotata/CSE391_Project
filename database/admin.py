import sqlite3
import os
from time import strftime


def dbConnect():
    # return sqlite3.connect(os.getenv('DATABASE'))
    return sqlite3.connect('database/main.db')   


def getTickets():
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Tickets  ORDER BY status DESC")
    result = cursor.fetchall()
    connection.close()
    return result

def getCountTickets():
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM Tickets")
    result = cursor.fetchall()
    connection.close()
    return result


def closeTicket(ticketID):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Tickets SET status='Closed' WHERE reportID='{ticketID}'")
    connection.commit()
    connection.close()


def allocateUser(username, password, req_id, phone, room_id, name):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Users(username, password, role) VALUES('{username}', '{password}', 'user')")
    cursor.execute(f"SELECT userID FROM Users WHERE username='{username}'")
    userID = cursor.fetchone()[0]
    cursor.execute(f"INSERT INTO Tenants(name, phone, roomID, userID) VALUES('{name}', '{phone}', '{room_id}', '{userID}')")
    cursor.execute(f"DELETE FROM joinReqs WHERE requestID='{req_id}'")
    connection.commit()
    connection.close()


def getJoinReqs():
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM joinReqs")
    result = cursor.fetchall()
    connection.close()
    return result


def getAvailableRooms():
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Rooms WHERE status='Available'")
    result = cursor.fetchall()
    connection.close()
    return result


def generateBill():
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute("SELECT userID, tenantID FROM Tenants")
    tenant_ids = cursor.fetchall()
    
    for tenant_id in tenant_ids:
        cursor.execute(f"SELECT * FROM Bills WHERE userID='{tenant_id[0]}'")
        bills = cursor.fetchall()
        
        for bill in bills:
            cursor.execute(f"SELECT * FROM Payments WHERE tenantID='{tenant_id[1]}' AND month='{strftime('%Y-%m')}' AND payment='{bill[0]}'")
            existing_payment = cursor.fetchone()
            if not existing_payment:
                cursor.execute(f"INSERT INTO Payments(payment, tenantID, amount, month, status, transactionID, type) VALUES('{bill[0]}', '{tenant_id[1]}', '{bill[3]}', '{strftime('%Y-%m')}', 'unpaid', 'unpaid', '{bill[2]}')")
    
    connection.commit()
    connection.close()