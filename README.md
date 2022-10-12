# Sudoku
Sudoku game, with vizualisation of algorithm

Perosonal project using a backtracking algorithm to create a solution.

start date of project: 20.04.2020

This project showcases how you can use algorithms to manipulate the difficulty of
a sudoku board created. In addition, it vizualises how a backtracking algorithm works
to solve a sudoku board.

## Creating the grid ##
This program use a quite brute force ish approach to create a brig. It first creates a possible configuration of a grid, 
then subsequently tries to remove random indexes and checks if the board still only has one solution. 
If the board has more than one solution it backtracks to the last board that only had one solution. 

The difficulty is managed by how many times the algorithm is allowed to backtrack. Let's say the algorithm is only allowed to
"fail" once, it would create a quite easy board. However, if it is allowed to backtrack, let's say 80 times, the board will 
have a lot more empty positions, making it easier to solve. 
