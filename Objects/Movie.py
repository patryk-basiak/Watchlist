import datetime

from Objects.Errors import EmptyEntry


class Movie:
    number = 0
    def __init__(self, title, release_year, genre_id=None, short_description=None, grade=None):
        self.title = title
        self.grade=grade
        self.id = Movie.number
        Movie.number += 1
        self.release_year = release_year
        self.genre = genre_id
        self.description = short_description
        self.reviews = []
        self.title_properties = title.split()

    @property
    def title(self):
        return self._title

    @property
    def release_year(self):
        return self._release_year

    def __str__(self):
        return f"Title: {self.title}\nrelease_year: {self.release_year}, genre: {self.genre}, description: {self.description}"

    def add_review(self, review):
        self.reviews.append(review)

    def delete_review(self, review):
        self.reviews.remove(review)

    def get_values(self):
        return [self.title, self.release_year, self.genre, self.grade, self.description]

    def print_reviews(self):
        print(self.title + " reviews: ")
        for review in self.reviews:
            print(f"ID: {review.id} User: {review.user}, rating: {review.rating}, text: {review.text}")

    @title.setter
    def title(self, value):
        if len(value) == 0:
            raise EmptyEntry("Title is null")
        self._title = value

    @release_year.setter
    def release_year(self, value):
        try:
            int(value)
        except TypeError:
            raise TypeError
        new_value = int(value)
        if new_value > datetime.datetime.now().year:
            raise ValueError
        self._release_year = new_value
