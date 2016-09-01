from handlers.base import BaseHandler
import tornado.web
import tornado.escape
import json
import os.path
from model.tictactoe import TicTacToe

class TicTacToeHandler(BaseHandler):
	def post(self):
		games = self.load_games()
		commands = self.get_argument("text", None).split()
		command = commands[0]
		action = None
		if len(commands) > 1:
			action = commands[1]
		channel_id = self.get_argument("channel_id", None)
		user_name = self.get_argument("user_name", None)
		if command == "start":
			# Check if game is already in channel
			# if yes print game already started
			# if no create game with action being playerO and user_name playerX
			if channel_id in games:
				return self.write({"response_type" : "in_channel", "text" : "Game Already Started In Channel"})
			else:
				game = TicTacToe()
				game.playerX = user_name
				game.playerO = action
				games[channel_id] = game.export()
				self.save_games(games)
				return self.write({"response_type" : "in_channel", "text" : "Game Created Between Player X : {} and Player O : {}".format(user_name, action)})

		# print "LOOK HERE!: {}".format(games[channel_id])
		if channel_id not in games:
			return self.write({"response_type" : "in_channel", "text" : "No game in this channel"})

		game = TicTacToe(games[channel_id])
		if command == "print":
			# Retrieve Board and Print it
			return self.write({"response_type" : "in_channel", "text" : str(game)})
		elif command == "move":
			# Check if user is current player
			print game
			moved = game.move(user_name, int(action))
			print game
			if not moved:
				return self.write({"response_type" : "in_channel", "text" : "Not your move..."})
			result = game.checkBoard()
			games[channel_id] = game.export()
			self.save_games(games)
			board = str(game)
			if result == 1:
				self.delete_game(user_name, game, games)
				return self.write({"response_type" : "in_channel", "text" : "Player O Wins! \n {}".format(board)}) 
			elif result == 5:
				self.delete_game(user_name, game, games)
				return self.write({"response_type" : "in_channel", "text" : "Player X Wins! \n {}".format(board)})
			else:
				return self.write({"response_type" : "in_channel", "text" : "{}".format(board)})

		elif command == "end":
			success = self.delete_game(user_name, channel_id, game, games)
			if success:
				return self.write({"response_type" : "in_channel", "text" : "Game Deleted"})
			else:
				return self.write({"response_type" : "in_channel", "text" : "Game Could Not Be Deleted"})


	def load_games(self):
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

	def save_games(self, games):
		f = open('saved_games', 'w')
		f.write(json.dumps(games))
		f.close()

	def delete_game(self, user_name, channel, game, games):
		success = False
		if user_name == game.playerO or user_name == game.playerX:
			del games[channel]
			self.save_games(games)
			success = True
		return success


