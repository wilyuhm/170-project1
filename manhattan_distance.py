#project 1 the eight puzzle

print 'Insert 8 Puzzle'
print 'Using default puzzle'

def move_blank_left(_puzzle):
	for row in _puzzle: 
		if 'b' in row:
			b_index = row.index('b')
			if b_index != 0:
				temp = row[b_index-1]
				row[b_index-1] = row[b_index] 
				row[b_index] = temp
				return	


def move_blank_right(_puzzle):
	for row in _puzzle: 
		if 'b' in row:
			b_index = row.index('b')
			if b_index != 2:
				temp = row[b_index+1]
				row[b_index+1] = row[b_index] 
				row[b_index] = temp
				return	


def move_blank_up(_puzzle):
	row_index = 0
	for row in _puzzle: 
		if 'b' in row:
			if row_index == 0: #can't move up from the top
				return
			b_index = row.index('b')
			temp = _puzzle[row_index-1][b_index]
			_puzzle[row_index-1][b_index] = 'b'
			row[b_index] = temp 
			return
		row_index = row_index+1
	
def move_blank_down(_puzzle):
	row_index = 0
	for row in _puzzle: 
		if 'b' in row:
			if row_index == 2: #can't move down from the bottom
				return
			b_index = row.index('b')
			temp = _puzzle[row_index+1][b_index]
			_puzzle[row_index+1][b_index] = 'b'
			row[b_index] = temp 
			return
		row_index = row_index+1


row1 = [1,2,3]
row2 = [4,'b',6]
row3 = [7,5,8]
puzzle = [row1,row2,row3]
move_blank_up(puzzle)
print puzzle
move_blank_left(puzzle)
print puzzle
move_blank_down(puzzle)
print puzzle
