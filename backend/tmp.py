from sqlalchemy import create_engine

engine = create_engine("sqlite://database/main.db")
connection = engine.raw_connection()
try:
    # Get a SQLite cursor from the connection
    cursor = connection.cursor()
    # Execute the ATTACH DATABASE command
    cursor.execute("ATTACH DATABASE ':memory:' AS party_master")
    # Commit the transaction
    connection.commit()
finally:
    # Close the connection
    connection.close()