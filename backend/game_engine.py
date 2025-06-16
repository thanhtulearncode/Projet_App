from Piece import *
from Action import *

class GameEngine:
    def __init__(self, color_pair='black-white'):
        self.color_pair = color_pair
        self.board = self.create_initial_board()
        self.current_player = self.get_player1_color()  
        self.game_over = False

    def get_player1_color(self):
        # Renvoie la couleur du joueur 1 selon la paire de couleurs choisie
        if self.color_pair == 'red-green':
            return 'red'
        elif self.color_pair == 'orange-blue':
            return 'orange'
        else:  # Par défaut black-white
            return 'white'
    
    def get_player2_color(self):
        # Renvoie la couleur du joueur 2 selon la paire de couleurs choisie
        if self.color_pair == 'red-green':
            return 'green'
        elif self.color_pair == 'orange-blue':
            return 'blue'
        else:  # Par défaut black-white
            return 'black'

    def create_initial_board(self):
        board = [[[] for _ in range(8)] for _ in range(8)]
        
        for row in range(8):
            for col in range(8):
                self.add_square(board, row, col)

        for col in range(8):
            if col % 2 == 0:
                board[0][col].append({'type': 'round', 'color': 'black', 'height': 1})
        
        # Ligne 2 (index 1)
        for col in range(8):
            if col % 2 == 1:
                board[1][col].append({'type': 'round', 'color': 'white', 'height': 1})
        
        # Ligne 7 (index 6)
        for col in range(8):
            if col % 2 == 0:
                board[6][col].append({'type': 'round', 'color': 'black', 'height': 1})

        # Ligne 8 (index 7)
        for col in range(8):
            if col % 2 == 1:
                board[7][col].append({'type': 'round', 'color': 'white', 'height': 1})
        
        return board

    def add_square(self, board, row, col):
        color = 'null'
        square = Square(color, (row, col))
        board[row][col].append(square)

    def add_pawn(self, board, row, col, color):
        pawn = Pawn(color, (row, col))
        board[row][col].append(pawn)

    def get_state(self):
        """Format pour transmission au frontend"""
        return self.board