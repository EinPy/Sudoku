import pygame
from sudoku_solve import print_board, solve
from board_generator import createValidGrid, fillGrid, solve_w_count
import tkinter as tk

pygame.init()


x_size = 750
y_size = 580
#colours
white = (255,255,255)
lightBrown = (139,69,19)
gray = (128,128,128)
lightGray = (200,200,200)
black = (0,0,0)
red = (255,0,0)
green = (0,128,0)
mediumBlue = (121,158,196)

win = pygame.display.set_mode((x_size,y_size))

pygame.display.set_caption('sudoku')

clock = pygame.time.Clock()

class Grid:
	grid = createValidGrid(50)
			

	def __init__(self,x_start,width,height,rows,cols):
		self.x_start = x_start
		self.width = width
		self.height = height
		self.rows = rows
		self.cols = cols
		self.cubes = []
		self.model = None
		self.selected = None
		self.solution = None
		self.solution_model = None


	
	def newGrid(self, diff):
		self.grid = createValidGrid(diff)
		for row in range(9):
			for col in range(9):
				self.cubes[row][col].set_val(self.grid[row][col])
		self.update_model()
		self.create_solution()
		for i in range(9):
			for j in range(9):
				self.cubes[i][j].set_temp(0)
				self.cubes[i][j].selected = False
		self.cubes[0][0].selected = True
		
	
	def create(self):
		self.cubes = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j] = Cube(self.x_start,self.grid[i][j], i, j, self.width, self.height)

	def update_model(self):
		self.model = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
		for i in range(self.rows):
			for j in range(self.cols):
				self.model[i][j] = self.cubes[i][j].value

	def create_solution(self):		
		self.solution = []
		for row in range(0,9):
			self.solution.append([])
			for col in range(0,9):
				self.solution[row].append(self.grid[row][col])
		print('this is the board')
		print_board(self.solution)
		solve(self.solution)
		print('this is the solved version')
		print_board(self.solution)

		
	def show_solution(self):
		self.solution_model = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].set_val(self.solution[i][j])
		self.update_model()

	def place(self, val):
#		print(self.model)
		row, col = self.selected
#		print(f'checking position {row}, {col}')
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set_val(val)
			self.update_model()

#			print(f'checking the value {val} in ({row}, {col}) for')
#			print_board(self.model)

			if self.solution[row][col] ==  val:
#				print('entered')
				return True
			else:
				print('the entered value did not match solution')
				self.cubes[row][col].set_val(0)
				self.cubes[row][col].set_temp(0)
				self.update_model()
				return False

	def sketch(self, val):
		row, col = self.selected
		self.cubes[row][col].set_temp(val)

	def draw(self,win):
		#drawing the lines
		gap = self.width / 9
		for i in range(self.rows + 1):
			if i % 3 == 0 and i != 0:
				thick = 4
			else:
				thick = 1
			pygame.draw.line(win,black,  (self.x_start,i*gap), (self.width + self.x_start,i*gap), thick) #horisontal 
			pygame.draw.line(win, black, (self.x_start + i*gap,0), (self.x_start + i*gap,self.height), thick) # vertical

			#drawing the bottom line all the way across the screen
			if i == 9:
				pygame.draw.line(win,black, (0,i*gap), (self.width + self.x_start,i*gap), thick)


		#drawing the cubes
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].draw(win)

	def draw_some(self,win):
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].draw(win)


	def select(self,row,col):
		#reset other cubes from being selected
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].selected = False

		self.cubes[row][col].selected = True
		self.selected = (row,col)

	def move_selected(self,change_row,change_col):
		row, col = self.selected
		self.cubes[row][col].selected = False
#		print(f'trying to change from {row},{col} to {row - change_row}, {col - change_col}')
		if row  - change_row <= 8 and row  - change_row >= 0:
			row -= change_row
		if col  + change_col <= 8 and col + change_col >= 0:
			col += change_col
		self.cubes[row][col].selected = True
		self.selected = (row,col)

	def clear(self):
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set_temp(0)

	def click(self,pos):
		"""
		detects a click
		param: pos
		return: row, col
		"""
		if pos[0] > self.x_start:
			if pos[0] - self.x_start < self.width and pos[1] < self.height:
				gap = self.width / 9
				x = (pos[0] - self.x_start ) // gap
				y = pos[1] // gap
				return (int(y),int(x))
			else:
				return None
		else:
			return None

	def is_finished(self):
		for i in range(self.rows):
			for j in range(self.cols):
				if self.cubes[i][j] == 0:
					return False
		return True

class Cube:
	cols = 9
	rows = 9

	def __init__(self,x_start,value,row,col,width,height):
		self.x_start = x_start
		self.value = value
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.temp = 0 #the small number you can keep in the corner
		self.selected = False

	def draw(self,win):
		# drawing the numbers on the screen
		fontBig = pygame.font.SysFont('arial',40) #font for the number
		fontSketch = pygame.font.SysFont('arial', 20)

		gap = self.width / 9
		x, y = self.x_start + self.col * gap, self.row * gap

		if self.temp != 0 and self.value == 0:
			text = fontSketch.render(str(self.temp),1,gray)
			win.blit(text,(x + gap - 15,y + 5))
		elif self.value != 0:
			text = fontBig.render(str(self.value),1,black)
			win.blit(text, (x + (gap/2 - text.get_width()/2), y +(gap/2 - text.get_height()/2)))

		if self.selected:
			pygame.draw.rect(win,(255,0,0),(x,y,gap,gap),3)

	def set_val(self,val):
		self.value = val

	def set_temp(self,val):
		self.temp = val

class Interface:

	def __init__(self,):
		self.strikes = 0

	def title(self,win):
		fnt = pygame.font.SysFont('comicsans', 60)
		text = fnt.render('Sudoku', True, white)
		win.blit(text,(50,50))

	def draw_strike(self,win):
		fnt = pygame.font.SysFont('comicsans',60)
		text = fnt.render('X', True, red)
		for i in range(self.strikes):
			win.blit(text,(20 + i * (text.get_width() + 20), y_size - text.get_height() - 15))

	def add_strike(self,strike):
		self.strikes += strike
	
	def select_diff(self, board):
		root = tk.Tk()
		root.title('Selecting difficulty')
		root.geometry('400x400')


		title = tk.Label(root,
							text = "Please Select Difficulty",
							fg = "blue",
							font = "Verdana 20 bold")				
		title.place(relx = 0.5,
					rely = 0.1,
					anchor = 'center')

		difficulty1 = tk.Label(root,
								text = "Easy",
								font = "Times 20")						
		difficulty1.place(relx = 0.08,
						  rely = 0.39)
								  
		difficulty2 = tk.Label(root,
								text = "Medium",
								font = "Times 20")
		difficulty2.place(relx = 0.5,
						  rely = 1/3,
						  anchor = "center")

		difficulty3 = tk.Label(root,
								text = "Hard",
								font = "Times 20")
		difficulty3.place(relx = 0.8,
						  rely = 0.39)
					
		horizontal = tk.Scale(root, 
								from_ = 0, 
								to = 100, 
								orient = tk.HORIZONTAL, 
								length = 200)
		horizontal.place(relx = 0.5,
						 rely = 0.4,
						 anchor = "center")
		horizontal.set(50)


		def select_diffculty():
			diff = horizontal.get()
			diff = int(((diff + 20) / 2) * 1.3)
			print(f'the attempts will be {diff}')
			board.newGrid(diff)
			root.destroy()


		enter = tk.Button(root, 
							text = 'Enter', 
							command = select_diffculty,
							activebackground = "#33A532",
							font = "Verdana 20 bold",
							fg = "gray")
		enter.place(relx = 0.5,
					rely = 0.6,
					anchor = "center")

		root.mainloop()


class Button:

	def __init__(self, x, y, width, height, color, text = ''):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.color = color

	def draw(self, win, outline = None):
		#if outline, draw slightly larger rectangle around it
		if outline:
			pygame.draw.rect(win, outline, (self.x - 2, self.y - 2,self.width + 4, self.height + 4), 0)

		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

		if self.text != '' :
			font = pygame.font.SysFont('comicsans', self.height  - 20)
			text = font.render(self.text, True, lightGray)
			win.blit(text, (self.x + (self.width /2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

	def is_over(self,pos):
		#pos is a tuple of (x,y) coordinates of the mouse
		x, y = pos
		if x > self.x and x < self.x + self.width:
			if y > self.y and y < self.y + self.height:
				return True

		return False

class Visualize:

	def __init__(self, bo, win, UX, buttons):
		self.bo  = bo
		self.win = win
		self.UX = UX
		self.buttons = buttons

	def find_empty(self):
		for i in range(9):
			for j in range(9):
				if self.bo.model[i][j] == 0:
					return (i,j) #returns a tuple with (row, column)
		return None #if there are no empty spaces

	def possible(self,n,pos):
		"""
		checks if a spot is possible, if possible return True
		param y: row
		param pos: (row, column)
		param bo: board
		"""
		y, x = pos
		self.bo.select(y, x)
#		print(f'checking the position {pos}')
		#checking the row
#		print(f'checking num: {n}')
		for i in range(9):
			if self.bo.model[y][i] == n and x != i:
#				print(f'num: {n} didn\' work')
				return False
		#checking the column for the number
		for i in range(0,9):
			if self.bo.model[i][x] == n and y != i:
#				print(f'num: {n} didn\' work')
				return False
		#checking if the number exists in the same box
		x_start = (x // 3) * 3
		y_start = (y // 3) * 3
		for i in range(0,3):
			for j in range(0,3):
				if self.bo.model[y_start + i][x_start + j] == n and (y_start + i,x_start + j) != pos:
#					print(f"num: {n} didn\' work1")
					return False
#		print(f'num: {n} did work')
		return True  

	def solve(self):
		#chechking for empty spaces, if there are none, the board is solved
		find = self.find_empty()
		if not find:
			return True
		else:
			row, col = find

		for i in range(1,10):
			if self.possible(i, (row, col)):
				self.bo.cubes[row][col].set_val(i)
				self.bo.update_model()
				redrawGameWindow(self.win, self.bo, self.UX, self.buttons)

				if self.solve():
					return True # no more empty spaces, the recursion stops

				#if no number worked for the next position, go bakc to the previous position
				self.bo.cubes[row][col].set_val(0)
				self.bo.update_model()

				redrawGameWindow(self.win, self.bo, self.UX, self.buttons)

		return False



		
def redrawGameWindow(win, board, UX, buttons):
	win.fill(white)
	pygame.draw.rect(win,mediumBlue,(0,0,x_size/3,y_size-(y_size/7)+6))
	board.draw(win)
	for button in buttons:	
		button.draw(win)
	UX.draw_strike(win)
	UX.title(win)
	pygame.display.update()




def run():
	board = Grid(x_size/3,500,y_size-(y_size/7),9,9)
	board.create()
	board.create_solution()
	running = True
	new_board = Button(50,150,150,50,gray,'New Board')
	solve_button  = Button(80,250,100,50,gray,'Solve')
	vizualize_button   = Button(30,350,200,50,gray,'Visualize Solution')
	buttons = [solve_button, vizualize_button, new_board]
	key = None
	UX = Interface()
	board.update_model()
#	print(board.model)
	board.draw(win)
	while running:

		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:	
					key = 1
				if event.key == pygame.K_2:
					key = 2
				if event.key == pygame.K_3:
					key = 3
				if event.key == pygame.K_4:
					key = 4
				if event.key == pygame.K_5:
					key = 5
				if event.key == pygame.K_6:
					key = 6
				if event.key == pygame.K_7:
					key = 7
				if event.key == pygame.K_8:
					key = 8
				if event.key == pygame.K_9:
					key = 9
				if event.key == pygame.K_RIGHT:
					key = None
					board.move_selected(0, 1)
					print('right')
				if event.key == pygame.K_LEFT:
					key = None
					board.move_selected(0, -1)
					print('left')
				if event.key == pygame.K_UP:
					key = None
					board.move_selected(1,0)
					print('up')
				if event.key == pygame.K_DOWN:
					key = None
					board.move_selected(-1,0)
					print('down')
				if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
					board.clear()
					key = None
				if event.key == pygame.K_RETURN:
					i, j = board.selected
					if board.cubes[i][j].temp != 0:
						if board.place(board.cubes[i][j].temp):
							print("Sucess")
						else:
							UX.add_strike(1)
							print("Wrong")
						key = None

			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = board.click(pos)
				if solve_button.is_over(pos):
					solve_button.color = green
					print('solve button pressed')
					board.show_solution()
				if vizualize_button.is_over(pos):
					print('vizualize_button has been pressd')
					vizualize_button.color = green
					vis = Visualize(board, win, UX, buttons)
					vis.solve()
				if new_board.is_over(pos):
					print('new board button has been pressed')
					new_board.color = green
					UX.select_diff(board)
				if clicked:
					board.select(clicked[0], clicked[1])
					key = None

			if event.type == pygame.MOUSEMOTION:
				if solve_button.is_over(pos):
					solve_button.color = green
				elif vizualize_button.is_over(pos):
					vizualize_button.color = green
				elif new_board.is_over(pos):
					new_board.color = green
				else:
					for button in buttons:
						button.color = gray


		if board.selected and key != None:
			board.sketch(key)

		clock.tick(400)
		redrawGameWindow(win, board, UX, buttons)
run()
