# models/collections.py
from .database import db_instance
from bson.objectid import ObjectId
from datetime import datetime
import hashlib
import secrets

class GameCollection:
    def __init__(self):
        self.collection = db_instance.db.games

    def get_all_games(self):
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": "consoles",
                        "localField": "console_id",
                        "foreignField": "_id",
                        "as": "console"
                    }
                },
                {
                    "$lookup": {
                        "from": "sellers",
                        "localField": "seller_id",
                        "foreignField": "_id",
                        "as": "seller"
                    }
                },
                {
                    "$unwind": "$console"
                },
                {
                    "$unwind": "$seller"
                },
                {
                    "$sort": {"date_listed": -1}
                }
            ]
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print(f"Error getting games: {e}")
            return []

    def get_game_by_id(self, game_id):
        try:
            pipeline = [
                {
                    "$match": {"_id": ObjectId(game_id)}
                },
                {
                    "$lookup": {
                        "from": "consoles",
                        "localField": "console_id",
                        "foreignField": "_id",
                        "as": "console"
                    }
                },
                {
                    "$lookup": {
                        "from": "sellers",
                        "localField": "seller_id",
                        "foreignField": "_id",
                        "as": "seller"
                    }
                },
                {
                    "$unwind": "$console"
                },
                {
                    "$unwind": "$seller"
                }
            ]
            result = list(self.collection.aggregate(pipeline))
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting game {game_id}: {e}")
            return None

    def add_game(self, game_data):
        try:
            result = self.collection.insert_one(game_data)
            return result
        except Exception as e:
            print(f"Error adding game: {e}")
            return None

    def search_games(self, filters):
        try:
            query = {}
            if filters.get('console'):
                # Ensure ObjectId conversion for console filter
                try:
                    query['console_id'] = ObjectId(filters['console'])
                except Exception:
                    query['console_id'] = filters['console']
            if filters.get('condition'):
                query['condition'] = filters['condition']
            if filters.get('rarity'):
                query['rarity'] = filters['rarity']
            pipeline = [
                {"$match": query},
                {
                    "$lookup": {
                        "from": "consoles",
                        "localField": "console_id",
                        "foreignField": "_id",
                        "as": "console"
                    }
                },
                {
                    "$lookup": {
                        "from": "sellers",
                        "localField": "seller_id",
                        "foreignField": "_id",
                        "as": "seller"
                    }
                },
                {"$unwind": "$console"},
                {"$unwind": "$seller"},
                {"$sort": {"date_listed": -1}}
            ]
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print(f"Error searching games: {e}")
            return []

    def add_game_image(self, game_id, filename):
        """Add image filename to game document"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(game_id)},
                {"$push": {"images": filename}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error adding image to game: {e}")
            return False

    def set_primary_image(self, game_id, filename):
        """Set primary image for game"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(game_id)},
                {"$set": {"primary_image": filename}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error setting primary image: {e}")
            return False

    def remove_game_image(self, game_id, filename):
        """Remove image from game"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(game_id)},
                {"$pull": {"images": filename}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error removing image from game: {e}")
            return False

    def is_game_owner(self, game_id, seller_id):
        """Check if seller owns this game"""
        try:
            game = self.collection.find_one({
                "_id": ObjectId(game_id),
                "seller_id": ObjectId(seller_id)
            })
            return game is not None
        except Exception as e:
            print(f"Error checking game ownership: {e}")
            return False

class SellerCollection:
    def __init__(self):
        self.collection = db_instance.db.sellers

    def get_all_sellers(self):
        try:
            return list(self.collection.find().sort("rating", -1))
        except Exception as e:
            print(f"Error getting sellers: {e}")
            return []

    def get_seller_by_id(self, seller_id):
        try:
            if isinstance(seller_id, str):
                seller_id = ObjectId(seller_id)
            return self.collection.find_one({"_id": seller_id})
        except Exception as e:
            print(f"Error getting seller {seller_id}: {e}")
            return None

    def get_seller_games(self, seller_id):
        try:
            pipeline = [
                {
                    "$match": {"seller_id": ObjectId(seller_id)}
                },
                {
                    "$lookup": {
                        "from": "consoles",
                        "localField": "console_id",
                        "foreignField": "_id",
                        "as": "console"
                    }
                },
                {
                    "$unwind": "$console"
                },
                {
                    "$sort": {"date_listed": -1}
                }
            ]
            games_collection = db_instance.db.games
            return list(games_collection.aggregate(pipeline))
        except Exception as e:
            print(f"Error getting seller games: {e}")
            return []

    def get_seller_by_username(self, username):
        """Get seller by username"""
        try:
            return self.collection.find_one({"username": username})
        except Exception as e:
            print(f"Error getting seller by username: {e}")
            return None

    def create_seller(self, seller_data):
        """Create new seller with hashed password"""
        try:
            # Hash password
            if 'password' in seller_data:
                salt = secrets.token_hex(16)
                password_hash = hashlib.sha256((seller_data['password'] + salt).encode()).hexdigest()
                seller_data['password_hash'] = password_hash
                seller_data['password_salt'] = salt
                del seller_data['password']
            
            seller_data.setdefault('rating', 5.0)
            seller_data.setdefault('total_sales', 0)
            seller_data.setdefault('member_since', datetime.now())
            
            result = self.collection.insert_one(seller_data)
            return result.inserted_id
        except Exception as e:
            print(f"Error creating seller: {e}")
            return None

    def verify_password(self, seller_id, password):
        """Verify seller password"""
        try:
            seller = self.get_seller_by_id(seller_id)
            if not seller or 'password_hash' not in seller:
                return False
            
            password_hash = hashlib.sha256((password + seller['password_salt']).encode()).hexdigest()
            return password_hash == seller['password_hash']
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False

    def update_seller_profile(self, seller_id, update_data):
        """Update seller profile information"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(seller_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating seller profile: {e}")
            return False

class ConsoleCollection:
    def __init__(self):
        self.collection = db_instance.db.consoles

    def get_all_consoles(self):
        try:
            return list(self.collection.find().sort("name", 1))
        except Exception as e:
            print(f"Error getting consoles: {e}")
            return []

    def get_console_by_id(self, console_id):
        try:
            if isinstance(console_id, str):
                console_id = ObjectId(console_id)
            return self.collection.find_one({"_id": console_id})
        except Exception as e:
            print(f"Error getting console by ID: {e}")
            return None

    def add_console(self, console_data):
        try:
            result = self.collection.insert_one(console_data)
            return result.inserted_id
        except Exception as e:
            print(f"Error adding console: {e}")
            return None

# Initialize collections
games_db = GameCollection()
sellers_db = SellerCollection()
consoles_db = ConsoleCollection()