import numpy as np


class Solution(object):
    def isValidSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: bool
        """
        # valid or not for rows
        freq_dict = []
        for row in board:
            for cell in row:
                if cell != ".":    
                    if cell in freq_dict:
                        return False
                freq_dict += [cell]
            freq_dict = []      
                
        # valid or not for columns
        freq_dict = []
        for row in np.array(board).T.tolist():
            for cell in row:
                if cell != ".":    
                    if cell in freq_dict:
                        return False
                freq_dict += [cell]
            freq_dict = [] 
        
        # valid or not for 3x3 (to be done)
        splits = [board[0:3], board[3:6], board[6:9]]
        splits_verticle = [list(range(3)), list(range(3, 6)), list(range(6, 9))]

        freq_dict = []
        for i in range(3):
            for column in splits_verticle:
                for j in column:    
                    for row in splits[i]:
                        if row[j] != ".":
                            if row[j] in freq_dict:
                                return False
                        freq_dict += [row[j]]
                freq_dict = []

        return True
