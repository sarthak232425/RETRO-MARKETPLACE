# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.collections import games_db, sellers_db, consoles_db
from models import init_sample_data
from utils.image_utils import image_handler
from bson.objectid import ObjectId
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# Authentication helpers - FIXED
def get_current_seller():
    seller_id = session.get('seller_id')
    if seller_id:
        try:
            seller = sellers_db.get_seller_by_id(seller_id)
            return seller
        except Exception as e:
            print(f"❌ Error getting seller: {e}")
            session.pop('seller_id', None)
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_seller = get_current_seller()
        if not current_seller:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize database
with app.app_context():
    init_sample_data()

@app.route('/')
def index():
    try:
        games = games_db.get_all_games()
        featured_games = games[:6]
        current_seller = get_current_seller()
        return render_template('index.html', 
                             featured_games=featured_games,
                             current_seller=current_seller)
    except Exception as e:
        flash(f"Error loading games: {str(e)}", "error")
        return render_template('index.html', featured_games=[], current_seller=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')
        
        seller = sellers_db.get_seller_by_username(username)
        if seller and sellers_db.verify_password(seller['_id'], password):
            session['seller_id'] = str(seller['_id'])
            flash(f'Welcome back, {seller["username"]}!', 'success')
            return redirect(url_for('seller_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    if session.get('seller_id'):
        return redirect(url_for('seller_dashboard'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        location = request.form.get('location', '')
        
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('register.html')
        
        if sellers_db.get_seller_by_username(username):
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        seller_data = {
            'username': username,
            'email': email,
            'password': password,
            'location': location,
            'rating': 5.0,
            'total_sales': 0,
            'member_since': datetime.now()
        }
        
        seller_id = sellers_db.create_seller(seller_data)
        if seller_id:
            session['seller_id'] = str(seller_id)
            flash('Account created successfully!', 'success')
            return redirect(url_for('seller_dashboard'))
        else:
            flash('Error creating account', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('seller_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/seller/dashboard')
@login_required
def seller_dashboard():
    current_seller = get_current_seller()
    seller_games = sellers_db.get_seller_games(str(current_seller['_id']))
    
    return render_template('seller_dashboard.html',
                         seller=current_seller,
                         games=seller_games,
                         current_seller=current_seller)

@app.route('/seller/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_seller_profile():
    current_seller = get_current_seller()
    
    if request.method == 'POST':
        try:
            update_data = {
                "location": request.form.get('location', ''),
                "bio": request.form.get('bio', ''),
                "shipping_info": request.form.get('shipping_info', ''),
                "response_time": request.form.get('response_time', ''),
                "contact_number": request.form.get('contact_number', '')
            }
            
            result = sellers_db.collection.update_one(
                {"_id": ObjectId(current_seller['_id'])},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                flash('Profile updated successfully!', 'success')
            else:
                flash('No changes made to your profile', 'info')
                
            return redirect(url_for('seller_dashboard'))
                
        except Exception as e:
            flash(f'Error updating profile: {str(e)}', 'error')
    
    return render_template('edit_seller_profile.html', 
                         seller=current_seller,
                         current_seller=current_seller)

@app.route('/games')
def games():
    try:
        console_filter = request.args.get('console')
        condition_filter = request.args.get('condition')
        rarity_filter = request.args.get('rarity')
        
        filters = {}
        if console_filter:
            filters['console'] = console_filter
        if condition_filter:
            filters['condition'] = condition_filter
        if rarity_filter:
            filters['rarity'] = rarity_filter
        
        if filters:
            games_list = games_db.search_games(filters)
        else:
            games_list = games_db.get_all_games()
        
        consoles = consoles_db.get_all_consoles()
        conditions = ["Mint", "Excellent", "Good", "Fair", "Poor"]
        rarities = ["Common", "Uncommon", "Rare", "Very Rare", "Ultra Rare"]
        current_seller = get_current_seller()
        
        return render_template('games.html', 
                             games=games_list, 
                             consoles=consoles,
                             conditions=conditions,
                             rarities=rarities,
                             current_filters=filters,
                             current_seller=current_seller)
    except Exception as e:
        flash(f"Error loading games: {str(e)}", "error")
        return render_template('games.html', games=[], consoles=[], conditions=[], rarities=[], current_filters={}, current_seller=None)

@app.route('/game/<game_id>')
def game_detail(game_id):
    game = games_db.get_game_by_id(game_id)
    if not game:
        flash('Game not found', 'error')
        return redirect(url_for('games'))
    
    current_seller = get_current_seller()
    is_owner = current_seller and games_db.is_game_owner(game_id, current_seller['_id'])
    
    return render_template('game_detail.html', 
                         game=game, 
                         current_seller=current_seller,
                         is_owner=is_owner)

@app.route('/add-game', methods=['GET', 'POST'])
@login_required
def add_game():
    current_seller = get_current_seller()
    
    if request.method == 'POST':
        try:
            image_filenames = []
            if 'images' in request.files:
                images = request.files.getlist('images')
                for image in images:
                    if image and image.filename:
                        filename, error = image_handler.save_image(image)
                        if error:
                            flash(f'Image upload error: {error}', 'warning')
                        elif filename:
                            image_filenames.append(filename)
            
            game_data = {
                "title": request.form['title'],
                "console_id": ObjectId(request.form['console_id']),
                "condition": request.form['condition'],
                "rarity": request.form['rarity'],
                "price": float(request.form['price']),
                "description": request.form['description'],
                "seller_id": ObjectId(current_seller['_id']),
                "date_listed": datetime.now(),
                "images": image_filenames
            }
            
            result = games_db.add_game(game_data)
            if result.inserted_id:
                flash('Game added successfully!', 'success')
                return redirect(url_for('seller_dashboard'))
            else:
                flash('Failed to add game to database', 'error')
                
        except Exception as e:
            flash(f'Error adding game: {str(e)}', 'error')
    
    consoles = consoles_db.get_all_consoles()
    conditions = ["Mint", "Excellent", "Good", "Fair", "Poor"]
    rarities = ["Common", "Uncommon", "Rare", "Very Rare", "Ultra Rare"]
    
    return render_template('add_game.html', 
                         consoles=consoles,
                         conditions=conditions,
                         rarities=rarities,
                         current_seller=current_seller)

@app.route('/game/<game_id>/add-images', methods=['POST'])
@login_required
def add_game_images(game_id):
    current_seller = get_current_seller()
    
    if not games_db.is_game_owner(game_id, current_seller['_id']):
        flash('You can only add images to your own games', 'error')
        return redirect(url_for('game_detail', game_id=game_id))
    
    try:
        game = games_db.get_game_by_id(game_id)
        if not game:
            flash('Game not found', 'error')
            return redirect(url_for('games'))
        
        image_filenames = []
        if 'images' in request.files:
            images = request.files.getlist('images')
            for image in images:
                if image and image.filename:
                    filename, error = image_handler.save_image(image)
                    if error:
                        flash(f'Image error: {error}', 'warning')
                    elif filename:
                        image_filenames.append(filename)
        
        if image_filenames:
            success_count = 0
            for filename in image_filenames:
                if games_db.add_game_image(game_id, filename):
                    success_count += 1
            
            flash(f'Added {success_count} image(s) successfully!', 'success')
        else:
            flash('No valid images were uploaded', 'warning')
            
    except Exception as e:
        flash(f'Error adding images: {str(e)}', 'error')
    
    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/sellers')
def sellers():
    sellers_list = sellers_db.get_all_sellers()
    current_seller = get_current_seller()
    return render_template('sellers.html', 
                         sellers=sellers_list, 
                         current_seller=current_seller)

@app.route('/seller/<seller_id>')
def seller_detail(seller_id):
    seller = sellers_db.get_seller_by_id(seller_id)
    if not seller:
        flash('Seller not found', 'error')
        return redirect(url_for('sellers'))
    
    seller_games = sellers_db.get_seller_games(seller_id)
    current_seller = get_current_seller()
    is_own_profile = current_seller and str(current_seller['_id']) == seller_id
    
    return render_template('seller_detail.html', 
                         seller=seller, 
                         games=seller_games,
                         current_seller=current_seller,
                         is_own_profile=is_own_profile)

@app.route('/contact-seller/<seller_id>', methods=['GET', 'POST'])
def contact_seller(seller_id):
    seller = sellers_db.get_seller_by_id(seller_id)
    if not seller:
        flash('Seller not found', 'error')
        return redirect(url_for('games'))
    
    if request.method == 'POST':
        buyer_name = request.form.get('name')
        buyer_email = request.form.get('email')
        message = request.form.get('message')
        game_title = request.form.get('game_title')
        
        print(f"Message to {seller['email']}:")
        print(f"From: {buyer_name} ({buyer_email})")
        print(f"About: {game_title}")
        print(f"Message: {message}")
        
        flash('Your message has been sent to the seller!', 'success')
        return redirect(url_for('game_detail', game_id=request.form.get('game_id')))
    
    return render_template('contact_seller.html', 
                         seller=seller,
                         current_seller=get_current_seller())

# Debug routes
@app.route('/debug/session')
def debug_session():
    return {
        'seller_id_in_session': session.get('seller_id'),
        'current_seller': get_current_seller()
    }

@app.route('/debug/sellers')
def debug_sellers():
    sellers = list(sellers_db.collection.find({}, {'username': 1, 'email': 1, '_id': 1}))
    for seller in sellers:
        seller['_id'] = str(seller['_id'])
    return {'sellers': sellers}

if __name__ == '__main__':
    print("\n🌐 Retro Games Marketplace starting...")
    print("📍 Local:   http://127.0.0.1:5000")
    print("📍 Network: http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)