from Objects.Movie import Movie
from Objects.Review import Review
from Objects.User import User

movie_list  = []
Titanic = Movie("Titanic", short_description="Two young lovers from completely different backgrounds meet and fall in love on the ill-fated maiden voyage of the unsinkable R.M.S. Titanic.")
movie_list.append(Titanic)
Patryk = User("Patryk", "123")
Patryk.add_movie(Movie("Minecraft"))
Patryk.add_movie(next((x for x in movie_list if x.title=="Titanic"), None))

for movie in Patryk.movie_list:
    print(movie)

Titanic.add_review(Review(Patryk, Titanic, "Good story", 5))
Titanic.print_reviews()
print("Movie find system")
def find_movie():
    m = input("Provide movie title: ")
    result = next((x for x in movie_list if x.title==m), None)
    if result is not None:
        print(result)
        return result
    else:
        print("There is not such film in our database")
find_movie()