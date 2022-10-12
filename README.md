# Sudoku
Sudoku game, with vizualisation of algorithm

Perosonal project using a backtracking algorithm to create a solution.

start date of project: 20.04.2020

This project showcases how you can use algorithms to manipulate the difficulty of
a sudoku board created. In addition, it vizualises how a backtracking algorithm works
to solve a sudoku board.

Demo video:
![](https://github.com/EinPy/Sudoku/blob/master/VizualiseBacktracingGif.gif)

## Creating the grid ##
This program use a quite brute force ish approach to create a brig. It first creates a possible configuration of a grid, 
then subsequently tries to remove random indexes and checks if the board still only has one solution. 
If the board has more than one solution it backtracks to the last board that only had one solution. 

The difficulty is managed by how many times the algorithm is allowed to backtrack. Let's say the algorithm is only allowed to
"fail" once, it would create a quite easy board. However, if it is allowed to backtrack, let's say 80 times, the board will 
have a lot more empty positions, making it easier to solve. 

## Solving the puzzle ##
Now, any human can solve sudoku quite efficiently, however, a computer can use a backtracking algorithm to do so with a bit more steps.
A brief overview of algorithm:

while Running:
  find first empty index
  input the lowest number that is valid at that index
    if it is valid, go to next index
    if not, try all other possible numbers at that index
    if none, are possible, backtrack to last attempted index

This can be quite hard to grasp at first, so hopefully it is clearer in the demo video. What it does, put simply,
is to attempt something at the first empty location, and than build on that in the next empty place it visits. 
If it gets to a sqauare where there are no valid inputs, it "knows" that something that was put earlier was wrong.
Therefore it backtracks and starts over again from an earlier position. 
