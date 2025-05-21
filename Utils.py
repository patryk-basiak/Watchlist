import datetime
import shutil
import sqlite3
from tkinter.font import names

from Objects.Director import Director
from Objects.Genre import Genre
from Objects.Movie import Movie
from Objects.Review import Review

res = None


def load_data(data):
    movies = []
    with open(data, "r") as file:
        for line in file:
            s = line.split(";")
            movies.append(Movie(s[0], int(s[1]), Genre.genre_from_id(s[2]), s[3], s[4]))
    return movies


def load_data_from_database():
    connection = sqlite3.connect("watchlist.db")
    cursor = connection.cursor()

    query = '''
    SELECT 
        m.title,
        d.id, d.name, d.surname,
        m.release_year,
        g.id, g.name,
        m.description
    FROM movies m
    JOIN directors d ON m.director_id = d.id
    JOIN genres g ON m.genre_id = g.id;
    '''

    cursor.execute(query)
    rows = cursor.fetchall()

    movies = []
    for row in rows:
        title = row[0]
        director = Director(name=row[2], surname=row[3], director_id=row[1])
        release_year = row[4]
        genre = Genre(name=row[6], genre_id=row[5])
        description = row[7]

        movie = Movie(title, director, release_year, genre, description)
        movies.append(movie)
    for movie in movies:
        query = '''
                SELECT *
FROM Review
WHERE movie_id = ?;
'''

        cursor.execute(query, (movie.id,))
        rows = cursor.fetchall()
        for row in rows:
            rev = Review(row[0], row[1], row[2] , movie.id, row[4], row[5], row[6])
            movie.reviews.append(rev)
    connection.close()
    return movies

file = 'films.txt'
movie_list = load_data_from_database()


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


def add_movie(title=None,director=None, release_year=None, genre_id=None, short_description=None):
    global movie_list
    movie = Movie(title, director, release_year, genre_id, short_description)
    movie_list.append(movie)
    save_movie(movie)


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
    elif var == "Director":
        val = sorted(get_last_respond(), key=lambda x: x.director)
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
    connection = sqlite3.connect("watchlist.db")
    sql = "INSERT INTO movies(title,director_id,release_year, genre_id, description) VALUES(?,?,?,?,? )"
    cursor = connection.cursor()
    cursor.execute(sql, (movie.title, movie.director.id, movie.release_year, movie.genre.id, movie.description))
    connection.commit()
    movie_list.append(movie)


def save_movie(movie):
    global file
    with open(file, "a") as file:
        file.write(';'.join(movie.get_values()))
    print("Movie save to txt file")

def get_all_genres():
    connection = sqlite3.connect("watchlist.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name FROM genres")
    rows = cursor.fetchall()
    connection.close()
    genres = [Genre(genre_id=row[0], name=row[1]) for row in rows]
    return genres

def get_all_directors():
    connection = sqlite3.connect("watchlist.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, surname FROM directors")
    rows = cursor.fetchall()
    connection.close()

    directors = [Director(director_id=row[0], name=row[1], surname=row[2]) for row in rows]
    return directors


def add_review(rew):
    connection = sqlite3.connect("watchlist.db")
    sql = "INSERT INTO Review(date, user_id,movie_id, text, rating, lang) VALUES(?,?,?,?,?,? )"
    cursor = connection.cursor()
    cursor.execute(sql, (datetime.datetime.now(), rew.user, rew.movie.id, rew.text, rew.rating, rew.lang))
    connection.commit()
    rew.movie.add_review(rew)