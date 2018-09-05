import sqlite3


class DbConnection:
    def __init__(self):
        self.connection = sqlite3.connect('db.sqlite3', check_same_thread=False)

    def get_connection(self):
        return self.connection