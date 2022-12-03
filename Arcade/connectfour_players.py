import copy 
import math
    
RED = (255, 0, 0)
YELLOW = YELLOW = (255, 255, 0)

class ConnectFourAIPlayer:
    def __init__(self, color, connectfour):
        self.color = color
        self.connectfour = connectfour
        
        # Max depth for the minimax algorithm which decides the intelligence of the AI 
        # 1-3: Easy
        # 4-5: Normal
        # 6-8: Hard
        self.max_depth = self.connectfour.max_depth_AI

    # Assume actions are numbered 1-9
    def result(self, state, column):
        newstate = copy.deepcopy(state)
        turn = self.get_turn(state)
        
        row = 5
        while newstate[row][column] != -1:
            row -=1
        newstate[row][column] = turn
        return newstate

    def get_turn(self, state):
        empties = 0
        for row in range(6):
            for column in range(7):
                if state[row][column] == -1:
                    empties += 1
        if empties % 2 == 0:
            return RED
        else:
            return YELLOW
        
    def actions(self, state):
        moves = []
        for column in range(7):
            if state[0][column] == -1:
                moves.append(column)
        return moves

    def terminal_test(self, state):
        win = False
        for row in range(6):
            for column in range(4):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row][column + 1]) and (
                        state[row][column] == state[row][column + 2]) and (
                            state[row][column] == state[row][column + 3]) 
                if win:
                    return True
    
        for column in range(7):
            for row in range(3):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row + 1][column]) and (
                        state[row][column] == state[row + 2][column]) and (
                            state[row][column] == state[row + 3][column])
                if win:
                    return True

        for column in range(4):
            for row in range(3):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row + 1][column + 1]) and (
                        state[row][column] == state[row + 2][column + 2]) and (
                            state[row][column] == state[row + 3][column + 3])
                if win:
                    return True
                    
        for column in range(3, 7):
            for row in range(3):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row + 1][column - 1]) and (
                        state[row][column] == state[row + 2][column - 2]) and (
                            state[row][column] == state[row + 3][column - 3])
                if win:
                    return True
                
        return self.is_draw(state)
    
    def is_draw(self, state):
        for row in range(6):
            for column in range(7):
                if state[row][column] == -1:
                    return False
        return True
    
    def get_winner(self, state):
        win = False
        for row in range(6):
            for column in range(4):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row][column + 1]) and (
                        state[row][column] == state[row][column + 2]) and (
                            state[row][column] == state[row][column + 3]) 
                if win:
                    return state[row][column]
    
        for column in range(7):
            for row in range(3):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row + 1][column]) and (
                        state[row][column] == state[row + 2][column]) and (
                            state[row][column] == state[row + 3][column])
                if win:
                    return state[row][column]

        for column in range(4):
            for row in range(3):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row + 1][column + 1]) and (
                        state[row][column] == state[row + 2][column + 2]) and (
                            state[row][column] == state[row + 3][column + 3])
                if win:
                    return state[row][column]
                    
        for column in range(3, 7):
            for row in range(3):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row + 1][column - 1]) and (
                        state[row][column] == state[row + 2][column - 2]) and (
                            state[row][column] == state[row + 3][column - 3])
                if win:
                    return state[row][column]
        return None
    
    def utility(self, state):
        if self.get_winner(state) == self.color: 
            return 1000
        elif self.get_winner(state) is not None:
            return -1000
        if self.is_draw(state):
            return 0
        else:
            return self.evaluate(state)
    
    def evaluate(self, state):
        # Checking for Rows for X or O victory.
        value = 0
        if self.color == RED:
            opponent = YELLOW
        else:
            opponent = YELLOW
            
        # Prefer to start in the middle (center column) 
        lst = [state[0][3],state[1][3],state[2][3],state[3][3],state[4][3],state[5][3]]
        value += lst.count(self.color) * 10
        
        for row in range(6):
            for column in range(4):
                lst = [state[row][column],state[row][column + 1],state[row][column + 2],state[row][column + 3]]
              
                if lst.count(self.color) == 3 and lst.count(-1) == 1:
                    value += 100
                elif lst.count(self.color) == 2 and lst.count(-1) == 2:
                    value += 50
                    
                if lst.count(opponent) == 3 and lst.count(-1) == 1:
                    value -= 90
                elif lst.count(opponent) == 2 and lst.count(-1) == 2:
                    value -= 40
                    
        for column in range(7):
            for row in range(3):
                lst = [state[row][column],state[row + 1][column],state[row + 2][column],state[row + 3][column]]

                if lst.count(self.color) == 3 and lst.count(-1) == 1:
                    value += 100
                elif lst.count(self.color) == 2 and lst.count(-1) == 2:
                    value += 50
                    
                if lst.count(opponent) == 3 and lst.count(-1) == 1:
                    value -= 90
                elif lst.count(opponent) == 2 and lst.count(-1) == 2:
                    value -= 40
                    
        for column in range(4):
            for row in range(3):
                lst = [state[row][column],state[row + 1][column + 1],state[row + 2][column + 2],state[row + 3][column + 3]]

                if lst.count(self.color) == 3 and lst.count(-1) == 1:
                    value += 100
                elif lst.count(self.color) == 2 and lst.count(-1) == 2:
                    value += 50
                    
                if lst.count(opponent) == 3 and lst.count(-1) == 1:
                    value -= 90
                elif lst.count(opponent) == 2 and lst.count(-1) == 2:
                    value -= 40

        for column in range(3, 7):
            for row in range(3):
                lst = [state[row][column],state[row + 1][column - 1],state[row + 2][column - 2],state[row + 3][column - 3]]

                if lst.count(self.color) == 3 and lst.count(-1) == 1:
                    value += 100
                elif lst.count(self.color) == 2 and lst.count(-1) == 2:
                    value += 50
                    
                if lst.count(opponent) == 3 and lst.count(-1) == 1:
                    value -= 90
                elif lst.count(opponent) == 2 and lst.count(-1) == 2:
                    value -= 40
                
        return value

    def get_move(self):     
        return self.alpha_beta_search(self.connectfour.get_grid())
        
    def alpha_beta_search(self, state):
        v, action = self.max_value(0,state,-math.inf,math.inf)
        return action

    def max_value(self, depth, state, alpha, beta):
        if self.terminal_test(state) or depth == self.max_depth:
            return self.utility(state), None
        v = -math.inf
        action = 0
        for i in self.actions(state):
            v1, action1 = self.min_value(depth+1,self.result(state,i),alpha,beta)
            if v1 > v:
                v, action = v1, i
                alpha = max(alpha,v)
            if v >= beta:
                return v, action
        return v, action
    
    def min_value(self, depth, state, alpha, beta):
        if self.terminal_test(state) or depth == self.max_depth:
            return self.utility(state), None
        v = math.inf
        action = 0
        for i in self.actions(state):
            v1, action1 = self.max_value(depth+1,self.result(state,i),alpha,beta)
            if v1 < v:
                v, action = v1, i
                beta = min(beta,v)
            if v <= alpha:
                return v, action
        return v, action
    