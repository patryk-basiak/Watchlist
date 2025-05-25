import datetime
import smtplib
import sqlite3
from email.mime.text import MIMEText
from xmlrpc.client import DateTime
from dotenv import load_dotenv
import os
import requests
from urllib.parse import quote


from Objects import User
from Objects.Director import Director
from Objects.Errors import MovieAlreadyExists, ReviewDoesntExist
from Objects.Genre import Genre
from Objects.Movie import Movie
from Objects.Review import Review
from analyze.Service import analyze

res = None


def load_data(data):
    movies = []
    with open(data, "r") as f:
        for line in f:
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
load_dotenv()
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

def find_movie_by_title(title) -> list[Movie] or None:
    title = title.lower()
    global res
    result = []
    for x in movie_list:
        if x.title.lower().startswith(title):
            result.append(x)
            continue
        else:
            for param in x.title_properties:
                if param == title:
                    result.append(x)
                    continue
            if jaro_find(x.title.lower(), title) > 0.85:
                result.append(x)

    if len(result) >= 0:
        res = result
        return result
    else:
        return None


def get_user_watchlist(user:User) -> list[[Movie, DateTime]]:
    return user.watch_list

def get_movie_list():
    return movie_list


def get_last_respond():
    if res is None:
        return movie_list
    return res


def sort_by(var):
    global res
    if var == "Title":
        val = sorted(get_last_respond(), key=lambda x: x.title)
    elif var == "Director":
        val = sorted(get_last_respond(), key=lambda x: x.director.surname)
    elif var == "Year":
        val = sorted(get_last_respond(), key=lambda x: x.release_year)
    elif var == "Genre":
        val = sorted(get_last_respond(), key=lambda x: x.genre.name)
    elif var == "Rating":
        val = sorted(get_last_respond(), key=lambda x: x.grade, reverse=True)
    else:
        val = get_last_respond()
    res = val
    return val


def add_movie(movie: Movie) -> None:
    global movie_list
    if check_movie_exists(movie):
        raise MovieAlreadyExists("Movie with that attributes already exists")
    connection = sqlite3.connect("watchlist.db")
    sql = "INSERT INTO movies(title,director_id,release_year, genre_id, description) VALUES(?,?,?,?,? )"
    cursor = connection.cursor()
    cursor.execute(sql, (movie.title, movie.director.id, movie.release_year, movie.genre.id, movie.description))
    connection.commit()
    movie_list.append(movie)

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
    sql = "INSERT INTO Review(date, user_id, movie_id, text, rating, lang) VALUES(?,?,?,?,?,? )"
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
    try:
        title = js['Title']
    except Exception as e:
        raise "Fetching error"
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
    add_movie(m)
    return m


def add_movie_to_watchlist(current_movie, user) -> None:
    connection = sqlite3.connect("watchlist.db")
    sql = "INSERT INTO User_Movie(userID, movieID, date) VALUES(?,?,? )"
    cursor = connection.cursor()
    date = datetime.datetime.now()
    cursor.execute(sql, (user.id, current_movie.id, date))
    connection.commit()
    user.add_movie(current_movie,date)

def remove_from_watchlist(movie, user) -> None:
    connection = sqlite3.connect("watchlist.db")
    sql = "DELETE FROM User_Movie WHERE userId = ? and movieId = ?"
    cursor = connection.cursor()
    cursor.execute(sql, (user.id, movie.id))
    connection.commit()
    user.delete_movie(movie)


def set_checkbox(current_movie, param, user) -> None:
    if param:
        connection = sqlite3.connect("watchlist.db")
        sql = "INSERT INTO Watched(userID, movieID) VALUES(?,? )"
        cursor = connection.cursor()
        cursor.execute(sql, (user.id, current_movie.id))
        connection.commit()

    else:
        connection = sqlite3.connect("watchlist.db")
        sql = "DELETE FROM Watched WHERE userId = ? and  movieId = ? "
        cursor = connection.cursor()
        cursor.execute(sql, (user.id, current_movie.id))
        connection.commit()
    current_movie.watched = param

def get_genre_from_watchlist(user:User) -> dict[str, int]:
    result = {}
    connection = sqlite3.connect("watchlist.db")
    cursor = connection.cursor()
    query = "SELECT name from Movies INNER JOIN main.genres g on g.id = Movies.genre_id inner join main.User_Movie UM on Movies.id = UM.movieID inner join main.User U on U.id = UM.userID where U.id =?"
    cursor.execute(query, (user.id,))
    rows = cursor.fetchall()
    for row in rows:
        if row[0] in result:
            result[row[0]] += 1
        else:
            result[row[0]] = 1
    connection.close()
    return result

def get_recommended_movie(user:User) -> Movie or None:
    r = get_genre_from_watchlist(user)
    genre = max(r, key=r.get)

    rating = -1
    temp_movie = None
    for movie in movie_list:
        if str(movie.genre) == genre:
            if not movie.watched and rating < movie.grade:
                temp_movie = movie
                rating = movie.grade
    new_list = sorted(movie_list, key=lambda x: x.grade, reverse=True)
    if not temp_movie:
        temp_movie = next(x for x in new_list if not x.watched)
    if not temp_movie:
        temp_movie = new_list[0]
    return temp_movie

def jaro_find(s1 :str, s2:str) -> float:
    if s1 == s2:
        return 1
    m = 0
    t = 0
    s_p = 0
    prefix = True
    for i, e in enumerate(s2):
        if e in s1:
            m += 1
            if i < len(s1) and e == s1[i]:
                if prefix:
                    s_p += 1
                t += 1
            else:
                prefix = False
    if m == 0:
        return 0
    t = (len(s2) - t) / 2
    result = 1 / 3 * (m / len(s1) + m / len(s2) + ((m - t) / m))

    l = s_p
    result += l * 0.1 * (1 - result)
    return result

def apply_genre_filer(selected_genres: [Genre])-> [Movie]:
    global res
    all_movies = res
    if res is None:
        all_movies = movie_list

    if len(selected_genres) == 0:
        result = movie_list
    else:
        result = [m for m in all_movies if m.genre.name in selected_genres]
    res = result
    return res

def apply_director_filer(selected_director :[Director]) -> [Movie]:
    global res
    all_movies = res
    if res is None:
        all_movies = movie_list

    if len(selected_director) == 0:
        result = movie_list
    else:
        result = [m for m in all_movies if m.director.full_name() in selected_director]
    res = result
    return res


def delete_review(review):
    connection = sqlite3.connect("watchlist.db")
    sql = "DELETE FROM Review WHERE user_id = ? and movie_id = ?"
    cursor = connection.cursor()
    if type(review.movie) == int: #napraw to kiedys patryk 
        cursor.execute(sql, (review.user, review.movie))
    else:
        cursor.execute(sql, (review.user, review.movie.id))
    connection.commit()
    movie = None
    if type(review.movie) == int:
        for m in movie_list:
            if m.id == review.movie:
                movie = m
                break
    else:
        for m in movie_list:
            if m.id == review.movie.id:
                movie = m
                break
    if movie is None:
        raise ValueError("Movie with that id not found")
    movie.delete_review(review)
    del review

def check_movie_exists(movie : Movie) -> bool:
    for m in movie_list:
        if movie.get_string_values() == m.get_values():
            return True

    return False
def get_review_id(review: Review) -> int:
    connection = sqlite3.connect("watchlist.db")
    cursor = connection.cursor()
    sql = "SELECT id FROM Review where user_id = ? and movie_id = ?"
    cursor.execute(sql, (review.user, review.movie))
    rows = cursor.fetchall()
    if len(rows) == 0:
        raise ReviewDoesntExist("review with that user_id and movie_id doesnt exists")
    return rows[0][0]

def report_review(review, user):
    sender = os.getenv("email_address")
    recipients = os.getenv("recipients")

    movie_title = next((x.title for x in movie_list if x.id == review.movie), "Unknown Movie")
    author_username = get_username_by_id(review.user) or "Unknown User"
    reporting_user = user.login or "Unknown Reporter"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email_body = (
        f"A review for the movie \"{movie_title}\" written by [{author_username}] "
        f"was reported by user {reporting_user} on {timestamp}.\n\n"
        f"Review ID: {get_review_id(review)}\n"
        "Please review this report and take appropriate action if necessary."
    )

    msg = MIMEText(email_body)
    msg['Subject'] = "Reported Review Notification"
    msg['From'] = sender
    msg['To'] = recipients
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, os.getenv("password"))
        smtp_server.sendmail(sender, recipients, msg.as_string())


def get_user_watchlist_watched(user):
    result = {"True" : 0, "False":0 }
    for movie, date in user.watch_list:
        result[str(movie.watched)] += 1

    result["Yes"] = result.pop("True")
    result["No"] = result.pop("False")
    return result


def get_the_best_genre():
    result = {}
    temp = {}
    for movie in movie_list:
        if movie.grade > 0:
            if movie.genre in result:
                result[str(movie.genre)] += movie.grade
                temp[str(movie.genre)] += 1
            else:
                result[str(movie.genre)] = movie.grade
                temp[str(movie.genre)] = 1
    for v in result:
        result[v] = result[v]/temp[v]
    return result

def update_movie(movie):
    connection = sqlite3.connect("watchlist.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE movies
        SET title = ?, release_year = ?, description = ?
        WHERE title = ? AND release_year = ?
    """, (movie.title, movie.release_year, movie.description, movie.title, movie.release_year))
    connection.commit()
    connection.close()


def get_image(language):
    if language == "Polish":
        return "Assets/Flag_of_Poland.png"
    if language == "English":
        return "Assets/Flag_of_the_United_States.png"
    if language == "Czech":
        return "Assets/Flag_of_the_Czech_Republic.png"
    if language == "German":
        return "Assets/Flag_of_Germany.png"
    if language == "French":
        return "Assets/Flag_of_France.png"
    if language is None:
        return "Assets/question_mark.png"
    return None

def test_language(prompt):
    result = analyze(prompt, data_form="String")
    return result