import numpy as np
import random
import itertools
from ast import literal_eval

class Sudoku:

    def __init__(self,matrix):
        self.puzzle = matrix
        self.matrix = []
        #self.set_up_cells()
        self.puzzle_transpose = np.array(matrix).T.tolist()
        self.agents = self.setup()

    def is_valid(self):

        # valid or not for rows
        freq_dict = []
        for row in self.puzzle:
            for cell in row:
                if cell != 0:    
                    if cell in freq_dict:
                        return False
                freq_dict += [cell]
            freq_dict = []      
                
        # valid or not for columns
        freq_dict = []
        for row in np.array(self.puzzle).T.tolist():
            for cell in row:
                if cell != 0:    
                    if cell in freq_dict:
                        return False
                freq_dict += [cell]
            freq_dict = [] 
        
        # valid or not for 3x3 (to be done)
        splits = [self.puzzle[0:3], self.puzzle[3:6], self.puzzle[6:9]]
        splits_verticle = [list(range(3)), list(range(3, 6)), list(range(6, 9))]

        freq_dict = []
        for i in range(3):
            for column in splits_verticle:
                for j in column:    
                    for row in splits[i]:
                        if row[j] != 0:
                            if row[j] in freq_dict:
                                return False
                        freq_dict += [row[j]]
                freq_dict = []

        return True
        
    def compare_agents(self, agent2):
        valid = [[0], []]
        if self.intersection(self[0:3], agent2[0:3]) in valid:
            if self.intersection(self[3:6], agent2[3:6]) in valid:
                if self.intersection(self[6:9], agent2[6:9]) in valid:
                    return True
        return False

    def intersection(lst1, lst2):
        return list(set(lst1) & set(lst2))
    
    def populate_agent(self):
        return random.choice(self.domain)
    
    def setup(self):
        list_of_agents = []
        for row in range(1, 4):
            for column in range(1, 4):
                list_of_agents += [Cell(len(list_of_agents), row, column)]

        return list_of_agents

        

class Cell(Sudoku):

    def __init__(self, pos, x, y):
        self.position = pos
        self.coordinates = [x, y]
        self.agent_view = {}
        self.NoGood = []
        self.permutation = []
        self.domain = list(itertools.permutations(list(range(1, 10))))

    def check_agent_view(self):
        for agent in self.agents[0: self.pos]:
            pass

    def backtrack(self):
        pass


