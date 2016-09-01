import handlers.home
import handlers.ttt

handlers = [
    # landing pages
	(r"/", handlers.home.HomeHandler),
	(r"/tictactoe", handlers.ttt.TicTacToeHandler),
    # Auth
    #(r"/login", handlers.home.AuthLoginHandler),
    #(r"/logout", handlers.home.AuthLogoutHandler),
]