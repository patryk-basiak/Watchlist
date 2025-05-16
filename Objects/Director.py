class Director:
    number = 0
    directors_by_id = {}

    def __init__(self, name, surname, director_id=None):
        self.name = name
        self.surname = surname
        self.id = director_id if director_id is not None else Director.number

        if director_id is None:
            Director.number += 1

        Director.directors_by_id[self.id] = self

    @staticmethod
    def director_from_id(n):
        n = int(n)
        return Director.directors_by_id.get(n, Director("Unknown", "", n))

    def full_name(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.full_name()

    @staticmethod
    def director_from_full_name(fullname):
        for director in Director.directors_by_id.values():
            if director.full_name().lower() == fullname.lower():
                return director
        return Director("Unknown", "")
