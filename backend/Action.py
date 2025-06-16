class Action:
    def __init__(self, type_action, start_pos, end_pos):
        """
        Initialise une action
        :param type_action: 'move_pion' ou 'stack_pieces'
        :param start_pos: (x, y) position de départ
        :param end_pos: (x, y) position d'arrivée
        """
        self.type_action = type_action
        self.start_pos = start_pos
        self.end_pos = end_pos
    
    def __str__(self):
        return f"{self.type_action} de {self.start_pos} vers {self.end_pos}"
    
    def execute(self, game_engine):
        """
        Exécute l'action sur le game_engine
        :param game_engine: Instance de GameEngine
        :return: True si l'action a réussi, False sinon
        """
        if self.type_action == 'move_pion':
            return game_engine.move_pion(
                self.start_pos[0], self.start_pos[1],
                self.end_pos[0], self.end_pos[1]
            )[0]  # Retourne le premier élément du tuple (success)
        else:  # stack_pieces
            return game_engine.stack_pieces(
                self.start_pos[0], self.start_pos[1],
                self.end_pos[0], self.end_pos[1]
            )

    def get_valid_moves(self, x, y):
        valid_moves = []
        piece = self.board[x][y].pop() if self.board[x][y] else None
        if piece:
            if piece.name == "Square":
                valid_moves = self.get_square_moves(piece, x, y)
            elif piece.name == "Pawn":
                valid_moves = self.get_pawn_moves(piece, x, y)

        self.board[x][y].append(piece)  # Restore the piece after checking
        return valid_moves
    
    
    def get_square_moves(self, x, y):
        directions = []
        for i in range(x + 1, 8):
            if self.board[i][y]:
                directions.append((i, y))
                break
        for i in range(x - 1, -1, -1):
            if self.board[i][y]:
                directions.append((i, y))
                break
        for j in range(y + 1, 8):
            if self.board[x][j]:
                directions.append((x, j))
                break
        for j in range(y - 1, -1, -1):
            if self.board[x][j]:
                directions.append((x, j))
                break

        return directions
    
    def get_pawn_moves(self, x, y, long_range):
        directions = []
        for i in range(x + 1, 8):
            if self.board[i][y]:
                for k in range(long_range):
                    if i + k < 8 and self.board[i + k][y]:
                        directions.append((i + k, y))
                    
            break

        for i in range(x - 1, -1, -1):
            if self.board[i][y]:
                for k in range(long_range):
                    if i - k >= 0 and self.board[i - k][y]:
                        directions.append((i - k, y))
                    
            break

        for j in range(y + 1, 8):
            if self.board[x][j]:
                for k in range(long_range):
                    if j + k < 8 and self.board[x][j + k]:
                        directions.append((x, j + k))
                    
            break

        for j in range(y - 1, -1, -1):
            if self.board[x][j]:
                for k in range(long_range):
                    if j - k >= 0 and self.board[x][j - k]:
                        directions.append((x, j - k))
                    
            break
        
        return directions