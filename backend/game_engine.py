class GameEngine:
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_player = 'white'  
        self.game_over = False

    def create_initial_board(self):
        board = [[[] for _ in range(8)] for _ in range(8)]
        
        for row in range(8):
            for col in range(8):
                board[row][col].append({'type': 'square', 'color': None, 'height': 1})
        
        # Ligne 1 (index 0)
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

    def get_state(self):
        """Format pour transmission au frontend"""
        return self.board