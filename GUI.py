import tkinter
from tkinter import END
from PIL import Image, ImageTk
import customtkinter
from CTkTable import *

import Utils
from Objects.Movie import Movie

class App(customtkinter.CTk):
    def __init__(self, user):
        super().__init__()

        self.table = None
        self.user = user
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Logo",
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"), command=self.home_button_event,
                                                 anchor="w")
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.find_movies_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                          border_spacing=10, text="Find movies",
                                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                                          hover_color=("gray70", "gray30")
                                                          , anchor="w", command=self.find_movies_event
                                                          )
        self.find_movies_button.grid(row=2, column=0, sticky="ew")

        self.watchlist_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Watchlist",
                                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        anchor="w", command=self.watchlist_event,
                                                        )
        self.watchlist_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Add movie",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                     anchor="w",command=self.frame_4_button_event,
                                                      )
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        # home
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)


        self.box = customtkinter.CTkLabel(self.home_frame,text=f"Welcome {user.login}")
        self.box.grid(row=1, column=0, padx=20,pady=10)

        #find movies
        self.second_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0,weight=1)
        self.second_frame.grid_columnconfigure(1,weight=1)
        self.second_frame.grid_columnconfigure(2,weight=1)

        self.movie_entry = customtkinter.CTkEntry(self.second_frame, width=700)
        self.movie_entry.grid(row=1, column=1, padx=20, pady=10,sticky="ew")

        self.find_button = customtkinter.CTkButton(self.second_frame, command=self.find_movies, text="Find", font=customtkinter.CTkFont(size=15, weight="bold"), width=100)
        self.find_button.grid(row=1, column=2, padx=20, pady=10, sticky="ew")

        self.sort_info = customtkinter.CTkLabel(self.second_frame, text="Sort by", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sort_info.grid(row=2,column=2, padx=20, pady=10, sticky="s")

        self.sort = customtkinter.CTkComboBox(self.second_frame, values=["Default", "Year", "Title", "Genre", "Rating"], command=self.sort)
        self.sort.grid(row=3,column=2, padx=20, pady=10, sticky="new")

        self.load_table(Utils.get_last_respond())


        # watchlist
        self.watchlist_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.watchlist_frame.grid_columnconfigure(0, weight=1)
        self.watchlist = customtkinter.CTkLabel(self.watchlist_frame, text=self.display_watchlist())
        self.watchlist.grid(row=1, column=0, padx=20, pady=10)

        #addmovie
        self.add_movie_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.add_movie_frame.grid_columnconfigure(0, weight=1)
        self.add_movie_frame.grid_columnconfigure(1, weight=1)
        self.add_movie_frame.grid_columnconfigure(2, weight=1)
        self.add_movie_frame.grid_columnconfigure(3, weight=1)

        self.label_title = customtkinter.CTkLabel(self.add_movie_frame, text="Title", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_title.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.movie_title_entry = customtkinter.CTkEntry(self.add_movie_frame)
        self.movie_title_entry.grid(row=1, column=2, padx=20, pady=10,sticky="ew")

        self.label_year = customtkinter.CTkLabel(self.add_movie_frame, text="Release year", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_year.grid(row=2, column=1, padx=20, pady=10, sticky="ew",)
        self.movie_year_entry = customtkinter.CTkEntry(self.add_movie_frame)
        self.movie_year_entry.grid(row=2, column=2, padx=20, pady=10, sticky="ew")


        self.label_genre = customtkinter.CTkLabel(self.add_movie_frame, text="Genre", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_genre.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        self.movie_genre_entry = customtkinter.CTkEntry(self.add_movie_frame)
        self.movie_genre_entry.grid(row=3, column=2, padx=20, pady=10, sticky="ew")

        self.label_description = customtkinter.CTkLabel(self.add_movie_frame, text="Description", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_description.grid(row=4, column=1, padx=20, pady=40, sticky="nsew")
        self.movie_description_entry = customtkinter.CTkTextbox(self.add_movie_frame, height=100)
        self.movie_description_entry.grid(row=4, column=2, padx=20, pady=10, sticky = "nsew", rowspan=2)

        self.add_movie_button = customtkinter.CTkButton(self.add_movie_frame, command = self.add_movie, text="Add movie", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.add_movie_button.grid(row=7, column=1, padx=20, pady=10, sticky = "ew", columnspan=2)

        #movieframe
        self.movie_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.movie_frame.grid_columnconfigure(0, weight=1)
        self.button_review = None
        self.button_add = None
        self.textbox = None
        self.current_movie = None
        self.select_frame_by_name("home")

        self.geometry("1440x480")
        self.title("WatchList")

        #logo
        self.logo = Image.open("Assets/Logo.png")
        self.ctk_logo = customtkinter.CTkImage(self.logo, size=(125, 26))
        self.add_logo = customtkinter.CTkLabel(self, image=self.ctk_logo, text="")
        self.add_logo.grid(row=0, column=0, padx=20, pady=17, sticky = "n")

        #programIcon
        self.icon = tkinter.PhotoImage(file ="Assets/WatchListIcon.png")
        self.iconphoto(True, self.icon)


    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.find_movies_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.watchlist_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.watchlist_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.watchlist_frame.grid_forget()
        if name == "frame_4":
            self.add_movie_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.add_movie_frame.grid_forget()
        if name == "movie_frame":
            self.movie_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.movie_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def find_movies_event(self):
        self.select_frame_by_name("frame_2")

    def watchlist_event(self):
        self.watchlist_frame.grid_forget()
        self.watchlist = customtkinter.CTkLabel(self.watchlist_frame, text=self.display_watchlist())
        self.watchlist.grid(row=1, column=0, padx=20, pady=10)
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def movie_frame_event(self):
        self.movie_frame.grid_forget()
        self.movie_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.movie_frame.grid_columnconfigure(0, weight=1)
        self.select_frame_by_name("movie_frame")

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def find_movies(self):
        respond = Utils.find_movie_by_title(self.movie_entry.get())
        self.load_table(respond)

    def display_watchlist(self):
        respond = Utils.get_user_watchlist(self.user)
        if len(respond) == 0:
            return "Watchlist is empty"
        return respond

    def get_movie_inf(self, movie):
        self.current_movie = movie
        self.title1 = customtkinter.CTkLabel(self.movie_frame, text=f"Title {movie.title}")
        self.title1.grid(row=1, column=0, padx=20, pady=10)
        self.year = customtkinter.CTkLabel(self.movie_frame, text=f"Release year {movie.release_year}")
        self.year.grid(row=2, column=0, padx=20, pady=10)
        self.genre = customtkinter.CTkLabel(self.movie_frame, text=f"Genre {movie.genre}")
        self.genre.grid(row=3, column=0, padx=20, pady=10)
        a = next((x for x in self.user.watch_list if x == movie), None)
        if a is not None:
            self.button_add = customtkinter.CTkButton(self.movie_frame, text="Remove from watchlist",
                                                      command=self.remove_from_watchlist)
        else:
            self.button_add = customtkinter.CTkButton(self.movie_frame, text="Add to watchlist", command=self.add_to_watchlist)
        self.button_add.grid(row=4, column=0, padx=20,pady=10)
        self.textbox = customtkinter.CTkTextbox(self.movie_frame, width=400, corner_radius=0)
        self.textbox.grid(row=5, column=0, sticky="nsew")
        self.textbox.insert("0.0", "Some example text!")
        self.button_review = customtkinter.CTkButton(self.movie_frame, text="Post review", command=self.post_review)
        self.button_review.grid(row=6, column=0, padx=20, pady=10)

    def movie_id(self, row):
        val = list(dict(row).values())[0]
        self.movie_frame_event()
        self.get_movie_inf(Utils.get_last_respond()[int(val)-1])

    def post_review(self):
        print(self.textbox.get('1.0', END))

    def add_to_watchlist(self):
        self.user.add_movie(self.current_movie)
    def remove_from_watchlist(self):
        self.user.delete_movie(self.current_movie)

    def sort(self, var):
        respond = Utils.sort_by(var)
        self.load_table(respond)

    def load_table(self, respond):
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.second_frame.grid_columnconfigure(1, weight=1)
        self.second_frame.grid_columnconfigure(2, weight=1)
        value = [["Title", "Release year", "Genre", "Rating"]]
        for r in respond:
            value.append(r.get_values()[:-1])
        if self.table is not None:
            self.table.grid_remove()
        self.table = CTkTable(self.second_frame, row=len(respond) + 1, values=value, wraplength=2000,
                              command=self.movie_id)
        self.table.grid(row=3, column=0, padx=20, pady=20, columnspan=2, sticky="we")

    def add_movie(self):
        title = self.movie_title_entry.get()
        year = self.movie_year_entry.get()
        genre = self.movie_genre_entry.get()
        description = self.movie_description_entry.get("1.0", "end").strip()

        movie = Movie(title, year, genre, description)
        print(movie)

        Utils.add_movie_object(movie)
