from handlers.base import BaseHandler
import tornado.web
import tornado.escape
import json
import os.path
from model.tictactoe import TicTacToe

class TicTacToeHandler(BaseHandler):
	def post(self):
		# Check Token
		token = self.get_argument("token", None)
		
		### NOTE: I didn't have time to set up the slack channel to get the token
		#if token != valid_token_id
		#	return self.send_error(500)

		# Load Saved Games Into Memory
		# This is a simplicity design for small project, a datastore like sql or caching like redis would be more optimal
		games = self.load_games()

		# Get the command from text field
		commands = self.get_argument("text", None).split()
		command = commands[0]
		
		# The action of the command is set only if 
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

		# These Commands Need the Game to Exist
		# If not return error message
		if channel_id not in games:
			return self.write({"response_type" : "in_channel", "text" : "No game in this channel"})

		# Create game classs
		game = TicTacToe(games[channel_id])

		if command == "print":
			# Retrieve Board and Print it
			return self.write({"response_type" : "in_channel", "text" : str(game)})
		elif command == "move":
			# Attempt the move, move does all the checking if valid
			#print game
			moved = game.move(user_name, int(action))
			#print game
			if not moved:
				# Move is invalid
				return self.write({"response_type" : "in_channel", "text" : "Not your move..."})
			
			# Check if game is over
			result = game.checkBoard()
			games[channel_id] = game.export()
			self.save_games(games)
			board = str(game)

			# Game is over if result is 1 (Player O wins), or 5 (Player X wins)
			# Delete the game so a new one can be created, if there is a winner
			if result == 1:
				self.delete_game(user_name, game, games)
				return self.write({"response_type" : "in_channel", "text" : "```Player O ({}) Wins! \n {}```".format(self.playerO, board)}) 
			elif result == 5:
				self.delete_game(user_name, game, games)
				return self.write({"response_type" : "in_channel", "text" : "```Player X ({}) Wins! \n {}```".format(self.playerX, board)})
			else:
				return self.write({"response_type" : "in_channel", "text" : "```{}```".format(board)})

		# End the game
		elif command == "end":
			# Only end the game if command is from one of the players
			success = self.delete_game(user_name, channel_id, game, games)
			if success:
				return self.write({"response_type" : "in_channel", "text" : "Game Deleted"})
			else:
				return self.write({"response_type" : "in_channel", "text" : "Game Could Not Be Deleted"})


	def load_games(self):
		# Game file is just flat json file
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
		# Save the games back to the file
		### NOTE not efficent, since all games are loaded on every request so slow
		### Done for speed and ease of programming (a cache system like Redis would be better)
		f = open('saved_games', 'w')
		f.write(json.dumps(games))
		f.close()

	def delete_game(self, user_name, channel, game, games):
		# Delete the game from the file and save it
		success = False
		if user_name == game.playerO or user_name == game.playerX:
			del games[channel]
			self.save_games(games)
			success = True
		return success


