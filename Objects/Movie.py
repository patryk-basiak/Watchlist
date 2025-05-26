import datetime
from Objects.Errors import EmptyEntry


class Movie:
    def __init__(self, title, director, release_year, genre, description, no, grade=0, watched=False):
        self.title = title
        self.director = director
        self.release_year = release_year
        self.genre = genre
        self.description = description
        self.grade = grade
        self.id = no
        self.reviews = []
        self.title_properties = title.split()
        cleaned_properties = []
        for prop in self.title_properties:
            cleaned_prop = ''.join(char for char in prop.lower() if char.isalnum() or char == ' ')
            cleaned_properties.append(cleaned_prop)
        self.title_properties = cleaned_properties
        self.watched = watched

    @property
    def title(self):
        return self._title


    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        self._grade = round(value, 2)


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
        if not value:
            raise EmptyEntry("Release year is empty")
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
        if len(self.reviews) == 1:
            self.grade = review.rating
        else:
            review_count = len(self.reviews)
            temp_sum = self.grade * review_count
            self.grade = (temp_sum + review.rating  ) / (review_count + 1)


    def delete_review(self, review):
        self.reviews.remove(review)
        if len(self.reviews) == 0:
            self.grade = 0
        else:
            review_count = len(self.reviews)
            temp_sum = self.grade * review_count
            self.grade = (temp_sum - review.rating  ) / review_count

    def get_values(self):
        return [self.title, self.director, self.release_year, self.genre, self.grade, self.description]
    def get_string_values(self):
        return [self.title, self.director.full_name(), str(self.release_year), self.genre.name, str(self.grade), self.description, str(self.watched)]

    def print_reviews(self):
        for review in self.reviews:
            print(f"ID: {review.id} User: {review.user}, rating: {review.rating}, text: {review.text}")