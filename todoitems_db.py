import sqlite3
import os
import psycopg2
import psycopg2.extras
import urllib.parse

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class ToDoDB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            # "todoitems_db.db")
            # self.connection.row_factory = dict_factory
            # self.cursor = self.connection.cursor()
        )

        self.cursor = self.connection.cursor()


    def __del__(self):
        self.connection.close()

    def createToDoList(self, item):
        sql = "INSERT INTO todoitems (item) VALUES (%s)"
        self.cursor.execute(sql, [item])
        self.connection.commit()
        return

    def createUser(self, fname, lname, email, password):
        sql = "INSERT INTO users (fname, lname, email, password) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, [fname, lname, email, password])
        self.connection.commit()
        return

    def getUserByEmail(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = %s", (email))
        rows = self.cursor.fetchone()
        return rows

    def getAllToDoItems(self):
        self.cursor.execute('SELECT * FROM todoitems')
        return self.cursor.fetchall()

    def updateToDoList(self, item, id):
        sql = "UPDATE todoitems SET item = %s WHERE id = %s"
        self.cursor.execute(sql, [item, id])
        self.connection.commit()
        return

    def retrieveTodoitem(self, id):
            self.cursor.execute('SELECT * FROM todoitems WHERE id = %s', (id,))
            rows = self.cursor.fetchone()
            return rows

    def getTodo(self, id):
        sql = "SELECT * FROM todoitems WHERE id = %s"
        self.cursor.execute(sql, [id]) #make sure data is list
        return self.cursor.fetchone()

    def deleteTodoitem(self, id):
            self.cursor.execute('DELETE FROM todoitems WHERE id = %s', (id))
            self.connection.commit()
            return

    def createTodoitemsTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS todoitems (id SERIAL PRIMARY KEY, item TEXT)")
        self.connection.commit()

    def createUsersTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, fname VARCHAR(255), lname VARCHAR(255), email VARCHAR(255), password TEXT)")
        self.connection.commit()


# change imports
# init will be different.


