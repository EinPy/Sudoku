from sudoku_solve import print_board, find_empty, possible, solve
from random import randint, shuffle


grid =[[0 for _ in range(9)] for _ in range(9)]
count = 0


testgrid = [[5,3,0,0,7,0,0,0,0],
			[6,0,0,1,9,5,0,0,0],
			[0,9,8,0,0,0,0,6,0],
			[8,0,0,0,6,0,0,0,3],
			[4,0,0,8,0,3,0,0,1],
			[7,0,0,0,2,0,0,0,6],
			[0,6,0,0,0,0,2,8,0],
			[0,0,0,4,1,9,0,0,5],
			[0,0,0,0,8,0,0,7,9]]

#check if grid full
#A function to check if the grid is full
def checkGrid(grid):
	for row in range(0,9):
		for col in range(0,9):
			if grid[row][col]==0:
				return False

  #We have a complete grid!
	return True 

def solve_w_count(grid):
	global count

	find = find_empty(grid)
	row, col = find
	
	for val in range(1,10):
		if possible(val, (row, col), grid):
			grid[row][col] = val
			if  checkGrid(grid):
				count += 1
				break
			else:
				if solve_w_count(grid):
					return True
					
	grid[row][col] = 0
	


numberList=[1,2,3,4,5,6,7,8,9]

def fillGrid(grid):
	global counter
	
	find = find_empty(grid)
	if not find:
		return True
	else:
		row, col = find
	
	shuffle(numberList)
	for value in numberList:
	#Check that this value has not already be used on this row
		if possible(value, (row, col), grid):
			grid[row][col]=value
			
			if fillGrid(grid):
				return True

	grid[row][col]=0             


#removing numbers
#more attempts will remove more numbers, making a more difficult grid

def createValidGrid(attempts):
	grid = [[0 for i in range(9)] for j in range(9)]
	fillGrid(grid)
	cheat = grid[8][8]
	positions = []
	for i in range(9):
		for j in range(9):
			positions.append((i,j))

	
	while attempts > 0:
		shuffle(positions)
		#find a random cell where the number is not 0
		loc = randint(0,len(positions) - 1)
		pos = positions[loc]
		positions.pop(loc)
		row, col = pos
		
		#remeber value in case it needs to be put back
		backup = grid[row][col]
		grid[row][col] = 0
		
		#copy grid to use backtracking to solve
		test_grid = []
		for row in range(0,9):
			test_grid.append([])
			for col in range(0,9):
				test_grid[row].append(grid[row][col])
				

		#count the number of posible solutions using backtracking algorithm
		count = 0
		solve_w_count(test_grid)
		#if the number of solutions is not one, it's not an indeal sudoku
		if count != 1:
			grid[row][col] = backup
			positions.append(pos)
			attempts -= 1
		
	print('done')
	print_board(test_grid)
	grid[8][8] = cheat
	return grid


if __name__ == "__main__":
	fillGrid(grid)
	print_board(grid)
	product = createValidGrid(20)
	print_board(product)
	product[8][8] = grid[8][8]
	print_board(product)
	for i in range(9):
		for j in range(9):
			if not possible(product[i][j], (i,j), product) and product[i][j] != 0:
				print('unvalid board')
 



