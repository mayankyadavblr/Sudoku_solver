import numpy as np
import itertools
from main import Sudoku, Cell


board = input("Enter your sudoku puzzle: ")
PUZZLE = Sudoku(board)

for cell in range(len(board)):
    Sudoku.AllAgents[cell].permutation = board[cell]

solved = False
while not solved:
    solved = PUZZLE.is_valid()