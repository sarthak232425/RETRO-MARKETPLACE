# Project Structure and Context Report

## Directory Overview

- `retro_games_marketplace/`
  - Main project folder for the Retro Video Game Marketplace web application.

### Subfolders and Files

- `app.py`: Main Flask application. Handles routing, rendering templates, business logic, and integrates with MongoDB for backend data. Supports authentication, seller dashboard, buyer-seller messaging, rupees sign localization, and image upload. Initializes sample data on startup.
- `requirements.txt`: Lists Python dependencies (Flask, pymongo, python-dotenv, Pillow, python-multipart).
- `.env`: Stores environment variables (MongoDB URI, Flask secret key).
- `config.py`: Loads environment variables and provides global config for database and uploads.
- `create_upload_dirs.py`: Script to create necessary upload directories for images and thumbnails.
- `reset_database.py`: Script to completely reset the database (dangerous, use for cleanup/testing only).

#### `models/`
- `__init__.py`: Initializes sample data for consoles, sellers, and games (Maharashtra, India context, rupees pricing). Ensures no duplicates on startup.
- `database.py`: Connects to MongoDB using config settings, handles connection errors.
- `collections.py`: Defines classes for games, sellers, consoles. Implements CRUD, authentication, filtering, and aggregation logic.

#### `utils/`
- `image_utils.py`: Handles image upload, validation, secure filename generation, and thumbnail creation using Pillow.

#### `templates/`
- `base.html`: Main Bootstrap layout, navigation, sticky footer, flash messages, and Font Awesome integration.
- `index.html`: Home page, hero section, featured games, modern UI.
- `games.html`: Game listing page with filters, grid view, rarity/condition badges, rupees sign for price.
- `game_detail.html`: Detailed view for a single game, seller info, rupees sign for price.
- `add_game.html`: Form for adding a new game listing, simple console dropdown, rupees sign for price.
- `sellers.html`: Seller grid with search/filter, stats, specialties, and Maharashtra context.
- `seller_detail.html`: Seller profile and their games.
- `login.html`, `register.html`: User authentication templates.
- `seller_dashboard.html`: Seller dashboard with game management, rupees sign for price.
- `edit_seller_profile.html`: Seller profile editing form.
- `contact_seller.html`: Buyer-seller messaging form, rupees sign for price.

#### `static/`
- `css/style.css`: Custom CSS for retro theme, Bootstrap overrides, card/badge styling.
- `images/`: Folder for static images (empty by default).
- `uploads/`: Folder for user-uploaded files.
  - `games/`: Stores uploaded game images.
  - `thumbnails/`: Stores thumbnail images for games.

## Script Summaries

- **app.py**: Main entry point. Sets up Flask app, routes, authentication, seller dashboard, game/seller CRUD, messaging, and initializes sample data. Handles all web requests and template rendering.
- **models/__init__.py**: Initializes sample data for consoles, sellers, and games (all Maharashtra, India, rupees pricing). Ensures no duplicates on startup. Can be extended for more data.
- **models/database.py**: Connects to MongoDB using config. Handles connection errors and provides database instance.
- **models/collections.py**: Classes for games, sellers, consoles. Implements CRUD, authentication, filtering, aggregation, and advanced queries.
- **utils/image_utils.py**: Handles image upload, validation, secure filename generation, and thumbnail creation using Pillow. Used in game listing forms.
- **config.py**: Loads environment variables from .env, provides global config for database and uploads.
- **create_upload_dirs.py**: Script to create necessary upload directories for images and thumbnails. Run once during setup.
- **reset_database.py**: Script to completely reset the database (deletes all games, sellers, consoles). Use for cleanup/testing only. Prompts for confirmation before deleting.

## Features
- User authentication (login/register)
- Seller dashboard and profile management
- Game listing, filtering, and detail views
- Buyer-seller messaging workflow
- Image upload and thumbnail generation
- All prices in rupees (₹), Maharashtra context
- Modern Bootstrap UI, sticky footer, Font Awesome icons
- Database cleanup/reset scripts for easy testing

---

*Last updated: October 15, 2025*
