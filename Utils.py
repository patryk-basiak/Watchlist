from Objects.Genre import Genre
from Objects.Movie import Movie

res = None
def load_data(data):
    movies = []
    with open(data, "r") as file:
        for line in file:
            s = line.split(";")
            movies.append(Movie(s[0],s[1],Genre.genre_from_id(s[2]),s[3], s[4]))
    return movies

def load_data_from_database():
    # TODO Implement
    pass
movie_list = load_data('films.txt')
def find_movie_by_title(title):
    title = title.lower()
    global res
    result = []
    for x in movie_list:
        if x.title.lower().startswith(title):
            result.append(x)
            continue
        else:
            for param in x.title_properties:
                if param.lower() == title:
                    result.append(x)
                    continue

    if len(result) >= 0:
        res = result
        return result
    else:
        return None
def get_user_watchlist(user):
    return user.watch_list

def add_movie(title=None, release_year=None, genre_id=None, short_description=None):
    global movie_list
    movie_list.append(Movie(title, release_year, genre_id, short_description))
def get_movie_list():
    return movie_list
def get_last_respond():
    if res is None:
        return movie_list
    return res

def sort_by(var):
    print(var)
    if var == "Title":
        val = sorted(get_last_respond(), key=lambda x: x.title)
    elif var == "Year":
        val = sorted(get_last_respond(), key=lambda x: x.release_year)
    elif var == "Genre":
        val = sorted(get_last_respond(), key=lambda x: x.genre.name)
    elif var == "Rating":
        val = sorted(get_last_respond(), key=lambda x: x.grade, reverse=True)
    else:
        val = get_last_respond()
    return val

def add_movie_object(movie):
    global movie_list
    movie_list.append(movie)