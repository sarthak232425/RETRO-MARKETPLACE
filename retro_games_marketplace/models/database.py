# models/database.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import Config
import sys

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        try:
            print("🔄 Attempting to connect to MongoDB Atlas...")
            self.client = MongoClient(Config.MONGODB_URI, serverSelectionTimeoutMS=5000)
            
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client[Config.DATABASE_NAME]
            
            print("✅ Successfully connected to MongoDB Atlas!")
            print(f"📊 Database: {Config.DATABASE_NAME}")
            
        except ServerSelectionTimeoutError as e:
            print(f"❌ MongoDB connection timeout: {e}")
            print("💡 Please check your:")
            print("   - Internet connection")
            print("   - MongoDB Atlas connection string")
            print("   - IP whitelist in MongoDB Atlas")
            sys.exit(1)
        except ConnectionFailure as e:
            print(f"❌ MongoDB connection failed: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)

    def get_db(self):
        return self.db

    def close_connection(self):
        if self.client:
            self.client.close()
            print("🔌 MongoDB connection closed")

# Create global instance
db_instance = Database()