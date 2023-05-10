class Sudoku:

    dec_to_bin={1:1,2:2,3:4,4:8,5:16,6:32,7:64,8:128,9:256}
    ideal=[1,2,3,4,5,6,7,8,9]

    def __init__(self,matrix):
        self.puzzle=matrix
        self.matrix=[]
        self.set_up_cells()

    def set_up_cells(self):
        for row in range(1,10):
            for cell in range(1,10):
                cell_name=f"C{row}{cell}"
                cell_name=Cell([],self.puzzle[row][cell],row,cell)
                rowToAdd=[]
                rowToAdd+=[cell_name]
            self.matrix+=[rowToAdd]

    def is_valid(self):

        # valid or not for rows
        for row in self.puzzle:
            if row!=self.ideal:
                return False
        
        # valid or not for columns
        columns=[]
        for column in range(1,10):
            for row in self.puzzle:
                columns+=[row[column]]
            if columns!=self.ideal:
                return False
            columns=[]
        
        # valid or not for 3x3 (to be done)


class Cell:

    def __init__(self,notes,value,row,column):
        self.value=value
        self.notes=notes
        self.row=row
        self.column=column