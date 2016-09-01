# TicTacToe

Valid Commands

# start a game against [username]
### only one game per channel
start [user_name] 

# end a game
### only one of the two players can end a game
end

# print board
print

# move [num]
### positions 0-8
### 0 | 1 | 2
### 3 | 4 | 7
### 6 | 5 | 8
### only player whose turn it is can move
### messages will return Not your move if not your move
### invalid moves will be ignored
move [0-8]