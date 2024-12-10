from typing import Any, Dict, Tuple
from venv import logger
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import sqlalchemy
import bcrypt
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_BINDS'] = {
    'users': os.getenv('DATABASE_URL', 'sqlite:///user_table.db'),
    'movies': os.getenv('DATABASE_URL', 'sqlite:///movie_table.db')
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    """
    """
    __bind_key__ = 'users'
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    salt = db.Column(db.LargeBinary, nullable=False)
    hashed_password = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def hash_password(password: str) -> Tuple[bytes, bytes]:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return salt, hashed_password

def verify_password(stored_salt: bytes, stored_hash: bytes, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

@app.route('/clear-user-catalog', methods=['DELETE'])   
def clear_catalog_user():
    """
    clears the user database

    Raises:
    """
    try:
        # Create a session
        with Session(db) as session:
            # Delete all songs
            session.query(User).delete()
            session.commit()
        
        # Log that the catalog was cleared successfully
        logger.info("Catalog cleared successfully.")
    
    except sqlalchemy.exc.SQLAlchemyError as e:
        # Log the error and raise it
        logger.error(f"Database error while clearing catalog: {str(e)}")
        raise e
    
@app.route('/clear-movie-catalog', methods=['DELETE'])    
def clear_catalog_Movie():
    try:
        # Create a session
        with Session(db) as session:
            # Delete all songs
            session.query(Movie).delete()
            session.commit()
        
        # Log that the catalog was cleared successfully
        logger.info("Catalog cleared successfully.")
    
    except sqlalchemy.exc.SQLAlchemyError as e:
        # Log the error and raise it
        logger.error(f"Database error while clearing catalog: {str(e)}")
        raise e

class Movie(db.Model):
    __bind_key__ = 'movies'
    __tablename__ = 'movie_table'
    id = db.Column(db.Integer, primary_key=True)
    original_language = db.Column(db.String(10), nullable=False)
    original_title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    vote_average = db.Column(db.Float, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Movie object to a dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the movie.
        """
        return {
            'id': self.id,
            'original_language': self.original_language,
            'original_title': self.original_title,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'runtime': self.runtime,
            'vote_average': self.vote_average
        }
    def __repr__(self):
        return f'<Movie {self.original_title} ({self.release_date.year if self.release_date else "Unknown"})>'

with app.app_context():
    db.create_all()


@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        logger.warning('Invalid account creation attempt: Missing credentials')
        return jsonify({'error': 'Username and password required'}), 400
    username = data['username']
    password = data['password']

    try:
        # Generate salt and hash
        salt, hashed_password = hash_password(password)
        
        # Create new user
        new_user = User(
            username=username, 
            salt=salt, 
            hashed_password=hashed_password
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f'Account created for username: {username}')
        return jsonify({'message': 'Account created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        logger.warning(f'Account creation failed: Username {username} already exists')
        return jsonify({'error': 'Username already exists'}), 409
    except Exception as e:
        # Catch any unexpected errors
        db.session.rollback()
        logger.error(f'Unexpected error in account creation: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        logger.warning('Invalid login attempt: Missing credentials')
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    try:
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            logger.warning(f'Login attempt for non-existent user: {username}')
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if verify_password(user.salt, user.hashed_password, password):
            logger.info(f'Successful login for username: {username}')
            return jsonify({'message': 'Login successful'}), 200
        else:
            logger.warning(f'Failed login attempt for username: {username}')
            return jsonify({'error': 'Invalid credentials'}), 401
    
    except Exception as e:
        logger.error(f'Unexpected error in login: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500
    
@app.route('/update-password', methods=['POST'])
def update_password():
    data = request.get_json()
    required_fields = ['username', 'current_password', 'new_password']
    if not all(field in data for field in required_fields):
        logger.warning('Invalid password update attempt: Missing credentials')
        return jsonify({'error': 'Username, current password, and new password required'}), 400
    
    username = data['username']
    current_password = data['current_password']
    new_password = data['new_password']
    try:
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            logger.warning(f'Password update attempt for non-existent user: {username}')
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not verify_password(user.salt, user.hashed_password, current_password):
            logger.warning(f'Failed password update attempt for username: {username}')
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Generate new salt and hash for the new password
        new_salt, new_hashed_password = hash_password(new_password)
        
        # Update user's password
        user.salt = new_salt
        user.hashed_password = new_hashed_password
        db.session.commit()
        
        logger.info(f'Password updated successfully for username: {username}')
        return jsonify({'message': 'Password updated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f'Unexpected error in password update: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

##############################################
# health and db checks
##############################################

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check for the service.
    """
    return jsonify({'status': 'healthy'}), 200

# Database Connection Check Endpoint
@app.route('/db-check', methods=['GET'])
def db_check():
    """
    Check database connection.
    """
    try:
        # Attempt to query the database to check the connection
        db.session.execute('SELECT 1')  
        return jsonify({'database_status': 'healthy'}), 200
    except Exception as e:
        app.logger.error(f"Database connection check failed: {str(e)}")  # Log error
        return jsonify({'database_status': 'unhealthy', 'error': str(e)}), 500

# TMDB API configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

##############################################
# Helper Functions
##############################################

def tmdb_request(endpoint, method='GET', params=None, data=None):
    url = f"{TMDB_BASE_URL}{endpoint}"
    headers = {
        'Authorization': f"Bearer {TMDB_API_KEY}",
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.request(method, url, params=params, json=data, headers=headers)
    return response.json()

##############################################
# Movie List Management
##############################################

@app.route('/api/list/create', methods=['POST'])
def create_list():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name:
            return make_response(jsonify({'error': 'Name is required'}), 400)

        response = tmdb_request('/list', method='POST', data={
            'name': name,
            'description': description
        })

        return make_response(jsonify({
            'status_code': response.get('status_code'),
            'status_message': response.get('status_message'),
            'list_id': response.get('id')
        }), 200)
    except Exception as e:
        app.logger.error(f"Error creating list: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/list/<int:list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    try:
        response = tmdb_request(f'/list/{list_id}', method='DELETE')

        return make_response(jsonify({
            'status_code': response.get('status_code'),
            'status_message': response.get('status_message')
        }), 200)
    except Exception as e:
        app.logger.error(f"Error deleting list: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/list/<int:list_id>/add_movie', methods=['POST'])
def add_movie_to_list(list_id):
    try:
        data = request.get_json()
        movie_id = data.get('movie_id')

        if not movie_id:
            return make_response(jsonify({'error': 'Movie ID is required'}), 400)

        response = tmdb_request(f'/list/{list_id}/add_item', method='POST', data={
            'media_id': movie_id
        })

        return make_response(jsonify({
            'status_code': response.get('status_code'),
            'status_message': response.get('status_message')
        }), 200)
    except Exception as e:
        app.logger.error(f"Error adding movie to list: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/list/<int:list_id>/remove_movie', methods=['POST'])
def remove_movie_from_list(list_id):
    try:
        data = request.get_json()
        movie_id = data.get('movie_id')

        if not movie_id:
            return make_response(jsonify({'error': 'Movie ID is required'}), 400)

        response = tmdb_request(f'/list/{list_id}/remove_item', method='POST', data={
            'media_id': movie_id
        })

        return make_response(jsonify({
            'status_code': response.get('status_code'),
            'status_message': response.get('status_message')
        }), 200)
    except Exception as e:
        app.logger.error(f"Error removing movie from list: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

##############################################
# Movie Details
##############################################

@app.route('/api/movie/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    try:
        response = tmdb_request(f'/movie/{movie_id}')

        movie_details = {
            'original_language': response.get('original_language'),
            'original_title': response.get('original_title'),
            'release_date': response.get('release_date'),
            'runtime': response.get('runtime'),
            'vote_average': response.get('vote_average')
        }

        return make_response(jsonify({
            'status': 'success',
            'movie_details': movie_details
        }), 200)
    except Exception as e:
        app.logger.error(f"Error getting movie details: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
