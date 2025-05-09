import tkinter
import customtkinter
from CTkTable import *

from Objects.Genre import Genre
from Objects.Movie import Movie

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

def load_data(data):
    movies = []
    with open(data, "r") as file:
        for line in file:
            s = line.split(";")
            movies.append(Movie(s[0],s[1],Genre.genre_from_id(s[2]),s[3]))
    return movies

mov = load_data("films.txt")
value = [x.get_values() for x in mov]
def submit():
    table.pack(expand=True, fill="both", padx=20, pady=20)
def clear():
    table.option_clear()
app = customtkinter.CTk()
app.geometry("1440x480")
app.title("WatchList")
table = CTkTable(master=app, row=len(mov), column=4, values=value)
textbox = customtkinter.CTkEntry(app)
textbox.pack()
button = customtkinter.CTkButton(app, text="Find Movies", command=submit)
button.pack()


app.mainloop()

