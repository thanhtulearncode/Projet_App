from piece import *
from Action import *
from AI import GameAI
from ia import MinMaxAI, RandomAI, AIFactory, EasyAI, MediumAI, HardAI

class GameEngine:
    def __init__(self, color_pair='black-white', ai_difficulty='medium'):
        self.color_pair = color_pair
        self.board = self.create_initial_board()
        self.current_player = 'white'  
        self.game_over = False
        
        # Initialize AI with the new difficulty system
        self.ai_difficulty = ai_difficulty
        self.ai = AIFactory.create_ai(ai_difficulty, 'black')
        
        print(f"[GameEngine] Initialized with {ai_difficulty} AI for black player")
        
    def set_ai_difficulty(self, difficulty):
        """
        Change the AI difficulty level
        
        Args:
            difficulty (str): 'easy', 'medium', or 'hard'
        """
        self.ai_difficulty = difficulty
        self.ai = AIFactory.create_ai(difficulty, 'black')
        print(f"[GameEngine] AI difficulty changed to {difficulty}")
        
    def get_ai_difficulty(self):
        """Get the current AI difficulty level"""
        return self.ai_difficulty
        
    def create_initial_board(self):
        board = [[[] for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                self.add_square(board, row, col)

        if self.color_pair == 'red-green':
            color1, color2 = 'red', 'green'
        elif self.color_pair == 'orange-blue':
            color1, color2 = 'orange', 'blue'
        else:
            color1, color2 = 'white', 'black'

        for col in range(8):
            row = (col + 1) % 2
            if (col < 4) == (col % 2 == 0):
                c1, c2 = color2, color1
            else:
                c1, c2 = color1, color2
            self.add_pawn(board, row, col, c1)
            self.add_pawn(board, 7 - row, col, c2)
        return board

    def clone(self):
        new_engine = GameEngine(self.color_pair, self.ai_difficulty)
        new_engine.board = [[stack.copy() for stack in row] for row in self.board]
        new_engine.current_player = self.current_player
        new_engine.game_over = self.game_over

        return new_engine

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
                valid_moves = self.get_pawn_moves(piece, x, y, long_range=None)
            print(f"[LOG] Coups valides pour {piece.name} ({piece.color}) en ({x},{y}) : {valid_moves}")
        else:
            print(f"[LOG] Case ({x},{y}) vide.")
        return valid_moves

    def get_square_moves(self, piece, x, y):
        directions = []
        for i in range(x + 1, 8):
            if self.board[i][y]:
                if self.board[i][y][-1].name == "Pawn":
                    break
                elif len(self.board[i][y]) + len(self.board[x][y]) > 5:
                    break
                else:
                    directions.append((i, y))
                    break
        for i in range(x - 1, -1, -1):
            if self.board[i][y]:
                if self.board[i][y][-1].name == "Pawn":
                    break
                elif len(self.board[i][y]) + len(self.board[x][y]) > 5:
                    break
                else:
                    directions.append((i, y))
                    break
        for j in range(y + 1, 8):
            if self.board[x][j]:
                if self.board[x][j][-1].name == "Pawn":
                    break
                elif len(self.board[x][j]) + len(self.board[x][y]) > 5:
                    break
                else:
                    directions.append((x, j))
                    break
        for j in range(y - 1, -1, -1):
            if self.board[x][j]:
                if self.board[x][j][-1].name == "Pawn":
                    break
                elif len(self.board[x][j]) + len(self.board[x][y]) > 5:
                    break
                else:
                    directions.append((x, j))
                    break
        return directions

    def get_pawn_moves(self, piece, x, y, long_range=None):
        # Le nombre de cases max = nombre de pièces carrées sous le pion
        if long_range is None:
            long_range = sum(1 for p in self.board[x][y] if getattr(p, 'name', None) == 'Square')
            print(f"[LOG] Long range for Pawn at ({x},{y}): {long_range}")
        directions = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:  # haut, bas, gauche, droite
            nx, ny = x, y
            steps = 0
            print(long_range)
            while steps < long_range:
                nx += dx
                ny += dy
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # hors de la grille
                # On saute les cases vides
                if not self.board[nx][ny]:
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
                steps += 1
                print(steps)
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
        """Retourne les cases cibles valides pour empiler depuis (src_x, src_y) selon la logique de get_square_moves"""
        if not self.board[src_x][src_y]:
            print(f"[LOG] Pas d'EPC en ({src_x},{src_y})")
            return []
        if any(getattr(p, 'name', None) == 'Pawn' for p in self.board[src_x][src_y]):
            print(f"[LOG] Case avec pion en ({src_x},{src_y}), impossible de déplacer l'EPC")
            return []
        if not any(getattr(p, 'name', None) == 'Square' for p in self.board[src_x][src_y]):
            print(f"[LOG] Pas de pièce carrée en ({src_x},{src_y})")
            return []
        moves = []
        # Utilise la même logique que get_square_moves
        for i in range(src_x + 1, 8):
            if self.board[i][src_y]:
                if any(getattr(p, 'name', None) == 'Square' for p in self.board[i][src_y]) and not any(getattr(p, 'name', None) == 'Pawn' for p in self.board[i][src_y]):
                    pile_cible = [p for p in self.board[i][src_y] if getattr(p, 'name', None) == 'Square']
                    pile_source = [p for p in self.board[src_x][src_y] if getattr(p, 'name', None) == 'Square']
                    if len(pile_cible) + len(pile_source) <= 5:
                        moves.append((i, src_y))
                        print(f"[LOG] Mouvement valide: ({src_x},{src_y}) -> ({i},{src_y})")
                break
        for i in range(src_x - 1, -1, -1):
            if self.board[i][src_y]:
                if any(getattr(p, 'name', None) == 'Square' for p in self.board[i][src_y]) and not any(getattr(p, 'name', None) == 'Pawn' for p in self.board[i][src_y]):
                    pile_cible = [p for p in self.board[i][src_y] if getattr(p, 'name', None) == 'Square']
                    pile_source = [p for p in self.board[src_x][src_y] if getattr(p, 'name', None) == 'Square']
                    if len(pile_cible) + len(pile_source) <= 5:
                        moves.append((i, src_y))
                        print(f"[LOG] Mouvement valide: ({src_x},{src_y}) -> ({i},{src_y})")
                break
        for j in range(src_y + 1, 8):
            if self.board[src_x][j]:
                if any(getattr(p, 'name', None) == 'Square' for p in self.board[src_x][j]) and not any(getattr(p, 'name', None) == 'Pawn' for p in self.board[src_x][j]):
                    pile_cible = [p for p in self.board[src_x][j] if getattr(p, 'name', None) == 'Square']
                    pile_source = [p for p in self.board[src_x][src_y] if getattr(p, 'name', None) == 'Square']
                    if len(pile_cible) + len(pile_source) <= 5:
                        moves.append((src_x, j))
                        print(f"[LOG] Mouvement valide: ({src_x},{src_y}) -> ({src_x},{j})")
                break
        for j in range(src_y - 1, -1, -1):
            if self.board[src_x][j]:
                if any(getattr(p, 'name', None) == 'Square' for p in self.board[src_x][j]) and not any(getattr(p, 'name', None) == 'Pawn' for p in self.board[src_x][j]):
                    pile_cible = [p for p in self.board[src_x][j] if getattr(p, 'name', None) == 'Square']
                    pile_source = [p for p in self.board[src_x][src_y] if getattr(p, 'name', None) == 'Square']
                    if len(pile_cible) + len(pile_source) <= 5:
                        moves.append((src_x, j))
                        print(f"[LOG] Mouvement valide: ({src_x},{src_y}) -> ({src_x},{j})")
                break
        print(f"[LOG] Mouvements valides pour EPC en ({src_x},{src_y}): {moves}")
        return moves

    def stack_pieces(self, src_x, src_y, dst_x, dst_y):
        """Déplace toute la pile carrée de src vers dst si possible."""
        print(f"[LOG] Tentative d'empilement: ({src_x},{src_y}) -> ({dst_x},{dst_y})")
        
        # Vérifier que la source et la destination sont valides
        if not (0 <= src_x < 8 and 0 <= src_y < 8 and 0 <= dst_x < 8 and 0 <= dst_y < 8):
            print("[LOG] Coordonnées hors limites")
            return False
            
        # Vérifier si la source contient un EPC et pas de pion
        if not self.board[src_x][src_y]:
            print("[LOG] Case source vide")
            return False
            
        if any(getattr(p, 'name', None) == 'Pawn' for p in self.board[src_x][src_y]):
            print(self.board[src_x][src_y])
            print("[LOG] Case source contient un pion")
            return False
            
        if not any(getattr(p, 'name', None) == 'Square' for p in self.board[src_x][src_y]):
            print("[LOG] Pas de pièce carrée à déplacer")
            return False
        
        # Vérifier que la destination contient un EPC et pas de pion
        if not self.board[dst_x][dst_y]:
            print("[LOG] Case destination vide")
            return False
            
        if any(getattr(p, 'name', None) == 'Pawn' for p in self.board[dst_x][dst_y]):
            print("[LOG] Case destination contient un pion")
            return False
            
        if not any(getattr(p, 'name', None) == 'Square' for p in self.board[dst_x][dst_y]):
            print("[LOG] Pas de pièce carrée à la destination")
            return False
        
        # Vérifier que la destination fait partie des coups valides
        valid_stack_moves = self.get_valid_stack_moves(src_x, src_y)
        if (dst_x, dst_y) not in valid_stack_moves:
            print("[LOG] La destination n'est pas un coup valide d'empilement")
            return False
        
        # Vérifier que l'empilement ne dépasse pas 5
        pile_source = [p for p in self.board[src_x][src_y] if getattr(p, 'name', None) == 'Square']
        pile_cible = [p for p in self.board[dst_x][dst_y] if getattr(p, 'name', None) == 'Square']
        if len(pile_source) + len(pile_cible) > 5:
            print("[LOG] L'empilement dépasserait 5 pièces")
            return False
        
        # Déplacer les pièces carrées
        for p in pile_source:
            self.board[dst_x][dst_y].append(p)
            p.position = (dst_x, dst_y)
        
        # Retirer les pièces carrées de la source
        self.board[src_x][src_y] = [p for p in self.board[src_x][src_y] if getattr(p, 'name', None) != 'Square']
        
        print(f"[LOG] Empilement réussi: {len(pile_source)} pièces de ({src_x},{src_y}) à ({dst_x},{dst_y})")
        return True

    def move_pion(self, start_x, start_y, end_x, end_y):
        """Déplace un pion rond sans capture spéciale."""
        if not self.board[start_x][start_y]:
            return False, None
        piece = self.board[start_x][start_y][-1]
        if getattr(piece, 'name', None) != 'Pawn':
            return False, None
        valid_moves = self.get_pawn_moves(piece, start_x, start_y)
        if (end_x, end_y) not in valid_moves:
            return False, None
        # Vérifie qu'il n'y a pas de pion adverse à la destination
        if any(getattr(p, 'name', None) == 'Pawn' and p.color != piece.color for p in self.board[end_x][end_y]):
            return False, None
        # Déplace le pion
        self.board[start_x][start_y].remove(piece)
        piece.position = (end_x, end_y)
        self.board[end_x][end_y].append(piece)
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True, None

    def attack_pion(self, start_x, start_y, end_x, end_y, captured_dest=None):
        print("attack_pion backend:", start_x, start_y, end_x, end_y, captured_dest)
        if not self.board[start_x][start_y]:
            print("[DEBUG] Pas de pion à la position de départ")
            return False, None, []
        piece = self.board[start_x][start_y][-1]
        if getattr(piece, 'name', None) != 'Pawn':
            print("[DEBUG] La pièce de départ n'est pas un pion")
            return False, None, []
        valid_moves = self.get_pawn_moves(piece, start_x, start_y)
        if (end_x, end_y) not in valid_moves:
            print(f"[DEBUG] ({end_x},{end_y}) n'est pas un coup valide pour ce pion : {valid_moves}")
            return False, None, []
        # Vérifie qu'il y a bien un pion adverse à la destination
        captured = None
        for p in self.board[end_x][end_y]:
            if getattr(p, 'name', None) == 'Pawn' and p.color != piece.color:
                captured = p
                if captured_dest is not None:
                    dest_x, dest_y = captured_dest
                    if not (0 <= dest_x < 8 and 0 <= dest_y < 8):
                        print("[DEBUG] Destination hors plateau !")
                        return False, None, []
                    if not self.board[dest_x][dest_y]:
                        print("[DEBUG] Destination vide !")
                        return False, None, []
                    if any(getattr(pp, 'name', None) == 'Pawn' for pp in self.board[dest_x][dest_y]):
                        print("[DEBUG] Destination déjà occupée par un pion !")
                        return False, None, []
                    self.board[end_x][end_y].remove(captured)
                    self.board[dest_x][dest_y].append(captured)
                else:
                    captured_valid_dest = []
                    for i in range(8):
                        for j in range(8):
                            if (i, j) == (end_x, end_y):
                                continue
                            if self.board[i][j] and not any(getattr(pp, 'name', None) == 'Pawn' for pp in self.board[i][j]):
                                captured_valid_dest.append((i, j))
                    print("[DEBUG] Cases valides pour le pion capturé:", captured_valid_dest)
                    return True, captured, captured_valid_dest
                break
        if not captured:
            print("[DEBUG] Pas de pion adverse à la destination !")
            return False, None, []
        # Déplace le pion attaquant
        self.board[start_x][start_y].remove(piece)
        piece.position = (end_x, end_y)
        self.board[end_x][end_y].append(piece)
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True, captured, []

    def can_stack(self, color):
        """Vérifie si le joueur peut empiler une pile carrée (CPE)."""
        for x in range(8):
            for y in range(8):
                if not self.board[x][y]:
                    continue
                # Check if the top piece is a square (CPE) and can be moved
                if hasattr(self.board[x][y][-1], 'name') and self.board[x][y][-1].name == 'Square':
                    valid_moves = self.get_valid_stack_moves(x, y)
                    if valid_moves:
                        print(f"Valid stack moves for CPE at ({x},{y}): {valid_moves}")
                        return True
        print(f"No valid CPE moves for {color}")
        return False

    def check_game_over(self):
        """Détecte la fin de partie (aucun joueur ne peut déplacer un CPE)."""
        
        print(f"[DEBUG] Checking if {self.current_player} can move any squares...")
        
        for x in range(8):
            for y in range(8):
                if self.board[x][y]:
                    if self.board[x][y][-1].name == 'Square':
                        valid_moves = self.get_square_moves(self.board[x][y][-1], x, y)
                        print(f"[AAAA] Valid moves for square at ({x},{y}): {valid_moves}")
                        if valid_moves:
                            return False
        return True

    def get_winner(self):
        """Détermine le gagnant selon les règles:
        1. Player with most pieces on buildings (stacks)
        2. In case of tie: player with most pieces on 4-piece CPEs, then 3-piece, etc."""
        
        # Count pieces on buildings (stacks) for each player
        white_building_pieces = 0
        black_building_pieces = 0
        
        # Dictionary to count pieces by stack size
        white_by_size = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        black_by_size = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for x in range(8):
            for y in range(8):
                if self.board[x][y]:
                    # Count squares in this stack
                    square_count = sum(1 for p in self.board[x][y] if hasattr(p, 'name') and p.name == 'Square')
                    
                    if square_count > 0:  # This is a building/stack
                        # Count pawns on this building
                        for p in self.board[x][y]:
                            if hasattr(p, 'name') and p.name == 'Pawn':
                                if p.color == 'white':
                                    white_building_pieces += 1
                                    white_by_size[square_count] += 1
                                elif p.color == 'black':
                                    black_building_pieces += 1
                                    black_by_size[square_count] += 1
        
        print(f"White pieces on buildings: {white_building_pieces}")
        print(f"Black pieces on buildings: {black_building_pieces}")
        print(f"White by stack size: {white_by_size}")
        print(f"Black by stack size: {black_by_size}")
        
        # First criterion: most pieces on buildings
        if white_building_pieces > black_building_pieces:
            return 'white'
        elif black_building_pieces > white_building_pieces:
            return 'black'
        
        # Tie: check by stack size (4, 3, 2, 1)
        for size in range(4, 0, -1):
            if white_by_size[size] > black_by_size[size]:
                return 'white'
            elif black_by_size[size] > white_by_size[size]:
                return 'black'
        
        return 'draw'

    def get_valid_epc_moves(self, row, col):
        """Obtenir tous les mouvements valides pour un EPC à la position (row, col)"""
        valid_moves = []
        
        # Vérifier que la case contient au moins une pièce carrée
        has_square = False
        for piece in self.board[row][col]:
            if piece['type'] == 'Square' or piece['type'] == 'square':
                has_square = True
                break
        
        if not has_square:
            print(f"No square found at {row},{col}")
            return {"validMoves": []}
        
        # Vérifier qu'il n'y a pas de pion sur cette case
        has_pawn = False
        for piece in self.board[row][col]:
            if piece['type'] == 'Pawn' or piece['type'] == 'round':
                has_pawn = True
                break
        
        if has_pawn:
            print(f"Pawn found at {row},{col}, can't move this EPC")
            return {"validMoves": []}
        
        # Un EPC ne peut se déplacer que d'une case orthogonalement
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Vérifier si la nouvelle position est dans les limites du plateau
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Vérifier que la case cible contient au moins une pièce carrée
                target_has_square = False
                for piece in self.board[new_row][new_col]:
                    if piece['type'] == 'Square' or piece['type'] == 'square':
                        target_has_square = True
                        break
                
                if not target_has_square:
                    continue
                
                # Vérifier que la case cible n'a pas de pion
                target_has_pawn = False
                for piece in self.board[new_row][new_col]:
                    if piece['type'] == 'Pawn' or piece['type'] == 'round':
                        target_has_pawn = True
                        break
                
                if target_has_pawn:
                    continue
                
                # Vérifier que la pile résultante ne dépasse pas 5 pièces carrées
                source_square_count = sum(1 for piece in self.board[row][col] 
                                         if piece['type'] == 'Square' or piece['type'] == 'square')
                target_square_count = sum(1 for piece in self.board[new_row][new_col] 
                                         if piece['type'] == 'Square' or piece['type'] == 'square')
                
                if source_square_count + target_square_count <= 5:
                    valid_moves.append([new_row, new_col])
        
        print(f"Valid EPC moves from {row},{col}: {valid_moves}")
        return {"validMoves": valid_moves}

    def move_epc(self, start_row, start_col, end_row, end_col):
        """Déplacer un EPC d'une case à une autre adjacente"""
        print(f"Attempting to move EPC from {start_row},{start_col} to {end_row},{end_col}")
        
        # Vérifier si les coordonnées sont valides
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            print("Invalid coordinates")
            return False
        
        # Vérifier que les cases sont adjacentes (déplacement d'une seule case)
        if not ((abs(start_row - end_row) == 1 and start_col == end_col) or 
                (abs(start_col - end_col) == 1 and start_row == end_row)):
            print("Not adjacent cells")
            return False
        
        # Vérifier que la case de départ contient au moins une pièce carrée
        start_squares = []
        for i, piece in enumerate(self.board[start_row][start_col]):
            if piece['type'] == 'Square' or piece['type'] == 'square':
                start_squares.append((i, piece))
        
        if not start_squares:
            print("No squares at start position")
            return False
        
        # Vérifier qu'il n'y a pas de pion sur la case de départ
        has_pawn_start = any(piece['type'] == 'Pawn' or piece['type'] == 'round' 
                            for piece in self.board[start_row][start_col])
        if has_pawn_start:
            print("Pawn at start position")
            return False
        
        # Vérifier que la case cible contient au moins une pièce carrée
        has_square_end = any(piece['type'] == 'Square' or piece['type'] == 'square' 
                            for piece in self.board[end_row][end_col])
        if not has_square_end:
            print("No squares at end position")
            return False
        
        # Vérifier que la case cible n'a pas de pion
        has_pawn_end = any(piece['type'] == 'Pawn' or piece['type'] == 'round' 
                          for piece in self.board[end_row][end_col])
        if has_pawn_end:
            print("Pawn at end position")
            return False
        
        # Compter le nombre de pièces carrées dans la pile source et cible
        source_square_count = len(start_squares)
        target_square_count = sum(1 for piece in self.board[end_row][end_col] 
                                 if piece['type'] == 'Square' or piece['type'] == 'square')
        
        # Vérifier que la pile résultante ne dépasse pas 5 pièces carrées
        if source_square_count + target_square_count > 5:
            print("Would exceed 5 squares limit")
            return False
        
        # Transférer toutes les pièces carrées de la source vers la cible
        # Nous devons retirer les pièces de la fin vers le début pour éviter de perturber les indices
        for i, piece in sorted(start_squares, reverse=True):
            self.board[start_row][start_col].pop(i)
            self.board[end_row][end_col].append(piece[1])
        
        print(f"Successfully moved {source_square_count} squares from {start_row},{start_col} to {end_row},{end_col}")
        return True