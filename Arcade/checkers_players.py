import copy
import math

class Piece:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True
        
class CheckersAIPlayer:
    def __init__(self, color, checkers):
        self.color = color
        self.checkers = checkers
        # Max depth for the minimax algorithm which decides the intelligence of the AI 
        # 1-3: Normal
        # 6-8: Hard
        self.max_depth = self.checkers.max_depth_AI
    
    def result(self, board, piece, move, skip):
        newstate = copy.deepcopy(board)
        row, column = move
        temp_piece = newstate.grid[piece.row][piece.column]
        newstate.move_piece(temp_piece, row, column)
        if skip is not None:
            newstate.remove_piece(skip)

        return newstate

    def evaluate(self, board):
        return board.blue_left - board.red_left + (board.blue_kings * 0.5 - board.red_kings * 0.5)
    
    # Check for double jump moves
    def could_double_jump(self, board):
        for piece in board.get_all_pieces(board.turn):
            for move, skip in board.get_valid_moves(piece).items():
                if len(skip) == 2:
                    return (piece, move, skip)
        return False
    
    # Check for jump moves
    def could_jump(self, board):
        for piece in board.get_all_pieces(board.turn):
            for move, skip in board.get_valid_moves(piece).items():
                if len(skip) == 1:
                    return (piece, move, skip)
        return False
    
    # Check for king double jump moves
    def king_double_jump(self, board):
        for piece in board.get_all_pieces(board.turn):
            if piece.king:
                for move, skip in board.get_valid_moves(piece).items():
                    if len(skip) == 2:
                        return (piece, move, skip)
        return False
    
    # Check for king jump moves
    def king_jump(self, board):
        for piece in board.get_all_pieces(board.turn):
            if piece.king:
                for move, skip in board.get_valid_moves(piece).items():
                    if len(skip) == 1:
                        return (piece, move, skip)
        return False
    
    # Check for moves to become a king piece
    def could_be_king(self, board):
        for piece in board.get_all_pieces(board.turn):
            if not piece.king:
                for move, skip in board.get_valid_moves(piece).items():
                    row, column = move
                    if row == 7 or row == 0:
                        return (piece, move, skip)
        return False
                    
    def get_move(self):
        board = self.checkers.get_board()
        
        # AI normal move
        if self.max_depth < 4:    
            if self.king_jump(board) != False:
                return self.king_jump(board)
            elif self.could_be_king(board) != False:
                return self.could_be_king(board)

        # AI hard move
        if self.max_depth > 4:
            if self.king_double_jump(board) != False:
                return self.king_jump(board)
            elif self.could_double_jump(board) != False:
                return self.could_double_jump(board)
            elif self.king_jump(board) != False:
                return self.king_jump(board)
            elif self.could_be_king(board) != False:
                return self.could_be_king(board)
            elif self.could_jump(board) != False:
                return self.could_jump(board)
            
        if self.alpha_beta_search(board) != 0:
            return self.alpha_beta_search(board)
        else:
            for piece in board.get_all_pieces(self.color):
                for move, skip in board.get_valid_moves(piece).items():
                    return (piece, move, skip)
                
    def alpha_beta_search(self, board):
        v, action = self.max_value(0, board, -math.inf, math.inf)
        return action

    def max_value(self, depth, board, alpha, beta):
        if depth == self.max_depth or board.result != None:
            return self.evaluate(board), None
        v = -math.inf
        action = 0
        for piece in board.get_all_pieces(self.color):
            for move, skip in board.get_valid_moves(piece).items():
                v1, action1 = self.min_value(depth+1, self.result(board,piece,move,skip), alpha, beta)
                if v1 > v:
                    v, action = v1, (piece,move,skip)
                    alpha = max(alpha, v)
                if v >= beta:
                    return v, action
        return v, action
    
    def min_value(self, depth, board, alpha, beta):
        if depth == self.max_depth or board.result != None:
            return self.evaluate(board), None
        v = math.inf
        action = 0
        for piece in board.get_all_pieces(self.color):
            for move, skip in board.get_valid_moves(piece).items():
                v1, action1 = self.max_value(depth+1, self.result(board,piece,move,skip), alpha, beta)
                if v1 < v:
                    v, action = v1, (piece,move,skip)
                    beta = min(beta, v)
                if v <= alpha:
                    return v, action
        return v, action