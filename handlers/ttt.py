from handlers.base import BaseHandler
import tornado.web
import tornado.escape

class TicTacToeHandler(BaseHandler):
    def get(self):
        # self.write("Hello, world")

        self.render("home.html", user=user)
