import copy 
import math

class TicTacToeHumanPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def is_automated(self):
        return False
    
class TicTacToeAIPlayer:
    def __init__(self, symbol, tictactoe):
        self.symbol = symbol
        self.tictactoe = tictactoe
        self.max_depth = 6  # Max depth for the minimax algorithm 

    def is_automated(self):
        return True

    # Assume actions are numbered 1-9
    def result(self, state, action):
        newstate = copy.deepcopy(state)
        turn = self.get_turn(state)

        action -= 1 # Adjustment of 1
        col = action % 3
        row = action // 3
        newstate[row][col] = turn

        return newstate

    def actions(self, state):
        moves = []
        for row in range(3):
            for col in range(3):
                if state[row][col] is None:
                    moves.append(row*3 + col + 1)
        return moves

    def terminal_test(self, state):
        for row in range(3):
            if state[row][0] is not None and state[row][0] == state[row][1] and state[row][0] == state[row][2]:
                return True
        for col in range(3):
            if state[0][col] is not None and state[0][col] == state[1][col] and state[0][col] == state[2][col]:
                return True
        if state[0][0] is not None and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
            return True
        if state[2][0] is not None and state[2][0] == state[1][1] and state[2][0] == state[0][2]:
            return True

        return self.is_draw(state)

    def is_draw(self, state):
        all_filled = True
        for row in range(3):
            for col in range(3):
                if state[row][col] is None:
                    all_filled = False
        return all_filled
    
    def utility(self, state):
        if self.get_winner(state) == self.symbol: 
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
        if self.symbol == 'X':
            opponent = 'O'
        else:
            opponent = 'X'
            
        for row in range(3) :    
            if state[row][0] is not None and state[row][0] == state[row][1] and state[row][1] == state[row][2]:       
                if state[row][0] == self.symbol:
                    value += 100
                elif state[row][0] == opponent:
                    value -= 100
 
        # Checking for Columns for X or O victory.
        for col in range(3) :
            if state[0][col] is not None and state[0][col] == state[1][col] and state[1][col] == state[2][col]:
                if state[0][col] == self.symbol:
                    value += 100
                elif state[0][col] == opponent:
                    value -= 100
 
        # Checking for Diagonals for X or O victory.
        if state[0][0] is not None and state[0][0] == state[1][1] and state[1][1] == state[2][2]:
            if state[0][0] == self.symbol:
                value += 100
            elif state[0][0] == opponent:
                value -= 100
 
        if state[0][2] is not None and state[0][2] == state[1][1] and state[1][1] == state[2][0] :
            if state[0][2] == self.symbol:
                value += 100
            elif state[0][2] == opponent:
                value -= 100
 
        # Else if none of them have won then return 0
        return value


    def get_winner(self, state):
        for row in range(3):
            if state[row][0] is not None and state[row][0] == state[row][1] and state[row][0] == state[row][2]:
                return state[row][0]
        for col in range(3):
            if state[0][col] is not None and state[0][col] == state[1][col] and state[0][col] == state[2][col]:
                return state[0][col]
        if state[0][0] is not None and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
            return state[0][0]
        if state[2][0] is not None and state[2][0] == state[1][1] and state[2][0] == state[0][2]:
            return state[2][0]

        return None 

    def get_turn(self, state):
        empties = 0
        for row in range(3):
            for col in range(3):
                if state[row][col] is None:
                    empties += 1

        if empties % 2 == 1:
            return 'X'
        else:
            return 'O'
        
    def cutoff_test(self, state, depth):
        if depth == self.max_depth:
            return True
        if self.terminal_test(state):
            return True
        return False
    
    def get_move(self):
        return self.alpha_beta_search(self.tictactoe.get_grid())
        
    def alpha_beta_search(self, state):
        v, action = self.max_value(0,state,-math.inf,math.inf)
        return action

    def max_value(self, depth, state, alpha, beta):
        if self.terminal_test(state) or self.cutoff_test(state,depth):
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
        if self.terminal_test(state) or self.cutoff_test(state,depth):
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
    