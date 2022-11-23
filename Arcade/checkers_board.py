BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STRONG_BLUE = (0, 0, 102)
BLUE = (50, 150, 200)
RED = (250, 50, 100)
GREEN = (0, 255, 0)
YELLOW = (102,102,0)

from checkers_players import Piece

class CheckersBoard():
    def __init__(self):
        self.grid = None
        self.selected = None
        self.turn = RED             # Turn of the player: {RED: player, BLUE: computer}
        self.valid_moves = {}       # Number of valid moves for the selected piece (reset when change turn)
        self.red_left = self.blue_left = 12     # Number of pieces for player and computer
        self.red_kings = self.blue_kings = 0    # Number of king pieces for player and computer
        
        self.game_over = False
        self.result = None
        self.initialize()
    
    # Initialize the grid
    def initialize(self):
        self.grid = []
        for i in range(8):
            row = []
            if i % 2 == 0:
                for j in range(8):
                    if j % 2 == 0:
                        row.append(-1)
                    elif j % 2 == 1:
                        row.append('-')
            elif i % 2 == 1:
                for j in range(8):
                    if j % 2 == 0:
                        row.append('-')
                    elif j % 2 == 1:
                        row.append(-1)
            self.grid.append(row)
        
        for i in range(3):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == -1:
                    self.grid[i][j] = Piece(i,j,BLUE)
                    
        for i in range(3):
            for j in range(len(self.grid[i+5])):
                if self.grid[i+5][j] == -1:
                    self.grid[i+5][j] = Piece(i+5,j,RED)
    
    # Select a piece based on the position passed from the player (row, column)
    def select(self, row, column):
        if row > 7 or column > 7:
            return 
        
        # If a piece is selected
        if self.selected is not None:
            result = self._make_move(row, column)
            
            # If moving the piece is unsuccessful 
            if not result:        
                self.selected = None        # Reset the selected piece
                self.select(row, column)    # Call the select function again
        
        piece = self.grid[row][column]
        # If another piece with the same color is selected
        if piece != '-' and piece != -1 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece)
            return True
        else:
            self.selected = None
            self.valid_moves = {}
            
        return False

    # Check if the move is valid or not
    def _make_move(self, row, column):
        if self.turn == RED:
            opponent = BLUE
        else:
            opponent = RED
            
        piece = self.grid[row][column]
        # Check if the piece is selected, the destination is a blank square and is in the list of valid moves for the piece
        if self.selected is not None and piece == -1 and (row, column) in self.valid_moves:
            self.move_piece(self.selected, row, column)
            skipped = self.valid_moves[(row, column)]   # List of skipped pieces (The pieces that got erased when we perform a jump move)
            if skipped is not None:
                self.remove_piece(skipped)
            
            if self.red_left <= 0 or self.blue_left <= 0:
                self.game_over = True
                self.result = "Player" if self.turn == RED else "Computer"
        
            # Check if the current player has any valid move to place on the board
            elif len(self.get_all_valid_moves(self.turn)) == 0:
                self.game_over = True
                self.result = "Computer" if self.turn == RED else "Player"
            
            # Check if the opponent has any valid move to place on the board
            elif len(self.get_all_valid_moves(opponent)) == 0:
                self.game_over = True
                self.result = "Player" if self.turn == RED else "Computer"
                
            self.next_player()
            
            
            
        else:
            return False

        return True

    # Move the piece to the wanted location on the board
    def move_piece(self, piece, row, column):
        self.grid[piece.row][piece.column], self.grid[row][column] = self.grid[row][column], self.grid[piece.row][piece.column]
        piece.row = row
        piece.column = column
        
        # If the piece moves to the furthest row, make that piece a king piece
        if row == 7 or row == 0:
            piece.make_king()
            if piece.color == BLUE:
                self.blue_kings += 1
            else:
                self.red_kings += 1
        
    def remove_piece(self, pieces):
        for piece in pieces:
            self.grid[piece.row][piece.column] = -1
            if piece != '-' and piece != -1:
                if piece.color == BLUE:
                    self.blue_left -= 1
                else:
                    self.red_left -= 1

    def next_player(self):
        self.valid_moves = {}
        self.selected = None
        if self.turn == RED:
            self.turn = BLUE
        else:
            self.turn = RED
    
    def get_all_pieces(self, color):
        pieces = []
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] != '-' and self.grid[i][j] != -1 and self.grid[i][j].color == color:
                    pieces.append(self.grid[i][j])
        return pieces
    
    def get_all_valid_moves(self, color):
        pieces = self.get_all_pieces(color)
        valid_moves = []
        for piece in pieces:
            moves = self.get_valid_moves(piece)
            if len(moves) > 0:
                for move in moves:
                    if move not in valid_moves:
                        valid_moves.append(move)
        return valid_moves
            
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self.traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self.traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
            
        if piece.color == BLUE or piece.king:
            moves.update(self.traverse_left(row +1, min(row+3, 8), 1, piece.color, left))
            moves.update(self.traverse_right(row +1, min(row+3, 8), 1, piece.color, right))
        
        return moves
    
    def traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.grid[r][left]
            if current != '-':
                if current == -1:
                    if skipped and not last:
                        break
                    elif skipped:
                        moves[(r, left)] = last + skipped
                    else:
                        moves[(r, left)] = last
                
                    if last:
                        if step == -1:
                            row = max(r-3, -1)
                        else:
                            row = min(r+3, 8)
                        moves.update(self.traverse_left(r+step, row, step, color, left-1, skipped=last))
                        moves.update(self.traverse_right(r+step, row, step, color, left+1, skipped=last))
                    break
                elif current.color == color:
                    break
                else:
                    last = [current]

                left -= 1
        
        return moves

    def traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right > 7:
                break
            
            current = self.grid[r][right]
            if current != '-':
                if current == -1:
                    if skipped and not last:
                        break
                    elif skipped:
                        moves[(r, right)] = last + skipped
                    else:
                        moves[(r, right)] = last
                
                    if last:
                        if step == -1:
                            row = max(r-3, -1)
                        else:
                            row = min(r+3, 8)
                        moves.update(self.traverse_left(r+step, row, step, color, right-1, skipped=last))
                        moves.update(self.traverse_right(r+step, row, step, color, right+1, skipped=last))
                    break
                elif current.color == color:
                    break
                else:
                    last = [current]

                right += 1
        
        return moves