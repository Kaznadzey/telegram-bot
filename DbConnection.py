import sqlite3


class DbConnection:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db.sqlite3', check_same_thread=False, timeout=10)

        return self.connection

    def close_connection(self):
        self.connection.close()
        self.connection = None
