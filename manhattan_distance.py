#project 1 the eight puzzle

key_row_1 = [1,2,3]
key_row_2 = [4,5,6]
key_row_3 = [7,8,'b']
key_puzzle = [key_row_1, key_row_2, key_row_3]

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

def get_tile_location(_puzzle, tile):
	row_index = 2
	for row in _puzzle:
		if tile in row:
			return (row.index(tile), row_index)
		row_index = row_index-1

def get_manhattan_distance(_puzzle, _key_puzzle):
	if _puzzle == _key_puzzle:
		return 0
	key_y = 2
	distance = 0
	for row in _puzzle:
		key_x = 0
		for tile in row:
			if(tile == 'b'):
				break
			(x,y) = get_tile_location(_key_puzzle, tile)
			distance += abs(key_x-x)
			distance += abs(key_y-y)	
			key_x+=1
		key_y-=1	
	return distance	


row1 = [1,2,3]
row2 = [4,'b',6]
row3 = [7,5,8]
puzzle = [row1,row2,row3]
print puzzle
print get_manhattan_distance(puzzle, key_puzzle)
move_blank_up(puzzle)
print puzzle
move_blank_left(puzzle)
print get_manhattan_distance(puzzle, key_puzzle)
print puzzle
move_blank_down(puzzle)
print get_manhattan_distance(puzzle, key_puzzle)
print puzzle
