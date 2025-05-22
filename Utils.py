import datetime
import shutil
import sqlite3
from tkinter.font import names

import requests
from urllib.parse import quote
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
        m.description,
        m.id
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
        id_n = row[8]

        movie = Movie(title, director, release_year, genre, description, id_n)
        movies.append(movie)

    for movie in movies:
        suma = 0

        query = '''
                SELECT *
FROM Review
WHERE movie_id = ?;
'''

        cursor.execute(query, (movie.id,))
        rows = cursor.fetchall()
        for row in rows:
            suma += float(row[5])
            parsed_date = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f")
            rev = Review(parsed_date, row[2] , movie.id, row[4], row[5], row[6])
            movie.reviews.append(rev)
        if len(rows) != 0:
            movie.grade = suma/len(rows)
        query = '''
                        SELECT *
        FROM Watched
        WHERE movieId = ?;
        '''
        cursor.execute(query, (movie.id,))
        result = cursor.fetchall()
        if len(result) > 0:
            movie.watched = True
    connection.close()


    return movies

file = 'films.txt'
movie_list = load_data_from_database()

def load_watchlist(user):
    connection = sqlite3.connect("watchlist.db")
    cursor = connection.cursor()

    query = '''
        SELECT 
            *
        FROM User_Movie
        where userId = ?
        '''

    cursor.execute(query, (user.id,))
    rows = cursor.fetchall()
    for row in rows:
        parsed_date = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f")
        user.watch_list.append([next(x for x in movie_list if x.id == row[1]), parsed_date])

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
    cursor.execute(sql, (rew.date, rew.user, rew.movie.id, rew.text, rew.rating, rew.lang))
    connection.commit()
    rew.movie.add_review(rew)

def get_username_by_id(user_id):
    connection = sqlite3.connect("watchlist.db")
    cursor = connection.cursor()
    sql = "SELECT login FROM user where id = ?"
    cursor.execute(sql, (user_id, ))
    rows = cursor.fetchall()
    print(rows)
    return rows[0][0]

def add_genre(param):
    connection = sqlite3.connect("watchlist.db")
    sql = "INSERT INTO Genres(name) VALUES(?)"
    cursor = connection.cursor()
    cursor.execute(sql, (param, ))
    connection.commit()
    genre_id = cursor.lastrowid
    connection.close()
    return genre_id

def add_director(param):
    connection = sqlite3.connect("watchlist.db")
    sql = "INSERT INTO Directors(name, surname) VALUES(?,?)"
    cursor = connection.cursor()
    cursor.execute(sql, (param[0], " ".join(param[1:])))
    connection.commit()

    director_id = cursor.lastrowid

    connection.close()

    return director_id



def get_movie_from_web(param):
    param = quote(param)
    apikey = "REMOVED"
    x = requests.get(f'https://www.omdbapi.com/?t={param}&apikey={apikey}')
    js = x.json()
    title = js['Title']
    director = None
    year = js['Released'].split()[-1]
    genre = None
    for g in get_all_genres():
        if g.name == js['Genre'].split(',')[0]:
            genre = g
            break
    if genre is None:
        genre_id = add_genre(js['Genre'].split(',')[0])
        genre = Genre(js['Genre'].split(',')[0], genre_id)
    for direct in get_all_directors():
        if direct.name == js['Director'].split()[0]:
            director = direct
            break
    if director is None:
        director_id = add_director(js['Director'].split())
        director = Director(js['Director'].split()[0], js['Director'].split()[1], director_id)

    description = js['Plot']
    m = Movie(title, director, year, genre, description, None)
    add_movie_object(m)
    return m


def add_movie_to_watchlist(current_movie, user):
    connection = sqlite3.connect("watchlist.db")
    sql = "INSERT INTO User_Movie(userID, movieID, date) VALUES(?,?,? )"
    cursor = connection.cursor()
    date = datetime.datetime.now()
    cursor.execute(sql, (user.id, current_movie.id, date))
    connection.commit()
    user.add_movie(current_movie,date)

def remove_from_watchlist(movie, user):
    connection = sqlite3.connect("watchlist.db")
    sql = "DELETE FROM User_Movie WHERE userId = ? and movieId = ?"
    cursor = connection.cursor()
    cursor.execute(sql, (user.id, movie.id))
    connection.commit()
    user.delete_movie(movie)


def set_checkbox(current_movie, param, user):
    if param:
        connection = sqlite3.connect("watchlist.db")
        sql = "INSERT INTO Watched(userID, movieID) VALUES(?,? )"
        cursor = connection.cursor()
        cursor.execute(sql, (user.id, current_movie.id))
        connection.commit()
    else:
        connection = sqlite3.connect("watchlist.db")
        sql = "DELETE FROM Watched WHERE userId, movieId "
        cursor = connection.cursor()
        cursor.execute(sql, (user.id, current_movie.id))
        connection.commit()
