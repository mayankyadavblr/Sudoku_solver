import numpy as np
import random
import itertools

class Sudoku:

    def __init__(self,matrix):
        self.puzzle = matrix
        self.matrix = []
        #self.set_up_cells()
        self.puzzle_transpose = np.array(matrix).T.tolist()
        domain = list(itertools.permutations(list(range(9))))

    def set_up_cells(self):
        for row in range(1,10):
            for cell in range(1,10):
                cell_name=f"C{row}x{cell}"
                cell_name=Cell([],self.puzzle[row][cell],row,cell)
                rowToAdd=[]
                rowToAdd+=[cell_name]
            self.matrix+=[rowToAdd]

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
    


class Cell(Sudoku):

    def __init__(self,notes,value,row,column):
        self.value=value
        self.domain = notes
        self.row=row
        self.column=column

sudoku = []