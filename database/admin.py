import sqlite3
import os

def dbConnect():
    return sqlite3.connect(os.getenv('DATABASE'))   

def getTickets():
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Tickets  ORDER BY status DESC")
    result = cursor.fetchall()
    connection.close()
    return result

def getTicketUser(userid):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT username FROM Users WHERE username='{userid}'")
    result = cursor.fetchall()
    connection.close()
    return result

def closeTicket(ticketID):
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Tickets SET status='Closed' WHERE reportID='{ticketID}'")
    connection.commit()
    connection.close()