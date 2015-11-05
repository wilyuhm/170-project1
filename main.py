import sys
import copy

key_row_1 = [1,2,3]
key_row_2 = [4,5,6]
key_row_3 = [7,8,'b']
key_puzzle = [key_row_1, key_row_2, key_row_3]

def move_blank_left(const_puzzle):
	_puzzle = const_puzzle
	for row in _puzzle: 
		if 'b' in row:
			b_index = row.index('b')
			if b_index != 0:
				temp = row[b_index-1]
				row[b_index-1] = row[b_index] 
				row[b_index] = temp
				return _puzzle
			else:
				return 0	


def move_blank_right(const_puzzle):
	_puzzle = const_puzzle
	for row in _puzzle: 
		if 'b' in row:
			b_index = row.index('b')
			if b_index != 2:
				temp = row[b_index+1]
				row[b_index+1] = row[b_index] 
				row[b_index] = temp
				return _puzzle
			else:
				return 0	


def move_blank_up(const_puzzle):
	_puzzle = const_puzzle
	row_index = 0
	for row in _puzzle: 
		if 'b' in row:
			if row_index == 0: #can't move up from the top
				return 0
			b_index = row.index('b')
			temp = _puzzle[row_index-1][b_index]
			_puzzle[row_index-1][b_index] = 'b'
			row[b_index] = temp 
			return _puzzle
		row_index = row_index+1
	
def move_blank_down(const_puzzle):
	_puzzle = const_puzzle
	row_index = 0
	for row in _puzzle: 
		if 'b' in row:
			if row_index == 2: #can't move down from the bottom
				return 0
			b_index = row.index('b')
			temp = _puzzle[row_index+1][b_index]
			_puzzle[row_index+1][b_index] = 'b'
			row[b_index] = temp 
			return _puzzle
		row_index = row_index+1

def get_tile_location(_puzzle, tile): #called by get_manhattan_distance, returns coordinates
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
			if(tile != 'b'):		
				(x,y) = get_tile_location(_key_puzzle, tile)
				distance += abs(key_x-x)
				distance += abs(key_y-y)	
			key_x+=1
		key_y-=1	
	return distance	

def get_misplacedtiles(_puzzle, _key_puzzle):
	if _puzzle == _key_puzzle:
		return 0
	key_y = 2
	misplaced_tiles = 0
	for row in _puzzle:
		key_x = 0
		for tile in row:
			if(tile != 'b'):		
				(x,y) = get_tile_location(_key_puzzle, tile)
				if (x,y) != (key_x, key_y):
					misplaced_tiles+=1
			key_x+=1
		key_y-=1	
	return misplaced_tiles

def print_array(a):
	for row in a:
		print row

def astar_manhattan(_puzzle, _key_puzzle):
	frontier = [] #new nodes...stores triplet (new_puzzle, g(n), h(n))
	visited = [] #already visited
	g=1 #g(n)
	numNodes = 1
	max_nodes = 1
	visiting = copy.deepcopy(_puzzle)
	print 'Expanding state: '
	print_array(visiting)
	visited.append(_puzzle)
	h=get_manhattan_distance(visiting, _key_puzzle)
	if h == 0:
		print 'Goal was the same as original'
		return (1,1,1) 
	while g<32:

		new_up = move_blank_up(copy.deepcopy(visiting))
		if new_up not in visited and new_up != 0:
			frontier.append((new_up, g,get_manhattan_distance(new_up, _key_puzzle)))
		new_down = move_blank_down(copy.deepcopy(visiting))
		if new_down not in visited and new_down != 0:
			frontier.append((new_down, g,get_manhattan_distance(new_down, _key_puzzle)))
		new_left = move_blank_left(copy.deepcopy(visiting))
		if new_left not in visited and new_left != 0:
			frontier.append((new_left, g,get_manhattan_distance(new_left, _key_puzzle)))
		new_right = move_blank_right(copy.deepcopy(visiting))
		if new_right not in visited and new_right != 0:
			frontier.append((new_right, g,get_manhattan_distance(new_right, _key_puzzle)))
		
		numNodes+=4
		tmp_len = len(frontier)
		if tmp_len > max_nodes:
			max_nodes = tmp_len
		#frontier now has all new puzzles, let's visit the best one (smallest f(n)) 
		
		smallest_gn = frontier[0][1]
		smallest_hn = frontier[0][2]
		smallest_fn = smallest_gn + smallest_hn
		smallest_fn_index = 0
		index = 0
		for node, gn, hn in frontier:
			if gn+hn < smallest_fn:
				smallest_fn = gn+hn
				smallest_gn = gn
				smallest_hn = hn
				smallest_fn_index = index
			index+=1
		#got smallest fn
		visiting = copy.deepcopy(frontier[smallest_fn_index][0])
		frontier.pop(smallest_fn_index)
		visited.append(visiting)
		if(smallest_hn == 0):
			print 'Goal!'
			return (numNodes, max_nodes, smallest_gn)
		print '\nThe best state to expand with a g(n) = ' + str(smallest_gn) + ' and a h(n) = ' + str(smallest_hn) + ' is...'
		print_array(visiting)
		print 'Expanding this node...'
		g = smallest_gn + 1
	print 'No solution'
	return


def astar_misplacedtiles(_puzzle, _key_puzzle):
	frontier = [] #new nodes...stores triplet (new_puzzle, g(n), h(n))
	visited = [] #already visited
	g=1 #g(n)
	numNodes=1
	max_nodes=1
	visiting = copy.deepcopy(_puzzle)
	print 'Expanding state: '
	print_array(visiting)
	visited.append(_puzzle)
	h=get_misplacedtiles(visiting, _key_puzzle)
	if h == 0:
		print 'Goal!'
		return
	while g<32:

		new_up = move_blank_up(copy.deepcopy(visiting))
		if new_up not in visited and new_up != 0:
			frontier.append((new_up, g,get_misplacedtiles(new_up, _key_puzzle)))
		new_down = move_blank_down(copy.deepcopy(visiting))
		if new_down not in visited and new_down != 0:
			frontier.append((new_down, g,get_misplacedtiles(new_down, _key_puzzle)))
		new_left = move_blank_left(copy.deepcopy(visiting))
		if new_left not in visited and new_left != 0:
			frontier.append((new_left, g,get_misplacedtiles(new_left, _key_puzzle)))
		new_right = move_blank_right(copy.deepcopy(visiting))
		if new_right not in visited and new_right != 0:
			frontier.append((new_right, g,get_misplacedtiles(new_right, _key_puzzle)))
		
		numNodes+=4
		tmp_len = len(frontier)
		if tmp_len > max_nodes:
			max_nodes = tmp_len
		#frontier now has all new puzzles, let's visit the best one (smallest f(n)) 
		
		smallest_gn = frontier[0][1]
		smallest_hn = frontier[0][2]
		smallest_fn = smallest_gn + smallest_hn
		smallest_fn_index = 0
		index = 0
		for node, gn, hn in frontier:
			if gn+hn < smallest_fn:
				smallest_fn = gn+hn
				smallest_gn = gn
				smallest_hn = hn
				smallest_fn_index = index
			index+=1
		#got smallest fn
		visiting = copy.deepcopy(frontier[smallest_fn_index][0])
		frontier.pop(smallest_fn_index)
		visited.append(visiting)
		if(smallest_hn == 0):
			print 'Goal!'
			return (numNodes,max_nodes,smallest_gn)
		print '\nThe best state to expand with a g(n) = ' + str(smallest_gn) + ' and a h(n) = ' + str(smallest_hn) + ' is...'
		print_array(visiting)
		print 'Expanding this node...'
		g = smallest_gn + 1
	print 'No solution'
	return

def uniform_cost_search(_puzzle, _key_puzzle):
	frontier = [] #new nodes...stores triplet (new_puzzle, g(n), h(n))
	visited = [] #already visited
	numNodes = 1
	max_nodes = 1
	g=1 #g(n)
	visiting = copy.deepcopy(_puzzle)
	print 'Expanding state: '
	print_array(visiting)
	visited.append(_puzzle)
	if visiting == _key_puzzle:
		print 'Goal! Same as start.'
		return (0,0,0)
	while g<31:
		new_up = move_blank_up(copy.deepcopy(visiting))
		if new_up not in visited and new_up != 0:
			frontier.append((new_up, g))
		new_down = move_blank_down(copy.deepcopy(visiting))
		if new_down not in visited and new_down != 0:
			frontier.append((new_down, g))
		new_left = move_blank_left(copy.deepcopy(visiting))
		if new_left not in visited and new_left != 0:
			frontier.append((new_left, g))
		new_right = move_blank_right(copy.deepcopy(visiting))
		if new_right not in visited and new_right != 0:
			frontier.append((new_right, g))
		
		numNodes+=4
		tmp_len = len(frontier)
		if tmp_len > max_nodes:
			max_nodes = tmp_len
		#frontier now has all new puzzles, let's visit the best one (smallest f(n)) 
		
		smallest_gn = frontier[0][1]
		smallest_hn = 0
		smallest_fn = smallest_gn + smallest_hn
		smallest_fn_index = 0
		index = 0
		for node, gn in frontier:
			if gn+0 < smallest_fn:
				smallest_fn = gn+hn
				smallest_gn = gn
				smallest_hn = 0
				smallest_fn_index = index
			index+=1
		#got smallest fn
		visiting = copy.deepcopy(frontier[smallest_fn_index][0])
		frontier.pop(smallest_fn_index)
		visited.append(visiting)
		if(visiting == _key_puzzle):
			print 'Goal!'
			return (numNodes, max_nodes,smallest_gn) 
		print '\nThe best state to expand with a g(n) = ' + str(smallest_gn) + ' and a h(n) = ' + str(smallest_hn) + ' is...'
		print_array(visiting)
		print 'Expanding this node...'
		g = smallest_gn + 1
	print 'No solution'
	return

#main
row1 = [1,'b',3]
row2 = [4,2,6]
row3 = [7,5,8]
default_puzzle = [row1,row2,row3]

print 'Welcome to William Keidel\'s 8-puzzle solver.'
answer = input('Type "1" to use a default puzzle, or "2" to enter your own puzzle.\n')
if answer == 1:
	puzzlechoice = 'default'
elif answer == 2:
	puzzlechoice = 'custom'
	print '\nEnter your puzzle, use a "b" or 0 to represent the blank'
	user_row1 = raw_input('Enter the first row, use space or tabs between numbers   ')
	user_row2 = raw_input('Enter the second row, use space or tabs between numbers   ')
	user_row3 = raw_input('Enter the third row, use space or tabs between numbers   ')
	x1,y1,z1 = user_row1.split()
	user_row1 = [x1,y1,z1]
	x2,y2,z2 = user_row2.split()
	user_row2 = [x2,y2,z2]
	x3,y3,z3 = user_row3.split()
	user_row3 = [x3,y3,z3]
	user_puzzle = [user_row1, user_row2, user_row3]
	for row in user_puzzle:
		for i in row:
			if i != 'b'  and i != '0':
				x = int(i)
				row[row.index(i)] = x
			else:
				row[row.index(i)] = 'b'

print 'Enter your choice of algorithm:'
print '1. Uniform Cost Search'
print '2. A* with the Misplaced Tiles heuristic'
print '3. A* with the Manhattan distance heuristic'
choice = input()
if puzzlechoice == 'default':
	puzzle = default_puzzle
else:
	puzzle = user_puzzle
n= 0
q = 0
d=0
if choice == 3:
	n,q,d = astar_manhattan(puzzle, key_puzzle)
elif choice == 2:
	n,q,d = astar_misplacedtiles(puzzle, key_puzzle)	
else:
	n,q,d = uniform_cost_search(puzzle, key_puzzle)

print '\nTo solve this problem the search algorithm expanded a total of ' + str(n) + ' nodes.'
print 'The maximum number of nodes in the queue at any one time was ' + str(q) + '.'
print 'The depth of the goal node was ' + str(d) + '.'
