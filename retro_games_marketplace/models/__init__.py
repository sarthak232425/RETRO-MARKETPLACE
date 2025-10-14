# models/__init__.py
from .collections import games_db, sellers_db, consoles_db
from .database import db_instance
from bson.objectid import ObjectId
from datetime import datetime
import hashlib

_SAMPLE_DATA_INITIALIZED = False

def init_sample_data():
    global _SAMPLE_DATA_INITIALIZED
    
    if _SAMPLE_DATA_INITIALIZED:
        print("✅ Sample data already initialized")
        return
    
    try:
        db = db_instance.db
        
        print("🔍 Checking database state...")
        
        existing_games = db.games.count_documents({})
        existing_sellers = db.sellers.count_documents({})
        existing_consoles = db.consoles.count_documents({})
        
        print(f"📊 Current: {existing_games} games, {existing_sellers} sellers, {existing_consoles} consoles")
        
        if existing_games > 0 or existing_sellers > 0:
            print("✅ Database already has data, skipping initialization")
            _SAMPLE_DATA_INITIALIZED = True
            return
        
        print("🚀 Initializing fresh sample data...")
        
        if existing_consoles == 0:
            consoles = [
                {"name": "Nintendo Entertainment System"},
                {"name": "Super Nintendo"}, 
                {"name": "Nintendo 64"},
                {"name": "GameCube"},
                {"name": "Sega Genesis"},
                {"name": "Sega Saturn"},
                {"name": "Sega Dreamcast"},
                {"name": "PlayStation"},
                {"name": "PlayStation 2"},
                {"name": "Game Boy"},
                {"name": "Game Boy Advance"}
            ]
            db.consoles.insert_many(consoles)
            print(f"✅ Added {len(consoles)} consoles")
        else:
            print("✅ Consoles already exist")

        console_map = {console["name"]: console["_id"] for console in db.consoles.find()}
        
        all_sellers = [
            {
                "username": "retro_gamer",
                "email": "retro@example.com",
                "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
                "rating": 4.8,
                "total_sales": 42,
                "member_since": datetime.now(),
                "location": "Mumbai, India",
                "bio": "Professional retro game collector. All games tested and guaranteed working.",
                "shipping_info": "Free shipping across Maharashtra",
                "response_time": "Within 2 hours",
                "contact_number": "+91 98765 43210"
            },
            {
                "username": "classic_collector", 
                "email": "collector@example.com",
                "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
                "rating": 4.9,
                "total_sales": 67,
                "member_since": datetime.now(),
                "location": "Delhi, India", 
                "bio": "Vintage gaming enthusiast since the 90s. Focus on rare and sealed games.",
                "shipping_info": "Free shipping in Delhi",
                "response_time": "Within 1 hour",
                "contact_number": "+91 97654 32109"
            },
            {
                "username": "solapur_retro",
                "email": "solapur@example.com",
                "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
                "rating": 4.7,
                "total_sales": 31,
                "member_since": datetime.now(),
                "location": "Solapur, Maharashtra",
                "bio": "Solapur's trusted retro game seller. Specializing in Sega and PlayStation classics.",
                "shipping_info": "Free shipping in Solapur",
                "response_time": "Within 2 hours",
                "contact_number": "+91 91234 56789"
            },
            {
                "username": "kolhapur_gamer",
                "email": "kolhapur@example.com",
                "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
                "rating": 4.9,
                "total_sales": 54,
                "member_since": datetime.now(),
                "location": "Kolhapur, Maharashtra",
                "bio": "Rare finds and collector's items from Kolhapur. Fast shipping and great deals.",
                "shipping_info": "Free shipping in Kolhapur",
                "response_time": "Within 1 hour",
                "contact_number": "+91 92345 67890"
            },
            {
                "username": "nagpur_gamer",
                "email": "nagpur@example.com",
                "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
                "rating": 4.6,
                "total_sales": 40,
                "member_since": datetime.now(),
                "location": "Nagpur, Maharashtra",
                "bio": "Nagpur's retro gaming expert. Specializing in Nintendo and Sega.",
                "shipping_info": "Free shipping in Nagpur",
                "response_time": "Within 3 hours",
                "contact_number": "+91 93456 78901"
            },
            {
                "username": "amravati_retro",
                "email": "amravati@example.com",
                "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
                "rating": 4.8,
                "total_sales": 29,
                "member_since": datetime.now(),
                "location": "Amravati, Maharashtra",
                "bio": "Amravati's best source for PlayStation and Sega classics.",
                "shipping_info": "Free shipping in Amravati",
                "response_time": "Within 2 hours",
                "contact_number": "+91 94567 89012"
            },
            {
                "username": "jalgaon_gamer",
                "email": "jalgaon@example.com",
                "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
                "rating": 4.7,
                "total_sales": 37,
                "member_since": datetime.now(),
                "location": "Jalgaon, Maharashtra",
                "bio": "Jalgaon's retro gaming hub. Specializing in rare finds and collector's items.",
                "shipping_info": "Free shipping in Jalgaon",
                "response_time": "Within 1 hour",
                "contact_number": "+91 95678 90123"
            }
        ]
        
        db.sellers.insert_many(all_sellers)
        print(f"✅ Added {len(all_sellers)} sellers")

        seller_map = {seller["username"]: seller["_id"] for seller in db.sellers.find()}
        
        all_games = [
            {
                "title": "Super Mario Bros. 3",
                "console_id": console_map["Nintendo Entertainment System"],
                "condition": "Excellent",
                "rarity": "Common",
                "price": 2499,
                "description": "Complete in box with manual. Tested and working.",
                "seller_id": seller_map["retro_gamer"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "The Legend of Zelda: Ocarina of Time", 
                "console_id": console_map["Nintendo 64"],
                "condition": "Good",
                "rarity": "Uncommon", 
                "price": 4199,
                "description": "Gold cartridge version. Some label wear but plays perfectly.",
                "seller_id": seller_map["classic_collector"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Final Fantasy VII",
                "console_id": console_map["PlayStation"], 
                "condition": "Excellent",
                "rarity": "Uncommon",
                "price": 3499,
                "description": "Complete with all 3 discs and manual in great condition.",
                "seller_id": seller_map["retro_gamer"], 
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Sonic the Hedgehog 2",
                "console_id": console_map["Sega Genesis"],
                "condition": "Mint", 
                "rarity": "Common",
                "price": 1899,
                "description": "Complete in box. Like new condition with manual.",
                "seller_id": seller_map["classic_collector"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Super Mario World",
                "console_id": console_map["Super Nintendo"],
                "condition": "Excellent",
                "rarity": "Common", 
                "price": 2999,
                "description": "Complete in box. Tested and working perfectly.",
                "seller_id": seller_map["retro_gamer"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Resident Evil 2",
                "console_id": console_map["PlayStation"],
                "condition": "Excellent",
                "rarity": "Rare",
                "price": 2999, 
                "description": "Dual Shock version. Complete with both discs and manual.",
                "seller_id": seller_map["classic_collector"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Pokemon Red Version",
                "console_id": console_map["Game Boy"],
                "condition": "Excellent",
                "rarity": "Rare",
                "price": 3999,
                "description": "Original cartridge, tested and working. Ships from Solapur.",
                "seller_id": seller_map["solapur_retro"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Crash Bandicoot",
                "console_id": console_map["PlayStation"],
                "condition": "Mint",
                "rarity": "Uncommon",
                "price": 2499,
                "description": "Complete in box, like new. Ships from Kolhapur.",
                "seller_id": seller_map["kolhapur_gamer"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "FIFA 07",
                "console_id": console_map["PlayStation 2"],
                "condition": "Good",
                "rarity": "Common",
                "price": 799,
                "description": "Disc only, works perfectly. Ships from Kolhapur.",
                "seller_id": seller_map["kolhapur_gamer"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Super Mario Land",
                "console_id": console_map["Game Boy"],
                "condition": "Excellent",
                "rarity": "Uncommon",
                "price": 2999,
                "description": "Classic platformer, tested and working. Ships from Jalgaon.",
                "seller_id": seller_map["jalgaon_gamer"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Virtua Fighter 2",
                "console_id": console_map["Sega Saturn"],
                "condition": "Mint",
                "rarity": "Rare",
                "price": 3499,
                "description": "Complete in box, like new. Ships from Amravati.",
                "seller_id": seller_map["amravati_retro"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Gran Turismo",
                "console_id": console_map["PlayStation"],
                "condition": "Excellent",
                "rarity": "Common",
                "price": 1599,
                "description": "Complete with manual, tested and working. Ships from Nagpur.",
                "seller_id": seller_map["nagpur_gamer"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Street Fighter Alpha 3",
                "console_id": console_map["PlayStation"],
                "condition": "Good",
                "rarity": "Uncommon",
                "price": 1899,
                "description": "Disc only, works perfectly. Ships from Solapur.",
                "seller_id": seller_map["solapur_retro"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Sonic Adventure",
                "console_id": console_map["Sega Dreamcast"],
                "condition": "Excellent",
                "rarity": "Rare",
                "price": 2999,
                "description": "Complete in box, tested and working. Ships from Amravati.",
                "seller_id": seller_map["amravati_retro"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Tekken Tag Tournament",
                "console_id": console_map["PlayStation 2"],
                "condition": "Mint",
                "rarity": "Uncommon",
                "price": 2199,
                "description": "Complete in box, like new. Ships from Jalgaon.",
                "seller_id": seller_map["jalgaon_gamer"],
                "date_listed": datetime.now(),
                "images": []
            },
            {
                "title": "Metal Gear Solid",
                "console_id": console_map["PlayStation"],
                "condition": "Excellent",
                "rarity": "Rare",
                "price": 2799,
                "description": "Complete with manual, tested and working. Ships from Kolhapur.",
                "seller_id": seller_map["kolhapur_gamer"],
                "date_listed": datetime.now(),
                "images": []
            }
        ]
        
        db.games.insert_many(all_games)
        print(f"✅ Added {len(all_games)} games")
        
        _SAMPLE_DATA_INITIALIZED = True
        print("🎮 Sample data initialization COMPLETE!")
        print(f"📊 Final counts: {db.games.count_documents({})} games, {db.sellers.count_documents({})} sellers")
        
    except Exception as e:
        print(f"❌ Error in sample data: {e}")