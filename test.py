from model.tictactoe import TicTacToe
import os.path
import json

def load_games():
		games = {}
		fname = 'saved_games'
		if not os.path.isfile(fname):
			return games

		with open(fname) as f:
			fg = f.read()
			if fg != "":
				games = json.loads(fg)
			f.close()
		return games

games = load_games()
for game in games:
	g = TicTacToe(games[game])
	print g
	print g.move("Steve", 1)
	print g.move("Steve", 4)
	print g.move("Frank", 3)
	print g
