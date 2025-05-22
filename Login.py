import tkinter as tk
import customtkinter

from Objects.User import User


class Login(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.user = None
        self.label_username = customtkinter.CTkLabel(self, text="Username:")
        self.label_username.pack()

        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        self.label_password = customtkinter.CTkLabel(self, text="Password:")
        self.label_password.pack()

        self.entry_password = customtkinter.CTkEntry(self, show="*")
        self.entry_password.pack()

        self.btn_login = customtkinter.CTkButton(self, text="Login", command=self.login)
        self.btn_login.pack()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "password":
            print("")
            # messagebox.showinfo("Login Successful", "Welcome, Admin!")
        else:
            print("s")
            # messagebox.showerror("Login Failed", "Invalid username or password")
        self.user = User("Patryk", '123',1)

    def on_closing(self):
            self.destroy()




