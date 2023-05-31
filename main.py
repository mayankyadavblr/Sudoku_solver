import numpy as np
import itertools
from queue import Queue
import time
import traceback

class Sudoku:

    def setup():
        list_of_agents = []
        for row in range(1, 4):
            for column in range(1, 4):
                list_of_agents += [Cell(len(list_of_agents), row, column, trial[len(list_of_agents)])]

        print("set up done")
        return list_of_agents

    def __init__(self, matrix):
        self.puzzle = matrix
        self.puzzle_transpose = np.array(matrix).T.tolist()
        self.AllAgents = Sudoku.setup()

    def is_valid(self):

        # valid or not for rows
        freq_dict = []
        for row in self.puzzle:
            for cell in row:
                if cell != 0:    
                    if cell in freq_dict:
                        print("False")
                        return False
                freq_dict += [cell]
            freq_dict = []      
                
        # valid or not for columns
        freq_dict = []
        for row in np.array(self.puzzle).T.tolist():
            for cell in row:
                if cell != 0:    
                    if cell in freq_dict:
                        print("False")
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
                                print("False")
                                return False
                        freq_dict += [row[j]]
                freq_dict = []
        print("True")
        return True
        
    def compare_agents(self, permutation, agent2):
        valid = [[0], []]
        if self.intersection(permutation[0:3], agent2[0:3]) in valid:
            if self.intersection(permutation[3:6], agent2[3:6]) in valid:
                if self.intersection(permutation[6:9], agent2[6:9]) in valid:
                    return True
        return False

    def intersection(self, lst1, lst2):
        return list(set(lst1) & set(lst2))
    


class Cell(Sudoku):

    Domain = list(itertools.permutations(list(range(1, 10))))
    #AllAgents = setup() #Potential problem with setup running multiple times

    def __init__(self, pos, x, y, permutation_orig):
        self.position = pos
        self.coordinates = [x, y]
        self.agent_view = {}
        self.NoGood = []
        self.permutation = permutation_orig
        self.domain = []
        self.queue = Queue()
        self.advanced_cull_domain()


    def send_receive_OK(self, pos,  new_permutation):
        
        self.agent_view[pos] = new_permutation
        self.check_agent_view()
        '''
        print(self.position, children)
        for agent in children:
            PUZZLE.AllAgents[agent].agent_view[pos] = new_permutation
            #PUZZLE.AllAgents[agent].check_agent_view()
        '''

    def send_receive_NoGood(self, inconsistent_set):
        self.NoGood += [inconsistent_set]
        #receiver.check_agent_view()
        self.check_agent_view()
            
    def check_agent_view(self):
        def check_consistency(permutation):
            for agent in self.agent_view.keys():
                if (self.coordinates[0] == PUZZLE.AllAgents[agent].coordinates[0]) or (self.coordinates[1] == PUZZLE.AllAgents[agent].coordinates[1]):
                    if not self.compare_agents(permutation, self.agent_view[agent]):
                        return False
            return True

        if (not check_consistency(self.permutation)) or (0 in self.permutation):

            found = False
            for permutation in self.domain:

                if permutation != self.permutation:

                    if check_consistency(permutation):

                        for agent in range(self.position+1, 9):
                            PUZZLE.AllAgents[agent].queue.put([self.position, permutation, PUZZLE.AllAgents[agent], lambda x, y, z: z.send_receive_OK(x, y)])
                        
                        #self.send_receive_OK(self.position, permutation, list(range(self.position+1, 9)))
                        found = True
                        self.permutation = permutation

                if found:
                    break

            if not found:
                self.backtrack()

    def backtrack(self):
        '''
        if inconsistency.isEmpty():
            print("No Solution, press ctrl+C")
            quit()
        else:
        '''
        iterable = list(self.agent_view.keys()).copy()
        iterable.sort(reverse=True)
        for agent in iterable:
                if (self.coordinates[0] == PUZZLE.AllAgents[agent].coordinates[0]) or (self.coordinates[1] == PUZZLE.AllAgents[agent].coordinates[1]):
                    if not self.compare_agents(self.permutation, self.agent_view[agent]):
                        break
        #least_priority = max(self.agent_view.keys())
        least_priority = agent
        #self.send_receive_NoGood(self.agent_view) # removed PUZZLE.AllAgents[least_priority],
        PUZZLE.AllAgents[least_priority].queue.put([self.agent_view, lambda x: PUZZLE.AllAgents[least_priority].send_receive_NoGood(x)])

        #self.agent_view[least_priority] = PUZZLE.puzzle[least_priority]
        self.agent_view.pop(least_priority)
        self.check_agent_view()


    def queue_control(self):
        print(self.agent_view)
        while not self.queue.empty():
            temp = self.queue.get()
            if len(temp) == 4:
                temp[3](temp[0], temp[1], temp[2])
            elif len(temp) == 2:#RECHECK THIS
                temp[1](temp[0])
        #print(self.agent_view)
        self.check_agent_view()
        print(self.permutation, self.position)


    def advanced_cull_domain(self):
        pos_dict = {}
        for i in self.permutation:
            if i != 0:
                pos_dict[i] = self.permutation.index(i)


        present = set(self.permutation)
        required = set([1, 2, 3, 4, 5, 6, 7, 8, 9]).difference(present)

        for domain_point in list(itertools.permutations(required)):
            domain_point = list(domain_point)
            for key in pos_dict:
                domain_point.insert(pos_dict[key], key)

            self.domain += [domain_point]
        #print(pos_dict, len(self.domain))
    
    def cull_domain(self):
    
        pos_dict = {}
        for i in self.permutation:
            if i != 0:
                pos_dict[i] = self.permutation.index(i)

        print(pos_dict)
        for permutation in Cell.Domain:
            for key in pos_dict:
                if permutation.index(key) != pos_dict[key]:
                    #print(permutation)
                    self.domain.remove(permutation)
                    break
        print("culling domain done", self.position, len(self.domain))


trial = [[0,0,0,6,8,0,1,9,0],[2,6,0,0,7,0,0,0,4],
         [7,0,1,0,9,0,5,0,0],[8,2,0,0,0,4,0,5,0],
         [1,0,0,6,0,2,0,0,3],[0,4,0,9,0,0,0,2,8],
         [0,0,9,0,4,0,7,0,3],[3,0,0,0,5,0,0,1,8],
         [0,7,4,0,3,6,0,0,0]]

#board = input("Enter your sudoku puzzle: ")
PUZZLE = Sudoku(trial)
print(PUZZLE.compare_agents([1,4,3,9,5,6,7,2,8],[1,0,0,6,0,2,0,0,3]), PUZZLE.AllAgents[5].domain[0])
for cell in range(len(trial)):
    PUZZLE.AllAgents[cell].permutation = trial[cell]

def initialize_cells():
    for agent in PUZZLE.AllAgents:
        #agent.cull_domain()
        agent.permutation = agent.domain[0]
        for agent1 in range(agent.position+1, 9):
            PUZZLE.AllAgents[agent1].queue.put([agent.position, agent.permutation, PUZZLE.AllAgents[agent1], lambda x, y, z: z.send_receive_OK(x, y)])
    pass

initialize_cells()

solved = False
cycle = 0


while not solved:
    print('here goes nothing')
    '''
    for agent in PUZZLE.AllAgents:
        #agent.check_agent_view()
        try:
            #agent.send_receive_OK(agent.position, agent.permutation, list(range(agent.position+1, 9)))
            pass
        except Exception as e:
            print(e)
            quit()
        print('one agent complete')
    solved = PUZZLE.is_valid()
    '''
    try:
        for agent in PUZZLE.AllAgents:
            agent.queue_control()
    except Exception as e:
        print(e, agent.position)
        quit()

    cycle += 1
    print(cycle)
    for agent in PUZZLE.AllAgents:
        if not agent.queue.empty():
            solved = False
    time.sleep(1)
print('phew we done baby')

