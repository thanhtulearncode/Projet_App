from Piece import *
from Action import *

class GameEngine:
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_player = 'white'  
        self.game_over = False

    def create_initial_board(self):
        board = [[[] for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                self.add_square(board, row, col)

        for col in range(8):
            if col % 2 == 0:
                self.add_pawn(board, 0, col, 'black')
                self.add_pawn(board, 6, col, 'black')
            else:
                self.add_pawn(board, 1, col, 'white')
                self.add_pawn(board, 7, col, 'white')
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
        board = [[[] for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                for piece in self.board[row][col]:
                    if hasattr(piece, 'name') and piece.name == "Square":
                        board[row][col].append({
                            "type": "Square",
                            "color": piece.color,
                            "position": piece.position
                        })
                    elif hasattr(piece, 'name') and piece.name == "Pawn":
                        board[row][col].append({
                            "type": "Pawn",
                            "color": piece.color,
                            "position": piece.position
                        })
        return board

    def get_valid_moves(self, x, y):
        valid_moves = []
        if self.board[x][y]:
            piece = self.board[x][y][-1]  # On lit sans retirer
            print(f"[LOG] Case ({x},{y}) contient : {piece.name} ({piece.color})")
            if piece.name == "Square":
                valid_moves = self.get_square_moves(piece, x, y)
            elif piece.name == "Pawn":
                valid_moves = self.get_pawn_moves(piece, x, y, long_range=1)
            print(f"[LOG] Coups valides pour {piece.name} ({piece.color}) en ({x},{y}) : {valid_moves}")
        else:
            print(f"[LOG] Case ({x},{y}) vide.")
        return valid_moves

    def get_square_moves(self, piece, x, y):
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

    def get_pawn_moves(self, piece, x, y, long_range=None):
        # Le nombre de cases max = nombre de pièces carrées sous le pion
        if long_range is None:
            long_range = sum(1 for p in self.board[x][y] if getattr(p, 'name', None) == 'Square')
        directions = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:  # haut, bas, gauche, droite
            nx, ny = x, y
            steps = 0
            while steps < long_range:
                nx += dx
                ny += dy
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # hors de la grille
                # On saute les cases vides
                if not self.board[nx][ny]:
                    steps += 1
                    continue
                # Si la case contient un pion allié, on ne peut pas s'arrêter
                if any(getattr(p, 'name', None) == 'Pawn' and p.color == piece.color for p in self.board[nx][ny]):
                    break
                # Si la case contient un pion adverse
                if any(getattr(p, 'name', None) == 'Pawn' and p.color != piece.color for p in self.board[nx][ny]):
                    # On ne peut s'arrêter ici que si on a fait exactement long_range pas
                    if steps + 1 == long_range:
                        directions.append((nx, ny))
                    break
                # Sinon, on peut s'arrêter ici
                directions.append((nx, ny))
                break
        return directions

    def move_piece(self, start_row, start_col, end_row, end_col):
        # Vérifier qu'il y a une pièce à la position de départ
        if not self.board[start_row][start_col]:
            return False, None
        piece = self.board[start_row][start_col][-1]
        valid_moves = self.get_valid_moves(start_row, start_col)
        if (end_row, end_col) not in valid_moves:
            return False, None
        # Gérer la capture éventuelle
        captured = None
        if self.board[end_row][end_col]:
            captured = self.board[end_row][end_col].pop()
        # Déplacer la pièce
        self.board[start_row][start_col].pop()
        piece.position = (end_row, end_col)
        self.board[end_row][end_col].append(piece)
        # Changer de joueur
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True, captured

    def get_valid_stack_moves(self, src_x, src_y):
        """Retourne les cases cibles valides pour empiler depuis (src_x, src_y)"""
        if not self.board[src_x][src_y]:
            return []
        if any(getattr(p, 'name', None) == 'Pawn' for p in self.board[src_x][src_y]):
            return []  # pas de pion sur la pile
        if not any(getattr(p, 'name', None) == 'Square' for p in self.board[src_x][src_y]):
            return []  # pas de pile carrée
        moves = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = src_x, src_y
            while True:
                nx += dx
                ny += dy
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                if not self.board[nx][ny]:
                    continue  # on saute les cases vides
                # On ne peut pas empiler si la pile cible dépasse 5
                pile_cible = [p for p in self.board[nx][ny] if getattr(p, 'name', None) == 'Square']
                pile_source = [p for p in self.board[src_x][src_y] if getattr(p, 'name', None) == 'Square']
                if len(pile_cible) + len(pile_source) <= 5:
                    moves.append((nx, ny))
                break
        return moves

    def stack_pieces(self, src_x, src_y, dst_x, dst_y):
        """Déplace toute la pile carrée de src vers dst si possible."""
        if (dst_x, dst_y) not in self.get_valid_stack_moves(src_x, src_y):
            return False
        pile_source = [p for p in self.board[src_x][src_y] if getattr(p, 'name', None) == 'Square']
        # On retire la pile source
        self.board[src_x][src_y] = [p for p in self.board[src_x][src_y] if getattr(p, 'name', None) != 'Square']
        # On ajoute à la pile cible
        self.board[dst_x][dst_y].extend(pile_source)
        return True

    def move_pion(self, start_x, start_y, end_x, end_y):
        """Déplace un pion rond selon les règles, gère la capture spéciale."""
        if not self.board[start_x][start_y]:
            return False, None
        piece = self.board[start_x][start_y][-1]
        if getattr(piece, 'name', None) != 'Pawn':
            return False, None
        valid_moves = self.get_pawn_moves(piece, start_x, start_y)
        if (end_x, end_y) not in valid_moves:
            return False, None
        # Capture spéciale
        captured = None
        for p in self.board[end_x][end_y]:
            if getattr(p, 'name', None) == 'Pawn' and p.color != piece.color:
                captured = p
                # Cherche une case libre pour déplacer le pion capturé
                for i in range(8):
                    for j in range(8):
                        if i == end_x and j == end_y:
                            continue
                        if self.board[i][j] and not any(getattr(pp, 'name', None) == 'Pawn' for pp in self.board[i][j]):
                            self.board[i][j].append(captured)
                            self.board[end_x][end_y].remove(captured)
                            break
                    else:
                        continue
                    break
                break
        # Déplace le pion
        self.board[start_x][start_y].remove(piece)
        piece.position = (end_x, end_y)
        self.board[end_x][end_y].append(piece)
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True, captured

    def can_stack(self, color):
        """Vérifie si le joueur peut empiler une pile carrée."""
        for x in range(8):
            for y in range(8):
                if not self.board[x][y]:
                    continue
                if any(getattr(p, 'name', None) == 'Pawn' and p.color == color for p in self.board[x][y]):
                    continue
                if any(getattr(p, 'name', None) == 'Square' for p in self.board[x][y]):
                    if self.get_valid_stack_moves(x, y):
                        return True
        return False

    def check_game_over(self):
        """Détecte la fin de partie (aucun joueur ne peut empiler)."""
        if not self.can_stack('white') and not self.can_stack('black'):
            self.game_over = True
            return True
        return False

    def get_winner(self):
        """Détermine le gagnant selon les règles de piles (5, puis 4, etc.)."""
        for h in range(5, 0, -1):
            white_count = 0
            black_count = 0
            for x in range(8):
                for y in range(8):
                    pile = [p for p in self.board[x][y] if getattr(p, 'name', None) == 'Square']
                    if len(pile) == h:
                        for p in self.board[x][y]:
                            if getattr(p, 'name', None) == 'Pawn':
                                if p.color == 'white':
                                    white_count += 1
                                elif p.color == 'black':
                                    black_count += 1
            if white_count > black_count:
                return 'white'
            elif black_count > white_count:
                return 'black'
        return 'draw'