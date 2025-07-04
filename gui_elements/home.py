import random

import customtkinter

import Utils
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageTk

class Home(customtkinter.CTkFrame):
    def __init__(self, user, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.user = user
        self.current_theme = customtkinter.get_appearance_mode()

        self.text_color = "white" if self.current_theme == "Dark" else "black"
        self.recommendation_color = "lightblue" if self.current_theme == "Dark" else "green"

        self.welcome_label = customtkinter.CTkLabel(
            self,
            text=f"🎬 Welcome, {user.login}!",
            font=("Arial", 20, "bold"),
            text_color=self.text_color,
        )
        print(self.current_theme)
        self.welcome_label.grid(row=0, column=1, padx=20, pady=(20, 10))
        total_movies = len(Utils.movie_list)
        total_label = customtkinter.CTkLabel(
            self,
            text=f"📂 Total movies in database: {total_movies}",
            font=("Arial", 14),
            text_color=self.text_color
        )
        total_label.grid(row=1, column=1, padx=20, pady=5)

        watchlist_count = len(user.watch_list)
        watchlist_label = customtkinter.CTkLabel(
            self,
            text=f"📝 Your watchlist: {watchlist_count} movies",
            font=("Arial", 14),
            text_color=self.text_color
        )
        watchlist_label.grid(row=2, column=1, padx=20, pady=5)

        recommended_movie = Utils.get_recommended_movie(user)
        self.recommendation_label = customtkinter.CTkLabel(
            self,
            text=f"⭐ Your recommendation: {recommended_movie.title}",
            font=("Arial", 14, "italic"),
            text_color=self.recommendation_color
        )
        self.recommendation_label.grid(row=3, column=1, padx=20, pady=(10, 20))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        chart_frame = customtkinter.CTkFrame(
            self,
            fg_color="#1a1a1a",
            corner_radius=12,
            border_width=2,
            border_color="gray30"
        )
        chart_frame.grid(row=4, column=0, padx=20, pady=10)

        second_chart = customtkinter.CTkFrame(
            self,
            fg_color="#1a1a1a",
            corner_radius=12,
            border_width=2,
            border_color="gray30"
        )
        second_chart.grid(row=4, column=1, padx=20, pady=10)

        third_chart = customtkinter.CTkFrame(
            self,
            fg_color="#1a1a1a",
            corner_radius=12,
            border_width=2,
            border_color="gray30"
        )
        third_chart.grid(row=4, column=2, padx=20, pady=10)

        self.image = self.load_chart_watchlist()
        self.logo_image = customtkinter.CTkImage(self.image, size=(300, 300))
        self.chart_label = customtkinter.CTkLabel(chart_frame, text="", image=self.logo_image)
        self.chart_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.image_watched = self.load_chart_watchlist_is_watched()
        self.image_watched_chart = customtkinter.CTkImage(self.image_watched, size=(300, 300))
        self.chart_label_watched = customtkinter.CTkLabel(second_chart, text="", image=self.image_watched_chart)
        self.chart_label_watched.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.image_genres = self.the_best_genre()
        self.image_genres_chart = customtkinter.CTkImage(self.image_genres, size=(300, 300))
        self.chart_label_genres = customtkinter.CTkLabel(third_chart, text="", image=self.image_genres_chart)
        self.chart_label_genres.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    def load_chart_watchlist(self):
        dane = Utils.get_genre_from_watchlist(self.user)
        kolory = self.random_color(len(dane))

        return self.load_chart(dane, 'Number', 'Genre', kolory, 'Genre in watchlist')

    def random_color(self, n):
        return [f"#{random.randint(50, 255):02x}{random.randint(50, 255):02x}{random.randint(50, 255):02x}" for _ in
                range(n)]

    def load_chart_watchlist_is_watched(self):
        dane = Utils.get_user_watchlist_watched(self.user)
        kolory = self.random_color(len(dane))

        return self.load_chart(dane, 'Count', 'Watched?', kolory, 'Watched movie in Watchlist')

    def the_best_genre(self):
        dane = Utils.get_the_best_genre()
        kolory = self.random_color(len(dane))

        return self.load_chart(dane, 'Rating', 'Genre', kolory, 'The best genres by rating')

    def update_charts(self):
        new_image1 = self.load_chart_watchlist()
        self.logo_image = customtkinter.CTkImage(new_image1, size=(300, 300))
        self.chart_label.configure(image=self.logo_image)

        new_image2 = self.load_chart_watchlist_is_watched()
        self.image_watched_chart = customtkinter.CTkImage(new_image2, size=(300, 300))
        self.chart_label_watched.configure(image=self.image_watched_chart)

        new_image3 = self.the_best_genre()
        self.image_genres_chart = customtkinter.CTkImage(new_image3, size=(300, 300))
        self.chart_label_genres.configure(image=self.image_genres_chart)

        self.recommendation_label.configure(text=f"⭐ Your recommendation: {Utils.get_recommended_movie(self.user).title}")

    @staticmethod
    def load_chart(dane, label_y, label_x, kolory, title):
        fig, ax = plt.subplots(facecolor='black')
        ax.set_facecolor('black')
        bars = ax.bar(dane.keys(), dane.values(), color=kolory)

        ax.set_title(title, color='white', weight='bold', size=20)
        ax.set_ylabel(label_y, color='white', weight='bold', size=15)
        ax.set_xlabel(label_x, color='white', weight='bold', size=15)
        ax.tick_params(colors='white', labelsize=10.5)
        ax.grid(axis='y', linestyle='--', alpha=0.3)

        plt.tight_layout()

        buf = BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)