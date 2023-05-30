import numpy as np
import itertools
from main import Sudoku, Cell



trial = [[0,0,0,6,8,0,1,9,0],[2,6,0,0,7,0,0,0,4],
         [7,0,1,0,9,0,5,0,0],[8,2,0,0,0,4,0,5,0],
         [1,0,0,6,0,2,0,0,3],[0,4,0,9,0,0,0,2,8],
         [0,0,9,0,4,0,7,0,3],[3,0,0,0,5,0,0,1,8],
         [0,7,4,0,3,6,0,0,0]]

#board = input("Enter your sudoku puzzle: ")
PUZZLE = Sudoku(trial)

for cell in range(len(trial)):
    PUZZLE.AllAgents[cell].permutation = trial[cell]

def initialize_cells():
    for agent in PUZZLE.AllAgents:
        #agent.cull_domain()
        agent.permutation = agent.domain[0]

initialize_cells()

solved = False
while not solved:
    print('here goes nothing')
    for agent in PUZZLE.AllAgents:
        #agent.check_agent_view()
        try:
            agent.send_receive_OK(agent.position, agent.permutation, list(range(agent.position+1, 9)))
        except Exception as e:
            print(e)
            quit()
        print('one agent complete')
    solved = PUZZLE.is_valid()

if solved:
    for agent in PUZZLE.AllAgents:
        print(agent.permutation)