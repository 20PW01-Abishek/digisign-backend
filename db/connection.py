# db/connection.py
from pymongo import MongoClient

class DatabaseConnection:
    _instance = None

    def __init__(self, uri):
        if not self._instance:
            self.client = MongoClient(uri)
            DatabaseConnection._instance = self
        else:
            self.client = self._instance.client

    def close(self):
        if self.client:
            self.client.close()

    def get_connection(self):
        return self.client