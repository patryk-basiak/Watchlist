
class User:
    def __init__(self, login, password, no):
        self.watch_list = None
        self.id = no
        self.login = login
        self.password = password
        self.watch_list = []
        self.reviews = []

    def add_movie(self, movie, date):
        self.watch_list.append([movie, date])

    def delete_movie(self, movie):
        temp = next(x for x in self.watch_list if x[0] == movie)
        self.watch_list.remove(temp)

    def __str__(self):
        return self.login

