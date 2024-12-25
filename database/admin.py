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