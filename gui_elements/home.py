import customtkinter

import Utils


class Home(customtkinter.CTkFrame):
    def __init__(self, user, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.user = user
        self.box = customtkinter.CTkLabel(self, text=f"Welcome {user.login}")
        self.box.grid(row=1, column=0, padx=20, pady=10)


        welcome_label = customtkinter.CTkLabel(self, text=f"🎬 Welcome, {user.login}!", font=("Arial", 20, "bold"))
        welcome_label.grid(row=0, column=0, padx=20, pady=(20, 10))


        total_movies = len(Utils.movie_list)
        total_label = customtkinter.CTkLabel(self, text=f"📂 Total movies in database: {total_movies}")
        total_label.grid(row=1, column=0, padx=20, pady=5)


        watchlist_count = len(user.watch_list)
        watchlist_label = customtkinter.CTkLabel(self, text=f"📝 Your watchlist: {watchlist_count} movies")
        watchlist_label.grid(row=2, column=0, padx=20, pady=5)


        recommended_movie = "Random"
        recommendation_label = customtkinter.CTkLabel(self, text=f"⭐ Today’s recommendation: {recommended_movie}",
                                                      font=("Arial", 14, "italic"))
        recommendation_label.grid(row=3, column=0, padx=20, pady=(10, 20))

