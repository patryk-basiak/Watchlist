import datetime
from Objects.Errors import EmptyEntry


class Movie:
    number = 0
    def __init__(self, title, director, release_year, genre, description, grade=None):
        self.title = title
        self.director = director
        self.release_year = release_year
        self.genre = genre
        self.description = description
        self.grade = grade
        self.id = Movie.number
        Movie.number += 1
        self.reviews = []
        self.title_properties = title.split()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise EmptyEntry("Title is null")
        self._title = value

    @property
    def release_year(self):
        return self._release_year

    @release_year.setter
    def release_year(self, value):
        try:
            new_value = int(value)
        except (TypeError, ValueError):
            raise TypeError("Rease year must be an Integer")
        if new_value > datetime.datetime.now().year:
            raise ValueError("Release year cannot be in the future")
        self._release_year = new_value

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Director: {self.director}\n"
                f"Release Year: {self.release_year}\n"
                f"Genre: {self.genre}\n"
                f"Description: {self.description}")

    def add_review(self, review):
        self.reviews.append(review)

    def delete_review(self, review):
        self.reviews.remove(review)

    def get_values(self):
        return [self.title, self.director, self.release_year, self.genre, self.grade, self.description]

    def print_reviews(self):
        print(self.title + " reviews: ")
        for review in self.reviews:
            print(f"ID: {review.id} User: {review.user}, rating: {review.rating}, text: {review.text}")