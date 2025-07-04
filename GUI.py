import tkinter
import datetime
from tkinter import END
from PIL import Image
import customtkinter
from CTkTable import *

from CTkFloatingNotifications import NotificationManager, NotifyType
import Utils
from Objects import User
from Objects.Errors import EmptyEntry
from Objects.Movie import Movie
from Objects.Review import Review
from gui_elements.home import Home
from gui_elements.watchlist import Watchlist


class App(customtkinter.CTk):
    def __init__(self, user:User):
        super().__init__()
        self.current_movie = None
        self.color = "#242424"
        self.notification_manager = NotificationManager(self)
        self.rating_slider = None
        self.table = None
        self.user = user
        self.val = 1
        self.watched_var = customtkinter.BooleanVar(value=False)
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
        self.home_frame = Home(self.user, self)

        #find movies
        self.second_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0,weight=1)
        self.second_frame.grid_columnconfigure(1,weight=1)
        self.second_frame.grid_columnconfigure(2,weight=5)

        self.search = customtkinter.CTkLabel(self.second_frame, text="Search", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.search.grid(row=1,column=0, padx=20, pady=10, sticky="e")
        self.movie_entry = customtkinter.CTkEntry(self.second_frame, width=700)
        self.movie_entry.grid(row=1, column=1, padx=20, pady=10,sticky="w")

        self.find_button = customtkinter.CTkButton(self.second_frame, command=self.find_movies, text="Search", font=customtkinter.CTkFont(size=15, weight="bold"), width=100)
        self.find_button.grid(row=1, column=2, padx=20, pady=10, sticky="ew")

        self.sort_info = customtkinter.CTkLabel(self.second_frame, text="Sort by", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sort_info.grid(row=2,column=2, padx=20, pady=0, sticky="new")

        self.sort = customtkinter.CTkComboBox(self.second_frame, values=["Default","Director", "Year", "Title", "Genre", "Rating"],font=customtkinter.CTkFont(size=15, weight="bold"), command=self.sort, state="readonly")
        self.sort.set("Default")
        self.sort.grid(row=2,column=2, padx=20, pady=30, sticky="new")

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
        self.genre_filter_frame.grid(row=2, column=2, padx=20, pady=140, sticky="new")
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
        self.director_filter_frame.grid(row=2, column=2, padx=20, pady=200, sticky="new")
        self.director_filter_frame.grid_remove()

        self.load_director_checkboxes()

        self.count_label = customtkinter.CTkLabel(self.second_frame, text=f"Displaying 10/{len(Utils.movie_list)} movies", font=customtkinter.CTkFont(size=12, slant="italic"),
                text_color="#888888",)
        self.count_label.grid(row=3,column=0, padx=10, pady=10, sticky="nsew", columnspan=3)
        # watchlist
        self.watchlist_frame = Watchlist(self, user)

        self.load_watchlist()
        self.bind("<Return>", lambda event: self.find_movies())
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

        self.add_movie_button_web = customtkinter.CTkButton(self.add_movie_frame, command = self.get_movie_from_web, text="Add movie from web [BETA]", font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="Green")
        self.add_movie_button_web.grid(row=8, column=1, padx=20, pady=10, sticky = "ew", columnspan=2)

        #movieframe
        self.movie_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.select_frame_by_name("home")

        self.geometry("1440x600")
        self.title("WatchList")

        # logo
        self.logo = Image.open("Assets/Logo.png")
        self.ctk_logo = customtkinter.CTkImage(self.logo, size=(125, 26))
        self.add_logo = customtkinter.CTkLabel(self, image=self.ctk_logo, text="")
        self.add_logo.grid(row=0, column=0, padx=20, pady=17, sticky = "n")

        # programIcon
        self.icon = tkinter.PhotoImage(file ="Assets/WatchListIcon.png")
        self.iconphoto(True, self.icon)


    def select_frame_by_name(self, name:str) -> None:
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
        self.home_frame.update_charts()

    def find_movies_event(self):
        self.load_table(Utils.get_movie_list())
        self.select_frame_by_name("frame_2")

    def watchlist_event(self):
        self.watchlist_frame.grid_forget()
        self.load_watchlist()
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def movie_frame_event(self):
        self.movie_frame.grid_forget()
        self.movie_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.movie_frame.grid_columnconfigure(0, weight=1)
        self.select_frame_by_name("movie_frame")

    def change_appearance_mode_event(self,new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.refresh_home_frame()
        if customtkinter.get_appearance_mode() == "Dark":
            self.color = "#242424"
        if customtkinter.get_appearance_mode() == "Light":
            self.color = "white"

    def find_movies(self):
        respond = Utils.find_movie_by_title(self.movie_entry.get())
        self.load_table(respond)

    def display_watchlist(self):
        respond = Utils.get_user_watchlist(self.user)
        if len(respond) == 0:
            return "Watchlist is empty"
        return respond

    def get_movie_inf(self, movie:Movie)->None:
        self.movie_frame.grid_columnconfigure(0, weight=1)
        self.movie_frame.grid_columnconfigure(1, weight=1)
        self.movie_frame.grid_columnconfigure(2, weight=1)
        self.current_movie = movie

        self.title1 = customtkinter.CTkLabel(self.movie_frame, text=f"Title: {movie.title}",
                                             font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title1.grid(row=1, column=0, padx=20, pady=10, sticky="nsew", columnspan=3)


        self.is_watched = customtkinter.CTkCheckBox(self.movie_frame, text=f"Watched?",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"), variable=self.watched_var, onvalue=True, offvalue=False, command=self.checkbox_watched)
        if self.current_movie.watched:
            self.is_watched.select()
        else:
            self.is_watched.deselect()
        self.is_watched.grid(row=1, column=0, padx=20, pady=10, sticky="w",columnspan=3)

        self.edit_button = customtkinter.CTkButton(self.movie_frame, text="Edit movie",
                                                   font=customtkinter.CTkFont(size=20, weight="bold"),
                                                   command=self.edit_movie)
        self.edit_button.grid(row=1, column=0, padx=20, pady=10, sticky="e",columnspan=3)

        self.year = customtkinter.CTkLabel(self.movie_frame, text=f"Release year: {movie.release_year}",
                                           font=customtkinter.CTkFont(size=20, weight="bold"))
        self.year.grid(row=2, column=0, padx=20, pady=10, sticky="nsew", columnspan=3)

        self.genre = customtkinter.CTkLabel(self.movie_frame, text=f"Genre: {movie.genre}",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.genre.grid(row=3, column=0, padx=20, pady=10, sticky="nsew", columnspan=3)

        self.description = customtkinter.CTkLabel(self.movie_frame, text=f"Description:\n {movie.description}",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"),wraplength=1000,
                                                  justify='center')
        self.description.grid(row=4, column=0, padx=20, pady=10, sticky="nsew", columnspan=3)

        a = next((x for x in self.user.watch_list if x[0] == movie), None)
        if a is not None:
            self.button_add = customtkinter.CTkButton(self.movie_frame, text="Remove from watchlist",
                                                      command=self.remove_from_watchlist,
                                                      font=customtkinter.CTkFont(size=15, weight="bold"))
            self.button_add.grid(row=5, column=1, padx=400, pady=10, sticky="ew")
        else:
            self.button_add = customtkinter.CTkButton(self.movie_frame, text="Add to watchlist",
                                                      command=self.add_to_watchlist,
                                                      font=customtkinter.CTkFont(size=15, weight="bold"))
            self.button_add.grid(row=5, column=1, padx=400, pady=10, sticky="ew")


        if len([x for x in self.current_movie.reviews if x.user == self.user.id]) == 0:
            self.rating_slider = customtkinter.CTkSlider(self.movie_frame, from_=0, to=5, number_of_steps=5,
                                                         command=self.update_stars,height=80, width=100,
                                                         progress_color=self.color,
                                                         fg_color=self.color,
                                                         button_color=self.color,
                                                         button_hover_color=self.color)
            self.rating_slider.set(3)
            self.rating_slider.grid(row=6, column=1, padx=15, pady=0, sticky="s")

            self.stars_label = customtkinter.CTkLabel(self.movie_frame, text="★★★☆☆",
                                                      font=customtkinter.CTkFont(size=20, weight="bold"),
                                                      text_color="#FFD700")
            self.stars_label.grid(row=6, column=1, padx=20, pady=10, sticky="s")

            self.rating = customtkinter.CTk

            self.textbox = customtkinter.CTkTextbox(self.movie_frame, width=400, corner_radius=0, height=150)
            self.textbox.grid(row=7, column=0, sticky="we", columnspan=3, padx=20, pady=10)
            self.textbox.insert("0.0", "Give us your feedback about this movie!")

            self.button_review = customtkinter.CTkButton(self.movie_frame, text="Post review", command=self.post_review,
                                                         font=customtkinter.CTkFont(size=15, weight="bold"))
            self.button_review.grid(row=8, column=0, padx=20, pady=10, sticky="ew", columnspan=3)

        for i, x in enumerate(self.current_movie.reviews):

            review_frame = customtkinter.CTkFrame(self.movie_frame, corner_radius=10, fg_color="#2a2a2a")
            review_frame.grid(row=9 + i, column=0, columnspan=4, padx=20, pady=10, sticky="we")

            # review_frame.grid_columnconfigure(1, weight=1)
            # review_frame.grid_columnconfigure(2, weight=1)
            review_frame.grid_columnconfigure(3, weight=1)

            user_label = customtkinter.CTkLabel(
                review_frame,
                text=f"{Utils.get_username_by_id(x.user)} - ⭐ {int(x.rating)}/5",
                font=customtkinter.CTkFont(size=14, weight="bold"),
                text_color="#f0db4f"
            )
            user_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))

            date_label = customtkinter.CTkLabel(
                review_frame,
                text=x.date.strftime("%d.%m.%Y %H:%M "),
                font=customtkinter.CTkFont(size=12, slant="italic"),
                text_color="#888888",
            )
            date_label.grid(row=0, column=1, sticky="w", padx=10, pady=(5, 0))

            third_chart = customtkinter.CTkFrame(
                review_frame,
                fg_color="#1a1a1a",
                corner_radius=12,
                border_width=2,
                border_color="gray30"
            )
            third_chart.grid(row=0, column=2, sticky="w", padx=10, pady=(5, 0))

            country_label = customtkinter.CTkLabel(
                third_chart,
                text="",
                image=customtkinter.CTkImage(Image.open(Utils.get_image(x.lang)), size=(30, 25)),
            )
            country_label.pack()


            if self.user.id == x.user:
                delete_button = customtkinter.CTkButton(
                    review_frame,
                    text="Delete review",
                    font=customtkinter.CTkFont(size=12),
                    command=lambda: self.delete_review(x)
                )
                delete_button.grid(row=0, column=4, sticky="e", padx=10, pady=(5, 0))
            else:
                delete_button = customtkinter.CTkButton(
                    review_frame,
                    text="Report review",
                    font=customtkinter.CTkFont(size=12),
                    command=lambda: self.report_review(x)
                )
                delete_button.grid(row=0, column=4, sticky="e", padx=10, pady=(5, 0))
            text_label = customtkinter.CTkLabel(
                review_frame,
                text=x.text,
                font=customtkinter.CTkFont(size=13),
                wraplength=600,
                justify="left"
            )
            text_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=(5, 10))

    def movie_id(self, row)->None:
        val = int(list(dict(row).values())[0])
        if val < 1:
            return
        self.val = val
        self.movie_frame_event()
        self.get_movie_inf(Utils.get_last_respond()[val-1])

    def post_review(self)->None:
        rew = Review(datetime.datetime.now(), self.user.id, self.current_movie, self.textbox.get('1.0', END), self.rating_slider.get(), Utils.test_language(self.textbox.get('1.0', END)))
        Utils.add_review(rew)
        self.movie_frame_event()
        self.get_movie_inf(Utils.get_last_respond()[self.val - 1])
        self.notification_manager.show_notification("Review posted!", NotifyType.SUCCESS, duration=1500)

    def get_movie_from_web(self):
        try:
            Utils.get_movie_from_web(self.movie_title_entry.get())
        except Exception as e:
             self.notification_manager.show_notification(str(e), NotifyType.ERROR, duration=1500)
             return
        self.notification_manager.show_notification(
            "Movie added", NotifyType.SUCCESS, duration=1500)
        self.frame_4_button_event()
    def add_to_watchlist(self):
        Utils.add_movie_to_watchlist(self.current_movie, self.user)
        self.get_movie_inf(Utils.get_last_respond()[self.val - 1])
    def remove_from_watchlist(self):
        Utils.remove_from_watchlist(self.current_movie, self.user)
        self.get_movie_inf(Utils.get_last_respond()[self.val - 1])

    def sort(self, var):
        respond = Utils.sort_by(var)
        self.load_table(respond)

    def load_table(self, respond):
        value = [["Title","Director", "Release year", "Genre", "Rating"]]
        count = len(respond)
        if len(respond) > 10:
            count = 10
            respond = respond[:10]
        for r in respond:
            value.append(r.get_values()[:-1])
        if self.table is not None:
            self.table.grid_remove()
        if len(respond) == 0:
            self.notification_manager.show_notification("No movies found", NotifyType.WARNING,
                                                        duration=1500)
            self.count_label.configure(text=f"No movies found")
            return
        self.table = CTkTable(self.second_frame, row=len(value), values=value, wraplength=2000,
                              command=self.movie_id)
        self.table.grid(row=2, column=0, padx=20, pady=20, columnspan=2, sticky="new")
        self.count_label.configure(text=f"Displaying {count}/{len(Utils.get_last_respond())} movies")

    def add_movie(self):
        title = self.movie_title_entry.get()
        year = self.movie_year_entry.get()
        genre = next(x for x in Utils.get_all_genres() if x.name == self.movie_genre_entry.get())
        director = next(x for x in Utils.get_all_directors() if x.name + ' ' + x.surname == self.movie_director_option.get())
        description = self.movie_description_entry.get("1.0", "end").strip()
        try:
            movie = Movie(title, director,  year, genre, description, None)
        except (EmptyEntry,TypeError, ValueError) as e:
            return self.notification_manager.show_notification(
                str(e), NotifyType.ERROR, duration=1500)
        try:
            Utils.add_movie(movie)
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
        result = Utils.apply_genre_filer(selected_genres)
        self.table.grid_remove()
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
            cb.grid(row=i, column=2, sticky="nw", pady=1)
            self.director_checkbox_vars[director] = var
            self.director_checkboxes.append(cb)

    def apply_director_filter(self):
        selected_director = [d.full_name() for d, var in self.director_checkbox_vars.items() if var.get()]
        result = Utils.apply_director_filer(selected_director)

        self.load_table(result)

    def load_watchlist(self):

        table_data = [["Title", "Director", "Release year", "Genre", "Rating", 'Watched', 'Added date', 'Watched date']]
        watchlist = Utils.get_user_watchlist(self.user)

        if len(watchlist) == 0:
            self.notification_manager.show_notification("No movies in watchlist", NotifyType.WARNING,
                                                        duration=1500)
            return

        for r in watchlist:
            to_append = r[0].get_values()[:-1]
            if r[0].watched:
                to_append.append("Yes")
            else:
                to_append.append("No")
            to_append.append(r[1].strftime("%d.%m.%Y %H:%M "))
            if r[0].watched_date is None:
                to_append.append("N/A")
            else:
                to_append.append(r[0].watched_date.strftime("%d.%m.%Y"))
            table_data.append(to_append)


        self.table = CTkTable(self.watchlist_frame, row=len(table_data), values=table_data,
                              wraplength=2000, command=self.get_movie_page_from_watchlist)
        self.table.grid(row=2, column=0, padx=20, pady=20, columnspan=2, sticky="new")

    def checkbox_watched(self):
        Utils.set_checkbox(self.current_movie, self.watched_var.get(), self.user)

    def delete_review(self, review):
        try:
            Utils.delete_review(review)
        except Exception as e:
            self.notification_manager.show_notification(
                str(e), NotifyType.ERROR, duration=1500)
            return
        self.movie_frame_event()
        self.get_movie_inf(Utils.get_last_respond()[self.val - 1])
        self.notification_manager.show_notification(
            "Review Deleted", NotifyType.SUCCESS, duration=1500)

    def report_review(self, review) -> None:
        try:
            Utils.report_review(review, self.user)
        except Exception as e:
            self.notification_manager.show_notification(
                str(e), NotifyType.ERROR, duration=1500)
            return
        self.notification_manager.show_notification(
            "Review Reported", NotifyType.SUCCESS, duration=1500)

    def edit_movie(self):
        self.edit_frame = customtkinter.CTkToplevel(self)
        self.edit_frame.title("Edit Movie")
        self.edit_frame.geometry("400x350")
        self.edit_frame.attributes("-topmost", True)
        self.edit_frame.resizable(False, False)
        self.edit_frame.grid_columnconfigure(0,weight=1)
        self.edit_frame.grid_columnconfigure(1,weight=1)

        customtkinter.CTkLabel(self.edit_frame, text="Edit title",font=customtkinter.CTkFont(size=20, weight="bold")
                               ).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        title_entry = customtkinter.CTkEntry(self.edit_frame)
        title_entry.insert(0, self.current_movie.title)
        title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        customtkinter.CTkLabel(self.edit_frame, text="Edit year", font=customtkinter.CTkFont(size=20, weight="bold")
                               ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        year_entry = customtkinter.CTkEntry(self.edit_frame)
        year_entry.insert(0, str(self.current_movie.release_year))
        year_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")

        customtkinter.CTkLabel(self.edit_frame, text="Edit description", font=customtkinter.CTkFont(size=20, weight="bold")
                               ).grid(row=2, column=0, padx=10, pady=10,sticky="nwe", columnspan=2)
        desc_entry = customtkinter.CTkTextbox(self.edit_frame, height=100)
        desc_entry.insert("0.0", self.current_movie.description)
        desc_entry.grid(row=3, column=0, padx=10, pady=10, sticky="new", columnspan=2)

        def save_changes():
            try:
                self.current_movie.title = title_entry.get()
                self.current_movie.release_year = int(year_entry.get())
                self.current_movie.description = desc_entry.get("1.0", "end").strip()
                Utils.update_movie(self.current_movie)
                self.notification_manager.show_notification("Movie updated", NotifyType.SUCCESS, duration=1500)
                self.edit_frame.destroy()
                self.movie_frame_event()
                self.get_movie_inf(self.current_movie)
            except Exception as e:
                self.notification_manager.show_notification(str(e), NotifyType.ERROR, duration=1500)

        save_button = customtkinter.CTkButton(self.edit_frame, text="Save changes", command=save_changes)
        save_button.grid(row=4, column=0, padx=10, pady=20, sticky="ew", columnspan=2)

    def get_movie_page_from_watchlist(self, row):
        val = int(list(dict(row).values())[0])
        if val < 1:
            return
        self.movie_frame_event()
        print(Utils.get_user_watchlist(self.user))
        self.get_movie_inf(Utils.get_user_watchlist(self.user)[val-1][0])

    def refresh_home_frame(self):
        self.home_frame.grid_forget()
        self.home_frame.destroy()
        self.home_frame = Home(self.user, self)
        self.home_frame.grid(row=0, column=1, sticky="nsew")
