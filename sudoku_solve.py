#random sudoku board with just one possible solution
grid = [[5,3,0,0,7,0,0,0,0],
		[6,0,0,1,9,5,0,0,0],
		[0,9,8,0,0,0,0,6,0],
		[8,0,0,0,6,0,0,0,3],
		[4,0,0,8,0,3,0,0,1],
		[7,0,0,0,2,0,0,0,6],
		[0,6,0,0,0,0,2,8,0],
		[0,0,0,4,1,9,0,0,5],
		[0,0,0,0,8,0,0,7,9]]

def print_board(bo):
	#for every third row print a long horizontal line
	for i in range(len(bo)):
		if i % 3 == 0 and i != 0:
			print('- - - - - - - - - - - - - - - -')

		#for every third number  print a vertical line
		for j in range(len(bo[0])):
			if j % 3 == 0 and j != 0:
				print(' | ', end = '')

			#if last number of row, norwal print with new row, if not end = ''
			if j == 8:
				print(bo[i][j])
			else:
				print(f' {bo[i][j]} ', end = '')


def possible(n,pos,bo):
	"""
	checks if a spot is possible, if possible return True
	param y: row
	param pos: (row, column)
	param bo: board
	"""
	y, x = pos
	print(f'checking the position {pos}')
	#checking the row
	print(f'checking num: {n}')
	for i in range(len(bo)):
		if bo[y][i] == n and x != i:
			print(f'num: {n} didn\' work')
			return False
	#checking the column for the number
	for i in range(0,9):
		if bo[i][x] == n and y != i:
			print(f'num: {n} didn\' work')
			return False
	#checking if the number exists in the same box
	x_start = (x // 3) * 3
	y_start = (y // 3) * 3
	for i in range(0,3):
		for j in range(0,3):
			if bo[y_start + i][x_start + j] == n and (y_start + i,x_start + j) != pos:
				print(f'num: {n} didn\' work1')
				return False
	print(f'num: {n} did work')
	return True  

def find_empty(bo):
	for i in range(len(bo)):
		for j in range(len(bo[0])):
			if bo[i][j] == 0:
				return (i,j) #returns a tuple with (row, column)
	return None #if there are no empty spaces

def solve(bo):
	#chechking for empty spaces, if there are none, the board is solved
	find = find_empty(bo)
	if not find:
		return True
	else:
		row, col = find

	for i in range(1,10):
		if possible(i, (row, col), bo):
			bo[row][col] = i

			if solve(bo):
				return True # no more empty spaces, the recursion stops

			#if no number worked for the next position, go bakc to the previous position
			bo[row][col] = 0

	return False