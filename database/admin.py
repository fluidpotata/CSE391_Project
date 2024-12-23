import sqlite3
import os

def dbConnect():
    return sqlite3.connect(os.getenv('DATABASE'))   

def getTickets():
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Tickets")
    result = cursor.fetchall()
    connection.close()
    return result

def getTicketUser(userid):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT username FROM Users WHERE id='{userid}'")
    result = cursor.fetchall()
    connection.close()
    return result