import pygame
from sudoku_solve import solve, possible, print_board
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

win = pygame.display.set_mode((x_size,y_size))

pygame.display.set_caption('sudoku')

clock = pygame.time.Clock()

class Grid:
	grid = [[5,3,0,0,7,0,0,0,0],
			[6,0,0,1,9,5,0,0,0],
			[0,9,8,0,0,0,0,6,0],
			[8,0,0,0,6,0,0,0,3],
			[4,0,0,8,0,3,0,0,1],
			[7,0,0,0,2,0,0,0,6],
			[0,6,0,0,0,0,2,8,0],
			[0,0,0,4,1,9,0,0,5],
			[0,0,0,0,8,0,0,7,9]]

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

	def create_solution(self):
		pass

	#making
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

	def place(self, val):
		print(self.model)
		row, col = self.selected
		print(f'checking position {row}, {col}')
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set_val(val)
			self.update_model()

			print(f'checking the value {val} in ({row}, {col}) for')
			print_board(self.model)

			if possible(val, (row,col), self.model) and solve(self.model):
				print('This happned')
				return True
			else:
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
			pygame.draw.line(win,black,  (self.x_start,i*gap), (self.width + self.x_start,i*gap), thick)
			pygame.draw.line(win, black, (self.x_start + i*gap,0), (self.x_start + i*gap,self.height), thick)

		#drawing the cubes
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
		print(f'trying to change from {row},{col} to {row - change_row}, {col - change_col}')
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
		if pos[0] - self.x_start < self.width and pos[1] < self.height:
			gap = self.width / 9
			x = (pos[0] - self.x_start ) // gap
			y = pos[1] // gap
			return (int(y),int(x))
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

class interface:

	def __init__(self):
		self.strikes = strikes

	def strike(self):
		fnt = pygame.font.SysFont('comicsans',40)
		


def redrawGameWindow(win,board):
	win.fill(white)
	pygame.draw.rect(win,lightBrown,(0,0,x_size/3,y_size-(y_size/7)+6))
	board.draw(win)
	pygame.display.update()




def run():
	board = Grid(x_size/3,500,y_size-(y_size/7),9,9)
	board.create()
	running = True
	key = None
	strikes = 0
	board.update_model()
	print(board.model)
	while running:

		for event in pygame.event.get():
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
							strikes += 1
							print("Wrong")
						key = None

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				clicked = board.click(pos)
				if clicked:
					board.select(clicked[0], clicked[1])
					key = None

		if board.selected and key != None:
			board.sketch(key)

		clock.tick(30)
		redrawGameWindow(win,board)
run()

