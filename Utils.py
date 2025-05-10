from Objects.Genre import Genre
from Objects.Movie import Movie


def load_data(data):
    movies = []
    with open(data, "r") as file:
        for line in file:
            s = line.split(";")
            movies.append(Movie(s[0],s[1],Genre.genre_from_id(s[2]),s[3]))
    return movies

def load_data_from_database():
    # TODO Implement
    pass
movie_list = load_data('films.txt')
def find_movie(m):
    result = next((x for x in movie_list if x.title==m), None)
    if result is not None:
        return result
    else:
        print("There is not such film in our database")

