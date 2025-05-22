from GUI import App
from Login import Login
from Objects.User import User

Patryk = User("Patryk", "123", 1)
# log = Login()
# log.mainloop()
# user = log.user

a = App(Patryk)
a.mainloop()