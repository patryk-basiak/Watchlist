import tkinter
from tkinter import END
from PIL import Image, ImageTk
import customtkinter
from CTkTable import *
from CTkFloatingNotifications import NotificationManager, NotifyType
import Utils
from Objects.Errors import EmptyEntry
from Objects.Movie import Movie
from Objects.Review import Review


class App(customtkinter.CTk):
    def __init__(self, user):
        super().__init__()
        self.notification_manager = NotificationManager(self)
        self.rating_slider = None
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
                                                                values=["System", "Light", "Dark"],
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

        self.search = customtkinter.CTkLabel(self.second_frame, text="Search", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.search.grid(row=1,column=0, padx=20, pady=10, sticky="e")
        self.movie_entry = customtkinter.CTkEntry(self.second_frame, width=700)
        self.movie_entry.grid(row=1, column=1, padx=20, pady=10,sticky="ew")

        self.find_button = customtkinter.CTkButton(self.second_frame, command=self.find_movies, text="Search", font=customtkinter.CTkFont(size=15, weight="bold"), width=100)
        self.find_button.grid(row=1, column=2, padx=20, pady=10, sticky="ew")

        self.sort_info = customtkinter.CTkLabel(self.second_frame, text="Sort by", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sort_info.grid(row=2,column=2, padx=20, pady=0, sticky="new")

        self.sort = customtkinter.CTkComboBox(self.second_frame, values=["Default","Director", "Year", "Title", "Genre", "Rating"],font=customtkinter.CTkFont(size=15, weight="bold"), command=self.sort)
        self.sort.grid(row=2,column=2, padx=20, pady=30, sticky="new")

        self.load_table(Utils.get_last_respond())

        self.filter_by = customtkinter.CTkLabel(self.second_frame, text="Filter by", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.filter_by.grid(row=2,column=2, padx=20, pady=70, sticky="new")

        self.genre_filter_visible = False
        self.genre_filter_button = customtkinter.CTkButton(
            self.second_frame,
            text="🔽 Genre",
            font=customtkinter.CTkFont(size=15, weight="bold"),
            command=self.toggle_genre_filter)
        self.genre_filter_button.grid(row=2, column=2, padx=10, pady=100, sticky="new")

        self.genre_filter_frame = customtkinter.CTkFrame(self.second_frame)
        self.genre_filter_frame.grid(row=2, column=2, padx=10, pady=140, sticky="new")
        self.genre_filter_frame.grid_remove()

        self.checkbox_vars = {}
        self.checkboxes = []

        self.load_genre_checkboxes()

        self.director_filter_visible = False
        self.director_checkbox_vars = {}
        self.director_checkboxes = []

        self.director_filter_button = customtkinter.CTkButton(
            self.second_frame,
            text="🔽 Directors",
            font=customtkinter.CTkFont(size=15, weight="bold"),
            command=self.toggle_director_filter)
        self.director_filter_button.grid(row=2, column=2, padx=10, pady=160, sticky="new")

        self.director_filter_frame = customtkinter.CTkFrame(self.second_frame)
        self.director_filter_frame.grid(row=2, column=2, padx=10, pady=200, sticky="new")
        self.director_filter_frame.grid_remove()

        self.load_director_checkboxes()

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

        genre_label = [x.name for x in Utils.get_all_genres()]
        self.label_genre = customtkinter.CTkLabel(self.add_movie_frame, text="Genre", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_genre.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        self.movie_genre_entry = customtkinter.CTkOptionMenu(self.add_movie_frame, values=genre_label)
        self.movie_genre_entry.grid(row=2, column=2, padx=20, pady=10, sticky="ew")

        self.label_year = customtkinter.CTkLabel(self.add_movie_frame, text="Release year", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_year.grid(row=3, column=1, padx=20, pady=10, sticky="ew",)
        self.movie_year_entry = customtkinter.CTkEntry(self.add_movie_frame)
        self.movie_year_entry.grid(row=3, column=2, padx=20, pady=10, sticky="ew")

        director_labels = [x.name + ' ' + x.surname for x in Utils.get_all_directors()]
        self.label_director = customtkinter.CTkLabel(self.add_movie_frame, text="Director",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_director.grid(row=4, column=1, padx=20, pady=10, sticky="ew")
        self.movie_director_option = customtkinter.CTkOptionMenu(self.add_movie_frame, values=director_labels)
        self.movie_director_option.grid(row=4, column=2, padx=20, pady=10, sticky="ew")

        self.label_description = customtkinter.CTkLabel(self.add_movie_frame, text="Description", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_description.grid(row=5, column=1, padx=20, pady=40, sticky="nsew")
        self.movie_description_entry = customtkinter.CTkTextbox(self.add_movie_frame, height=100)
        self.movie_description_entry.grid(row=5, column=2, padx=20, pady=10, sticky = "nsew", rowspan=2)

        self.add_movie_button = customtkinter.CTkButton(self.add_movie_frame, command = self.add_movie, text="Add movie", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.add_movie_button.grid(row=7, column=1, padx=20, pady=10, sticky = "ew", columnspan=2)

        #movieframe
        self.movie_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
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
        self.load_table(Utils.get_movie_list())
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
        self.bind("<Return>", lambda event: self.find_movies())
        respond = Utils.find_movie_by_title(self.movie_entry.get())
        self.load_table(respond)

    def display_watchlist(self):
        respond = Utils.get_user_watchlist(self.user)
        if len(respond) == 0:
            return "Watchlist is empty"
        return respond

    def get_movie_inf(self, movie):
        self.movie_frame.grid_columnconfigure(0, weight=1)
        self.movie_frame.grid_columnconfigure(1, weight=1)
        self.movie_frame.grid_columnconfigure(2, weight=1)
        self.current_movie = movie

        self.title1 = customtkinter.CTkLabel(self.movie_frame, text=f"Title: {movie.title}",
                                             font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title1.grid(row=1, column=0, padx=20, pady=10, sticky="nsew", columnspan=3)

        self.year = customtkinter.CTkLabel(self.movie_frame, text=f"Release year: {movie.release_year}",
                                           font=customtkinter.CTkFont(size=20, weight="bold"))
        self.year.grid(row=2, column=0, padx=20, pady=10, sticky="nsew", columnspan=3)

        self.genre = customtkinter.CTkLabel(self.movie_frame, text=f"Genre: {movie.genre}",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.genre.grid(row=3, column=0, padx=20, pady=10, sticky="nsew", columnspan=3)

        a = next((x for x in self.user.watch_list if x == movie), None)
        if a is not None:
            self.button_add = customtkinter.CTkButton(self.movie_frame, text="Remove from watchlist",
                                                      command=self.remove_from_watchlist,
                                                      font=customtkinter.CTkFont(size=15, weight="bold"))
        else:
            self.button_add = customtkinter.CTkButton(self.movie_frame, text="Add to watchlist",
                                                      command=self.add_to_watchlist,
                                                      font=customtkinter.CTkFont(size=15, weight="bold"))
        self.button_add.grid(row=4, column=0, padx=20,pady=10, sticky="",columnspan=3)


        self.rating_slider = customtkinter.CTkSlider(self.movie_frame, from_=0, to=5, number_of_steps=5,
                                                     command=self.update_stars,height=80, width=100,
                                                        progress_color="#242424",
                                                        fg_color="#242424",
                                                        button_color="#242424",
                                                        button_hover_color="#242424")
        self.rating_slider.set(3)
        self.rating_slider.grid(row=5, column=1, padx=15, pady=0, sticky="s")

        self.stars_label = customtkinter.CTkLabel(self.movie_frame, text="★★★☆☆",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"),
                                                  text_color="#FFD700")
        self.stars_label.grid(row=5, column=1, padx=20, pady=0, sticky="s")

        self.rating = customtkinter.CTk

        self.textbox = customtkinter.CTkTextbox(self.movie_frame, width=400, corner_radius=0, height=150)
        self.textbox.grid(row=7, column=0, sticky="we", columnspan=3, padx=20, pady=10)
        self.textbox.insert("0.0", "Give us your feedback about this movie!")

        self.button_review = customtkinter.CTkButton(self.movie_frame, text="Post review", command=self.post_review,
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
        self.button_review.grid(row=8, column=0, padx=20, pady=10, sticky="ew", columnspan=3)

        for i, x in enumerate(self.current_movie.reviews):
            self.review = customtkinter.CTkLabel(self.movie_frame, text=f"{x.user}, {x.text}, {int(x.rating)}, {x.date}",
                                                  font=customtkinter.CTkFont(size=14))
            self.review.grid(row=8 + i, column=0, sticky="we", columnspan=3, padx=20, pady=10)

    def movie_id(self, row):
        val = int(list(dict(row).values())[0])
        if val < 1:
            return
        self.movie_frame_event()
        self.get_movie_inf(Utils.get_last_respond()[val-1])

    def post_review(self):
        rew = Review(self.user,self.current_movie, self.textbox.get('1.0', END), self.rating_slider.get())
        self.current_movie.add_review(rew)


    def add_to_watchlist(self):
        self.user.add_movie(self.current_movie)
    def remove_from_watchlist(self):
        self.user.delete_movie(self.current_movie)

    def sort(self, var):
        respond = Utils.sort_by(var)
        self.load_table(respond)

    def load_table(self, respond):
        value = [["Title","Director", "Release year", "Genre", "Rating"]]
        for r in respond:
            value.append(r.get_values()[:-1])
        if self.table is not None:
            self.table.grid_remove()
        self.table = CTkTable(self.second_frame, row=len(respond) + 1, values=value, wraplength=2000,
                              command=self.movie_id)
        self.table.grid(row=2, column=0, padx=20, pady=20, columnspan=2, sticky="new")

    def add_movie(self):
        title = self.movie_title_entry.get()
        year = self.movie_year_entry.get()
        genre = next(x for x in Utils.get_all_genres() if x.name == self.movie_genre_entry.get())
        director = next(x for x in Utils.get_all_directors() if x.name + ' ' + x.surname == self.movie_director_option.get())
        description = self.movie_description_entry.get("1.0", "end").strip()
        try:
            movie = Movie(title, director,  year, genre, description)
        except (EmptyEntry,TypeError, ValueError) as e:
            return self.notification_manager.show_notification(
                str(e), NotifyType.ERROR, duration=1500)
        try:
            Utils.add_movie_object(movie)
        except Exception as e:
            return self.notification_manager.show_notification(
                str(e), NotifyType.ERROR),
        self.notification_manager.show_notification(
            "Movie added", NotifyType.SUCCESS, duration=1500)

    def update_stars(self, value):
        full_stars = int(float(value))
        empty_stars = 5 - full_stars
        stars_text = "★" * full_stars + "☆" * empty_stars
        self.stars_label.configure(text=stars_text)

    def toggle_genre_filter(self):
        self.genre_filter_visible = not self.genre_filter_visible
        if self.genre_filter_visible:
            self.genre_filter_frame.grid()
            self.genre_filter_button.configure(text="🔼 Hide genre filter", font=customtkinter.CTkFont(size=15, weight="bold"))
            self.director_filter_button.grid_remove()
            self.director_filter_frame.grid_remove()
        else:
            self.director_filter_button.grid()
            self.genre_filter_frame.grid_remove()
            self.genre_filter_button.configure(text="🔽 Genres", font=customtkinter.CTkFont(size=15, weight="bold"))

    def load_genre_checkboxes(self):
        genre_list = Utils.get_all_genres()
        for i, genre in enumerate(genre_list):
            var = customtkinter.BooleanVar()
            cb = customtkinter.CTkCheckBox(self.genre_filter_frame,
                                           text=genre.name,
                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                           variable=var,
                                           command=self.apply_genre_filter)
            cb.grid(row=i, column=2, sticky="new", pady=1)
            self.checkbox_vars[genre] = var
            self.checkboxes.append(cb)

    def apply_genre_filter(self):
        selected_genres = [g.name for g, var in self.checkbox_vars.items() if var.get()]
        all_movies = Utils.get_movie_list()

        if not selected_genres:
            result = all_movies
        else:
            result = [m for m in all_movies if m.genre.name in selected_genres]

        self.load_table(result)

    def toggle_director_filter(self):
        self.director_filter_visible = not self.director_filter_visible
        if self.director_filter_visible:
            self.genre_filter_frame.grid_remove()
            self.director_filter_frame.grid()
            self.director_filter_button.configure(text="🔼 Hide director filter",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        else:
            self.director_filter_frame.grid_remove()
            self.director_filter_button.configure(text="🔽 Directors",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))

    def load_director_checkboxes(self):
        director_list = Utils.get_all_directors()
        for i, director in enumerate(director_list):
            var = customtkinter.BooleanVar()
            cb = customtkinter.CTkCheckBox(
                self.director_filter_frame,
                text=director.full_name(),
                font=customtkinter.CTkFont(size=15, weight="bold"),
                variable=var,
                command=self.apply_director_filter
            )
            cb.grid(row=i, column=2, sticky="new", pady=1)
            self.director_checkbox_vars[director] = var
            self.director_checkboxes.append(cb)

    def apply_director_filter(self):
        selected_director = [d.full_name() for d, var in self.director_checkbox_vars.items() if var.get()]
        all_movies = Utils.get_movie_list()

        if not selected_director:
            result = all_movies
        else:
            print(selected_director)
            result = [m for m in all_movies if m.director.full_name() in selected_director]

        self.load_table(result)

