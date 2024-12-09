import logging
from typing import List, Dict

# Configure logger for the model
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Movie:
    def __init__(self, id: int, title: str, release_date: str, runtime: int, vote_average: float):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.runtime = runtime
        self.vote_average = vote_average

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'runtime': self.runtime,
            'vote_average': self.vote_average,
        }


class MovieListModel:
    def __init__(self):
        self.movie_list: List[Movie] = []

    def add_movie(self, movie: Movie) -> None:
        logger.info(f"Adding movie {movie.title} (ID: {movie.id}) to the list")
        if movie.id in [m.id for m in self.movie_list]:
            logger.error(f"Movie with ID {movie.id} already exists")
            raise ValueError(f"Movie with ID {movie.id} already exists in the list")

        self.movie_list.append(movie)

    def remove_movie(self, movie_id: int) -> None:
        logger.info(f"Removing movie with ID {movie_id} from the list")
        movie = next((m for m in self.movie_list if m.id == movie_id), None)
        if not movie:
            logger.error(f"Movie with ID {movie_id} not found")
            raise ValueError(f"Movie with ID {movie_id} not found in the list")

        self.movie_list.remove(movie)
        logger.info(f"Movie with ID {movie_id} has been removed")

    def get_movie_by_id(self, movie_id: int) -> Movie:
        logger.info(f"Fetching movie with ID {movie_id}")
        movie = next((m for m in self.movie_list if m.id == movie_id), None)
        if not movie:
            logger.error(f"Movie with ID {movie_id} not found")
            raise ValueError(f"Movie with ID {movie_id} not found in the list")

        return movie

    def get_all_movies(self) -> List[Movie]:
        logger.info("Fetching all movies in the list")
        return self.movie_list

    def clear_list(self) -> None:
        logger.info("Clearing all movies from the list")
        self.movie_list.clear()

    def get_list_length(self) -> int:
        return len(self.movie_list)

    def get_movie_details(self, movie_id: int, tmdb_request) -> Movie:
        logger.info(f"Getting movie details for ID {movie_id} from TMDB API")
        response = tmdb_request(f"/movie/{movie_id}")

        if "id" not in response:
            logger.error(f"Failed to get details for movie ID {movie_id}")
            raise ValueError(f"Movie with ID {movie_id} not found in TMDB API")

        movie = Movie(
            id=response["id"],
            title=response.get("original_title"),
            release_date=response.get("release_date"),
            runtime=response.get("runtime"),
            vote_average=response.get("vote_average"),
        )
        logger.info(f"Got details for movie {movie.title} (ID: {movie.id})")
        return movie


    
   