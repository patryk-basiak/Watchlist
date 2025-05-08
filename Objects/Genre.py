class Genre:
    number = 0
    def __init__(self, name, description):
        self.name = name
        self.id = Genre.number
        Genre.number += 1
        self.description = description