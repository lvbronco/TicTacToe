import json

class TicTacToe:
	# ## Class Variables ###

	# ## Private Instance Methods ###
	def __init__(self, bd=None):
		if bd is None:
			bd = [[0 for i in range(3)] for j in range(3)]
		else:
			bd = json.loads(bd)
		self.board = bd 
		self.playerX = None
		self.playerO = None
		self.moveNum = 0

	def export(self):
		return json.dumps(self.board)

	def printBoard(self):
		mapkey = {}
		mapkey[0] = ' '
		mapkey[1] = 'O'
		mapkey[5] = 'X'
		for i in range(3):
			print "{} | {} | {}".format(mapkey[self.board[i][0]],mapkey[self.board[i][1]],mapkey[self.board[i][2]])
			if i < 2:
				print "---------"

	def updateBoard(self, pos):
		if pos > 8:
			return
		pos_x = pos % 3
		pos_y = pos / 3

		# Player 1 is 1, Player 0 (or 2) is 5
		mov = 1
		if self.moveNum % 2 == 0:
			mov = 5
		if self.board[pos_y][pos_x] == 0:
			self.board[pos_y][pos_x] = mov
			self.moveNum += 1

		# check board status

	def checkBoard(self):
		rows = self.checkRows()
		if rows:
			return rows
		cols = self.checkCols()
		if cols:
			return cols
		dias = self.checkDias()
		if dias:
			return dias

	def checkRows(self):
		for i in range(3):
			total = sum(self.board[i])
			if total == 15:
				return 5
			elif total == 3:
				return 1
		return 0

	def checkCols(self):
		for i in range(3):
			total = 0
			for j in range(3):
				total += self.board[j][i]
			if total == 15:
				return 5
			elif total == 3:
				return 1
		return 0

	def checkDias(self):
		total = 0
		total2 = 0
		for i in range(3):
			total += self.board[i][i]
			total2 += self.board[i][2-i]
		if total == 15 or total2 == 15:
			return 5
		elif total == 3 or total2 == 3:
			return 1
		return 0

ttt = TicTacToe()
ttt.printBoard()
ttt.updateBoard(0)
# print ttt.checkBoard()
ttt.updateBoard(7)
# print ttt.checkBoard()
ttt.updateBoard(4)
# print ttt.checkBoard()
ttt.updateBoard(6)
# print ttt.checkBoard()
ttt.updateBoard(8)
print ttt.checkBoard()
ttt.printBoard()

t = ttt.export()
uuu = TicTacToe(t)
uuu.printBoard()