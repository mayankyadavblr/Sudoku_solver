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
        
    def compare_agents(self, permutation, agent2):
        valid = [[0], []]
        if self.intersection(permutation[0:3], agent2.permutation[0:3]) in valid:
            if self.intersection(permutation[3:6], agent2.permutation[3:6]) in valid:
                if self.intersection(permutation[6:9], agent2.permutation[6:9]) in valid:
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
        Domain = list(itertools.permutations(list(range(1, 10))))
        self.domain = Domain + []
        self.cull_domain()



    def check_agent_view(self):
        def check_consistency(permutation):
            for agent in self.agents[0: self.pos]:
                if (self.coordinates[0] == agent.coordinates[0]) or (self.coordinates[1] == agent.coordinates[1]):
                    if not self.compare_agents(permutation, agent):
                        return False
            return True
        
        if not check_consistency(self.permutation):
            
            found = False
            for permutation in self.domain:
                if permutation != self.permutation:
                    if check_consistency(permutation):
                        self.send_OK()
                        found = True
                        self.permutation = permutation
                        pass
            if not found:
                self.backtrack()

    def send_OK(self):
        pass
            
    def backtrack(self):
        pass
    
    def cull_domain(self):
        pos_dict = {}
        for i in self.permutation:
            if i != 0:
                pos_dict[i] = self.permutation.index(i)

        for permutation in self.Domain:
            for key in pos_dict:
                if permutation.index(key) != pos_dict[key]:
                    self.domain.remove(permutation)
                    break