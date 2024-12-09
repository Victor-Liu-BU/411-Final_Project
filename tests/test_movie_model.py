import pytest
from movie_collection.models.movie_model import MovieListModel, Movie

@pytest.fixture()
def movie_list_model():
    """Fixture to provide a new instance of MovieListModel for each test."""
    return MovieListModel()

@pytest.fixture
def sample_movie1():
    return Movie(1, "Inception", "2010-07-16", 148, 8.8)

@pytest.fixture
def sample_movie2():
    return Movie(2, "The Dark Knight", "2008-07-18", 152, 9.0)

@pytest.fixture
def sample_movie_list(sample_movie1, sample_movie2):
    return [sample_movie1, sample_movie2]

##################################################
# Add Movie Management Test Cases
##################################################

def test_add_movie_to_list(movie_list_model, sample_movie1):
    """Test adding a movie to the list."""
    movie_list_model.add_movie(sample_movie1)
    assert len(movie_list_model.movie_list) == 1
    assert movie_list_model.movie_list[0].title == 'Inception'

def test_add_duplicate_movie_to_list(movie_list_model, sample_movie1):
    """Test error when adding a duplicate movie to the list by ID."""
    movie_list_model.add_movie(sample_movie1)
    with pytest.raises(ValueError, match="Movie with ID 1 already exists in the list"):
        movie_list_model.add_movie(sample_movie1)

def test_add_invalid_movie_to_list(movie_list_model):
    """Test error when adding an invalid movie to the list."""
    with pytest.raises(TypeError, match="Movie is not of valid type"):
        movie_list_model.add_movie("Not a movie object")

##################################################
# Remove Movie Management Test Cases
##################################################

def test_remove_movie_from_list(movie_list_model, sample_movie_list):
    """Test removing a movie from the list by movie_id."""
    for movie in sample_movie_list:
        movie_list_model.add_movie(movie)
    assert len(movie_list_model.movie_list) == 2
    movie_list_model.remove_movie(1)
    assert len(movie_list_model.movie_list) == 1
    assert movie_list_model.movie_list[0].id == 2

def test_remove_nonexistent_movie(movie_list_model):
    """Test error when removing a non-existent movie from the list."""
    with pytest.raises(ValueError, match="Movie with ID 1 not found in the list"):
        movie_list_model.remove_movie(1)

def test_clear_movie_list(movie_list_model, sample_movie1):
    """Test clearing the entire movie list."""
    movie_list_model.add_movie(sample_movie1)
    movie_list_model.clear_list()
    assert len(movie_list_model.movie_list) == 0

##################################################
# Movie Retrieval Test Cases
##################################################

def test_get_movie_by_id(movie_list_model, sample_movie1):
    """Test successfully retrieving a movie from the list by movie ID."""
    movie_list_model.add_movie(sample_movie1)
    retrieved_movie = movie_list_model.get_movie_by_id(1)
    assert retrieved_movie.id == 1
    assert retrieved_movie.title == 'Inception'
    assert retrieved_movie.release_date == '2010-07-16'
    assert retrieved_movie.runtime == 148
    assert retrieved_movie.vote_average == 8.8

def test_get_all_movies(movie_list_model, sample_movie_list):
    """Test successfully retrieving all movies from the list."""
    for movie in sample_movie_list:
        movie_list_model.add_movie(movie)
    all_movies = movie_list_model.get_all_movies()
    assert len(all_movies) == 2
    assert all_movies[0].id == 1
    assert all_movies[1].id == 2

def test_get_list_length(movie_list_model, sample_movie_list):
    """Test getting the length of the movie list."""
    for movie in sample_movie_list:
        movie_list_model.add_movie(movie)
    assert movie_list_model.get_list_length() == 2

##################################################
# Movie Details Retrieval Test Case
##################################################

def test_get_movie_details(movie_list_model, mocker):
    """Test retrieving movie details from TMDB API."""
    mock_tmdb_request = mocker.Mock()
    mock_tmdb_request.return_value = {
        "id": 3,
        "original_title": "Interstellar",
        "release_date": "2014-11-07",
        "runtime": 169,
        "vote_average": 8.6
    }

    movie = movie_list_model.get_movie_details(3, mock_tmdb_request)
    
    assert movie.id == 3
    assert movie.title == "Interstellar"
    assert movie.release_date == "2014-11-07"
    assert movie.runtime == 169
    assert movie.vote_average == 8.6

    mock_tmdb_request.assert_called_once_with("/movie/3")

def test_get_movie_details_not_found(movie_list_model, mocker):
    """Test error when movie details are not found in TMDB API."""
    mock_tmdb_request = mocker.Mock()
    mock_tmdb_request.return_value = {}

    with pytest.raises(ValueError, match="Movie with ID 999 not found in TMDB API"):
        movie_list_model.get_movie_details(999, mock_tmdb_request)

    mock_tmdb_request.assert_called_once_with("/movie/999")
