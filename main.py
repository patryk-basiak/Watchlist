from Objects.Genre import Genre
from Objects.Movie import Movie
from Objects.Review import Review
from Objects.User import User

Patryk = User("Patryk", "123")



print("Movie find system")
def find_movie(movie_list):
    m = input("Provide movie title: ")
    result = next((x for x in movie_list if x.title==m), None)
    if result is not None:
        print(result)
        return result
    else:
        print("There is not such film in our database")


def load_data(data):
    movies = []
    with open(data, "r") as file:
        for line in file:
            s = line.split(";")
            movies.append(Movie(s[0],s[1],Genre.genre_from_id(s[2]),s[3]))
    return movies

mov = load_data("films.txt")
for m in mov:
    print(m)
