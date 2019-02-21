import sqlite3
from sqlite3 import Error

conn = sqlite3.connect(user.sqlite3)



def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
 
if __name__ == '__main__':
    create_connection("C:\\sqlite\db\pythonsqlite.db")



c = conn.cursor()