from pymongo import MongoClient

class Database:
    def __init__(self, uri: str, dbName: str):
        self.client = MongoClient(uri)
        self.dbName = dbName
        self.db = self.client[self.dbName]

    def get_collection(self, colName: str):
        col = self.db[colName]
        return col

# initialize the database intance
db_intance = Database('mongodb://10.1.55.230:27017', "BLE")