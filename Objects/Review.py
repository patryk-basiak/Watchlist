import datetime


class Review:
    number = 0
    def __init__(self, user, movie, text=None, stars=0, language="English" ):
        self.id = Review.number
        Review.number += 1
        self.date = datetime.datetime.now()
        self.user = user
        self.movie = movie
        self.text = text
        self.rating = stars
        self.lang = language
