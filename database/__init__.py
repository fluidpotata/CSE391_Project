import sqlite3
from database.user import *
import os
from dotenv import load_dotenv
load_dotenv()

def dbConnect():
    return sqlite3.connect(os.getenv('DATABASE'))
