from GUI import App
from Login import Login
from Objects.User import User
from Utils import load_watchlist
from analyze.Service import load

Patryk = User("Patryk", "123", 1)
# log = Login()
# log.mainloop()
# user = log.user
load()
load_watchlist(Patryk)
a = App(Patryk)
a.mainloop()