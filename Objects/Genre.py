class Genre:
    number = 0
    def __init__(self, name, description):
        self.name = name
        self.id = Genre.number
        Genre.number += 1
        self.description = description
    @staticmethod
    def genre_from_id(n):
        n = int(n)
        if n == 0:
            return Genre("Romance", "lorem ipsum")
    def __str__(self):
        return self.name