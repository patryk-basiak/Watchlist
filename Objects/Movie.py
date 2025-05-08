class Movie:
    number = 0
    def __init__(self, title=None, release_year=None, genre_id=None, short_description=None):
        self.title = title
        self.id = Movie.number
        Movie.number += 1
        self.release_year = release_year
        self.genre = genre_id
        self.description = short_description
        self.reviews = []
    def __str__(self):
        return f"Title: {self.title}\nrelease_year: {self.release_year}, genre: {self.genre}, description: {self.description}"

    def add_review(self, review):
        self.reviews.append(review)

    def delete_review(self, review):
        self.reviews.remove(review)

    def print_reviews(self):
        print(self.title + " reviews: ")
        for review in self.reviews:
            print(f"ID: {review.id} User: {review.user}, rating: {review.rating}, text: {review.text}")