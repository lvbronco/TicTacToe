from handlers.base import BaseHandler
import tornado.web
import tornado.escape
import bcrypt

class HomeHandler(BaseHandler):
    def get(self):
        # self.write("Hello, world")
        user_id = self.get_secure_cookie("user")
        user = None
        #if user_id:
        #    user = self.db.get("""SELECT * FROM user WHERE id = %s""", user_id)

        print user

        self.render("home.html", user=user)


# class AuthLoginHandler(BaseHandler):
#     def get(self):
#         next_url = self.get_argument('next', '/')
#         self.set_cookie("redirect_after_login", next_url)
#         self.render("login.html", next_url=next_url, first_hide="signup")

#     def post(self):
#         username = self.valid("username")
#         password = self.valid("password")

#         if (self.errors):
#             return self.send_error(400, chunk={'Status' : 'Error', 'Errors' : self.errors })

#         # validate that the login works
#         user = self.mysqldb.get("""SELECT id, password FROM user WHERE username = %s""", username)

#         if (user == None):
#             return self.send_error(400, chunk={'Status' : 'Error', 'Errors' : {'alert' : 'Bad login. Username or password is incorrect.'} })

#         stored_password = user["password"][7:]
#         hashed = bcrypt.hashpw(password.encode('utf-8'), stored_password.encode('utf-8'))

#         if hashed == stored_password:
#             self.set_secure_cookie("user", str(user["id"]))
#             return self.write({'Status' : 'OK', 'redirect_url' : self.get_cookie('redirect_after_login')})
#         else:
#             return self.send_error(400, chunk={'Status' : 'Error', 'Errors' : {'alert' : 'Bad login. Username or password is incorrect.'} })


# class AuthLogoutHandler(BaseHandler):
#     def get(self):
#         self.clear_cookie("user")
#         self.redirect(self.get_argument("next", "/"))