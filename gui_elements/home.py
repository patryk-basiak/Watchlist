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

        welcome_label = customtkinter.CTkLabel(
            self,
            text=f"🎬 Welcome, {user.login}!",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        welcome_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        total_movies = len(Utils.movie_list)
        total_label = customtkinter.CTkLabel(
            self,
            text=f"📂 Total movies in database: {total_movies}",
            font=("Arial", 14),
            text_color="gray80"
        )
        total_label.grid(row=1, column=0, padx=20, pady=5)

        watchlist_count = len(user.watch_list)
        watchlist_label = customtkinter.CTkLabel(
            self,
            text=f"📝 Your watchlist: {watchlist_count} movies",
            font=("Arial", 14),
            text_color="gray80"
        )
        watchlist_label.grid(row=2, column=0, padx=20, pady=5)

        recommended_movie = Utils.get_recommended_movie(user)
        recommendation_label = customtkinter.CTkLabel(
            self,
            text=f"⭐ Today’s recommendation: {recommended_movie.title}",
            font=("Arial", 14, "italic"),
            text_color="lightblue"
        )
        recommendation_label.grid(row=3, column=0, padx=20, pady=(10, 20))


        chart_frame = customtkinter.CTkFrame(
            self,
            fg_color="#1a1a1a",
            corner_radius=12,
            border_width=2,
            border_color="gray30"
        )
        chart_frame.grid(row=4, column=0, padx=20, pady=10)

        self.image = self.load_chart()
        self.logo_image = customtkinter.CTkImage(self.image, size=(250, 250))
        self.chart_label = customtkinter.CTkLabel(chart_frame, text="", image=self.logo_image)
        self.chart_label.pack(padx=10, pady=10)

    def load_chart(self):
        dane = Utils.get_genre_from_watchlist(self.user)
        kolory = self.losuj_kolory(len(dane))

        plt.style.use('dark_background')

        fig, ax = plt.subplots(facecolor='black')
        ax.set_facecolor('black')
        bars = ax.bar(dane.keys(), dane.values(), color=kolory)

        ax.set_title('Genres in watchlist', color='white')
        ax.set_ylabel('Number', color='white')
        ax.set_xlabel('Genre', color='white')
        ax.tick_params(colors='white')
        ax.grid(axis='y', linestyle='--', alpha=0.3)

        plt.tight_layout()

        buf = BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)


    def losuj_kolory(self, n):
        return [f"#{random.randint(50, 255):02x}{random.randint(50, 255):02x}{random.randint(50, 255):02x}" for _ in
                range(n)]

