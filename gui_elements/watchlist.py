import os
from tkinter import filedialog

import customtkinter

from CTkFloatingNotifications import NotificationManager, NotifyType


class Watchlist(customtkinter.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master,fg_color="transparent", **kwargs)
        self.user = user
        self.notification_manager = NotificationManager(master)
        self.grid_columnconfigure(0, weight=1)
        self.watchlist = customtkinter.CTkLabel(self, text="Your watchlist")
        self.watchlist.grid(row=1, column=0, padx=20, pady=10)

        self.export_button = customtkinter.CTkButton(self, text="Export watchlist", command=self.export_watchlist)
        self.export_button.grid(row=1, column=0, padx=20, pady=20)

    def export_watchlist(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save watchlist as..."
        )
        ext = os.path.splitext(filepath)[1].lower()
        sep = ' '
        if ext == ".csv":
            sep = ';'
        else:
            print("Unknown file type or user did not specify extension")
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    headers = ['Title', 'Director', 'Release year' , 'Genre', 'Rating', 'Description', 'Watched?']
                    file.write(sep.join(headers) + '\n')
                    for movie, date in self.user.watch_list:
                        file.write(f"{sep.join(movie.get_string_values())}\n")
                self.notification_manager.show_notification(
                    "Watchlist exported", NotifyType.SUCCESS, duration=1500)
            except Exception as e:
                self.notification_manager.show_notification(
                    "Error saving file", NotifyType.ERROR, duration=1500)