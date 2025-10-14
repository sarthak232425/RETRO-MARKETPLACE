# reset_database.py - RUN THIS ONCE to completely reset
from models.database import db_instance

def reset_database():
    """COMPLETELY reset the database - DANGEROUS but fixes everything"""
    db = db_instance.db
    print("🧨 NUKING database...")
    # Delete everything
    db.games.delete_many({})
    db.sellers.delete_many({})
    db.consoles.delete_many({})
    print("✅ Database reset complete!")
    print("🔄 Restart your Flask app to get clean sample data")

if __name__ == "__main__":
    confirm = input("❌ This will DELETE ALL DATA. Type 'YES' to continue: ")
    if confirm == "YES":
        reset_database()
    else:
        print("🚫 Cancelled")
