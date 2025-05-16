class Genre:
    number = 0
    genres_by_id = {}

    def __init__(self, name, genre_id=None):
        self.name = name
        self.id = genre_id if genre_id is not None else Genre.number
        if genre_id is None:
            Genre.number += 1
        Genre.genres_by_id[self.id] = self

    @staticmethod
    def genre_from_id(n):
        n = int(n)
        return Genre.genres_by_id.get(n, Genre("Unknown", n))

    def __str__(self):
        return self.name

    def genre_from_name(name):
        for genre in Genre.genres_by_id.values():
            if genre.name.lower() == name.lower():
                return genre
        return Genre(name)