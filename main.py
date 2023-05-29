import numpy as np
import random
import itertools
from ast import literal_eval

def setup(self):
    list_of_agents = []
    for row in range(1, 4):
        for column in range(1, 4):
            list_of_agents += [Cell(len(list_of_agents), row, column)]

    return list_of_agents

class Sudoku:
    
    AllAgents = setup()

    def __init__(self,matrix):
        self.puzzle = matrix
        self.matrix = []
        self.puzzle_transpose = np.array(matrix).T.tolist()

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
    


        

class Cell(Sudoku):
    
    Domain = list(itertools.permutations(list(range(1, 10))))

    def __init__(self, pos, x, y):
        self.position = pos
        self.coordinates = [x, y]
        self.agent_view = {}
        self.NoGood = []
        self.permutation = []
        self.domain = Cell.Domain + []
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

    def send_receive_OK(self, pos, new_permutation, children):
        for agent in children:
            Sudoku.AllAgents

    def send_receive_NoGood(self, receiver, inconsistent_set):
        receiver.NoGood += [inconsistent_set]
        receiver.check_agent_view()
            
    def backtrack(self, inconsistency):
        if inconsistency.isEmpty():
            #terminate program
            pass
        else:
            least_priority = max(self.agent_view.keys())
            self.send_NoGood(Sudoku.AllAgents[least_priority], self.agent_view)
            self.agent_view[least_priority] = PUZZLE.puzzle[least_priority]
            self.check_agent_view()


    
    def cull_domain(self):
    
        pos_dict = {}
        for i in self.permutation:
            if i != 0:
                pos_dict[i] = self.permutation.index(i)

        for permutation in Cell.Domain:
            for key in pos_dict:
                if permutation.index(key) != pos_dict[key]:
                    self.domain.remove(permutation)
                    break

PUZZLE = Sudoku()