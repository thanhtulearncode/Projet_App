class Action:
    def __init__(self, board):
        self.board = board

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