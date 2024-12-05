from flask import Flask, jsonify, make_response, request
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

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
        }), 201)
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