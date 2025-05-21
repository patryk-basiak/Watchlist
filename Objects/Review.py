import datetime


class Review:
    number = 0
    def __init__(self, date, user_id, movie, text=None, stars=0, language="English" ):
        self.date = date
        self.user = user_id
        self.movie = movie
        self.text = text
        self.rating = stars
        self.lang = language
