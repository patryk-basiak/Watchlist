
class User:
    number = 0
    def __init__(self, login, password):
        self.watch_list = None
        self.id = User.number
        User.number += 1
        self.login = login
        self.password = password
        self.watch_list = []
        self.reviews = []

    def add_movie(self, movie):
        print("added")
        self.watch_list.append(movie)

    def delete_movie(self, movie):
        self.watch_list.remove(movie)

    def __str__(self):
        return self.login

