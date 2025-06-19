import copy
import random

import copy
import random
import numpy as np

class MinMaxAI:
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth
        self.transposition_table = {}
        
    def zobrist_hash(self, game_engine):
        """Crée un hash unique pour l'état du jeu"""
        board_hash = 0
        for row in range(8):
            for col in range(8):
                stack = game_engine.board[row][col]
                if stack:
                    top_piece = stack[-1]
                    piece_type = getattr(top_piece, 'name', type(top_piece).__name__)
                    piece_color = getattr(top_piece, 'color', 'None')
                    piece_hash = hash(f"{row},{col},{piece_type},{piece_color},{len(stack)}")
                    board_hash ^= piece_hash
        return board_hash

    def get_max_height(self, game_engine):
        """Trouve la hauteur maximale des piles sur le plateau"""
        max_height = 0
        for row in range(8):
            for col in range(8):
                stack = game_engine.board[row][col]
                if stack and len(stack) > max_height:
                    max_height = len(stack)
        return max_height

    def get_position_value(self, row, col):
        """Retourne la valeur positionnelle d'une case"""
        # Centre plus important que les bords
        center_value = [
            [1, 1, 2, 2, 2, 2, 1, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [2, 3, 4, 4, 4, 4, 3, 2],
            [2, 3, 4, 5, 5, 4, 3, 2],
            [2, 3, 4, 5, 5, 4, 3, 2],
            [2, 3, 4, 4, 4, 4, 3, 2],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 1, 2, 2, 2, 2, 1, 1]
        ]
        return center_value[row][col] * 3

    def evaluate(self, game_engine):
        """Fonction d'évaluation sophistiquée avec plusieurs facteurs"""
        score = 0
        max_height = self.get_max_height(game_engine)
        
        for row in range(8):
            for col in range(8):
                stack = game_engine.board[row][col]
                if not stack:
                    continue
                    
                height = len(stack)
                top_piece = stack[-1]
                
                # 1. Contrôle des piles de hauteur maximale
                if height == max_height and top_piece.name == 'Pawn':
                    if top_piece.color == self.color:
                        score += 50  # Bonus important
                    else:
                        score -= 50
                        
                # 2. Valeur positionnelle
                position_value = self.get_position_value(row, col)
                if top_piece.name == 'Pawn' and top_piece.color == self.color:
                    moves = game_engine.get_pawn_moves(top_piece, row, col)
                    # Bonus pour les mouvements vers le centre
                    center_bonus = sum(self.get_position_value(m[0], m[1]) for m in moves)
                    score += len(moves) * 2 + center_bonus * 0.5
                    
                # 3. Mobilité
                if top_piece.name == 'Pawn' and top_piece.color == self.color:
                    moves = game_engine.get_pawn_moves(top_piece, row, col)
                    score += len(moves) * 2
                    
                # 4. Menaces sur les pions adverses
                if top_piece.name == 'Pawn' and top_piece.color != self.color:
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        r, c = row + dr, col + dc
                        if 0 <= r < 8 and 0 <= c < 8:
                            adj_stack = game_engine.board[r][c]
                            if adj_stack and adj_stack[-1].name == 'Pawn' and adj_stack[-1].color == self.color:
                                score += 10  # Bonus pour la menace
                
                # 5. Stratégie spécifique: éviter les piles de hauteur 5 trop tôt
                if height == 5 and top_piece.name == 'Square':
                    if any(p.name == 'Pawn' and p.color == self.color for p in stack):
                        score -= 30  # Décourager de bloquer ses propres pions
                
                # 6. Pions isolés (fin de partie)
                if top_piece.name == 'Pawn' and top_piece.color == self.color:
                    if self.is_isolated(game_engine, row, col):
                        score -= 15

        return score

    def is_isolated(self, game_engine, row, col):
        """Vérifie si un pion est isolé (version optimisée)"""
        directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                stack = game_engine.board[r][c]
                if stack and stack[-1].name == 'Pawn' and stack[-1].color == self.color:
                    return False
        return True

    def get_all_moves(self, game_engine, color):
        """Retourne les coups ordonnés par potentiel"""
        moves = []
        for row in range(8):
            for col in range(8):
                if game_engine.board[row][col]:
                    top_piece = game_engine.board[row][col][-1]
                    # Priorité aux captures
                    if top_piece.name == 'Pawn' and top_piece.color == color:
                        print(f"[DEBUG] Considering pawn at ({row},{col}) for moves")
                        pawn_moves = game_engine.get_pawn_moves(top_piece, row, col)
                        print(f"[DEBUG] Valid pawn moves from ({row},{col}): {pawn_moves}")
                        for move in pawn_moves:
                            # Vérifie si c'est une capture
                            target_stack = game_engine.board[move[0]][move[1]]
                            is_capture = target_stack and target_stack[-1].name == 'Pawn' and target_stack[-1].color != color
                            moves.append(("move_pion", (row, col), (move[0], move[1]), is_capture))
                    # Priorité aux empilages qui créent des piles hautes
                    elif top_piece.name == 'Square':
                        valid_moves = game_engine.get_valid_stack_moves(row, col)
                        for end_pos in valid_moves:
                            new_height = len(game_engine.board[row][col]) + len(game_engine.board[end_pos[0]][end_pos[1]])
                            moves.append(("stack_pieces", (row, col), end_pos, new_height))
        # Trie les coups par importance (captures et empilages hauts d'abord)
        moves.sort(key=lambda x: (
            -1 if x[0] == "move_pion" and x[3] else  # Captures d'abord
            -x[3] if x[0] == "stack_pieces" else 0,  # Empilages hauts d'abord
            random.random()  # Random pour varier l'ordre des coups équivalents
        ), reverse=True)
        return [(m[0], m[1], m[2]) for m in moves]  # Retourne sans le score

    def is_valid_combo(self, pawn_move, stack_move):
        """Vérifie si une combinaison de coups est valide"""
        return (
            pawn_move[2][0] == stack_move[1][0] and
            pawn_move[2][1] == stack_move[1][1]
        )

    def get_all_move_pairs(self, game_engine, color):
        """Optimized: Retourne toutes les paires valides (move_pion, stack_pieces) pour un tour, en générant les stack moves après le move_pion, en minimisant les clones et scans."""
        pawn_moves = []
        # Collect all pawn moves efficiently
        for row in range(8):
            for col in range(8):
                if game_engine.board[row][col]:
                    top_piece = game_engine.board[row][col][-1]
                    if top_piece.name == 'Pawn' and top_piece.color == color:
                        for move in game_engine.get_pawn_moves(top_piece, row, col):
                            pawn_moves.append(('move_pion', (row, col), move))
        pairs = []
        for pawn in pawn_moves:
            temp_game = game_engine.clone()
            self.apply_move(temp_game, pawn)
            found_valid = False
            # Only check stack moves for cells that do not have a pawn on top and are not the pawn's new cell
            for row in range(8):
                for col in range(8):
                    if temp_game.board[row][col]:
                        top_piece = temp_game.board[row][col][-1]
                        if top_piece.name == 'Square' and (row, col) != pawn[2]:
                            for end_pos in temp_game.get_valid_stack_moves(row, col):
                                pairs.append([pawn, ('stack_pieces', (row, col), end_pos)])
                                found_valid = True
            if not found_valid:
                pairs.append([pawn])
        # Also allow stack-only moves if no pawn moves are possible
        if not pairs:
            for row in range(8):
                for col in range(8):
                    if game_engine.board[row][col]:
                        top_piece = game_engine.board[row][col][-1]
                        if top_piece.name == 'Square':
                            for end_pos in game_engine.get_valid_stack_moves(row, col):
                                pairs.append([('stack_pieces', (row, col), end_pos)])
        return pairs

    def get_best_move(self, game_engine):
        # Get all possible actions
        pawn_moves = [m for m in self.get_all_moves(game_engine, self.color) if m[0] == 'move_pion']
        stack_moves = [m for m in self.get_all_moves(game_engine, self.color) if m[0] == 'stack_pieces']

        best_score = float('-inf')
        best_pair = None

        # Try all pairs and score them
        for pawn in pawn_moves:
            for stack in stack_moves:
                if self.is_valid_combo(pawn, stack):
                    temp_game = game_engine.clone()
                    temp_game.move_piece(pawn[1][0], pawn[1][1], pawn[2][0], pawn[2][1])
                    if temp_game.get_valid_stack_moves(stack[1][0], stack[1][1]):
                        temp_game.stack_pieces(stack[1][0], stack[1][1], stack[2][0], stack[2][1])
                        score = self.evaluate(temp_game)
                        print(f"[AI DEBUG] Evaluating pair: {pawn}, {stack} -> score: {score}")
                        if score > best_score:
                            best_score = score
                            best_pair = (pawn, stack)

        # If no valid pair found, try all pairs and pick the first that is valid in sequence
        if not best_pair and pawn_moves and stack_moves:
            for pawn in pawn_moves:
                temp_game = game_engine.clone()
                temp_game.move_piece(pawn[1][0], pawn[1][1], pawn[2][0], pawn[2][1])
                for stack in stack_moves:
                    valid_stacks = temp_game.get_valid_stack_moves(stack[1][0], stack[1][1])
                    if stack[2] in valid_stacks:
                        best_pair = (pawn, stack)
                        break
                if best_pair:
                    break

        # If still not possible, raise or skip the turn
        if not best_pair:
            raise Exception("No valid move_pion and stack_pieces pair found!")

        return [best_pair[0], best_pair[1]]

    def minimax_search(self, game_engine, depth):
        """Effectue une recherche MinMax à une profondeur spécifique"""
        # Utilise la table de transposition pour accélérer la recherche
        game_hash = self.zobrist_hash(game_engine)
        if game_hash in self.transposition_table:
            entry = self.transposition_table[game_hash]
            if entry['depth'] >= depth:
                return entry['value'], entry['best_move']
        
        # Vérifie si c'est une fin de partie
        if self.is_endgame(game_engine):
            eval_score, best_move = self.endgame_strategy(game_engine)
        else:
            eval_score, best_move = self.minimax(
                game_engine.clone(), 
                depth, 
                True, 
                float('-inf'), 
                float('inf')
            )
        
        # Stocke le résultat dans la table de transposition
        self.transposition_table[game_hash] = {
            'depth': depth,
            'value': eval_score,
            'best_move': best_move
        }
        
        return eval_score, best_move

    def is_endgame(self, game_engine):
        """Détermine si c'est une fin de partie"""
        pawn_count = 0
        for row in range(8):
            for col in range(8):
                stack = game_engine.board[row][col]
                if stack and stack[-1].name == 'Pawn':
                    pawn_count += 1
        
        # Fin de jeu quand il y a peu de pions ou quand les piles sont presque toutes à hauteur max
        return pawn_count <= 4 or self.get_max_height(game_engine) >= 4

    def endgame_strategy(self, game_engine):
        best_combo = None
        best_score = float('-inf')
        max_height = self.get_max_height(game_engine)
        pawn_moves = [m for m in self.get_all_moves(game_engine, self.color) if m[0] == 'move_pion']
        stack_moves = [m for m in self.get_all_moves(game_engine, self.color) if m[0] == 'stack_pieces']
        print("[DEBUG] pawn_moves:", pawn_moves)
        print("[DEBUG] stack_moves:", stack_moves)
        for pawn in pawn_moves:
            for stack in stack_moves:
                if self.is_valid_combo(pawn, stack):
                    temp_game = game_engine.clone()
                    temp_game.move_piece(pawn[1][0], pawn[1][1], pawn[2][0], pawn[2][1])
                    if temp_game.get_valid_stack_moves(stack[1][0], stack[1][1]):
                        temp_game.stack_pieces(stack[1][0], stack[1][1], stack[2][0], stack[2][1])
                        score = self.endgame_evaluate(temp_game, max_height)
                        if score > best_score:
                            best_score = score
                            best_combo = (pawn, stack)
        if best_combo:
            return best_score, best_combo
        move_pion = next((m for m in pawn_moves), None)
        stack_piece = next((s for s in stack_moves), None)
        if move_pion and stack_piece:
            return 0, (move_pion, stack_piece)
        return 0, None  # Aucun coup possible

    def endgame_evaluate(self, game_engine, max_height):
        """Évaluation optimisée pour la fin de partie"""
        score = 0
        current_max_height = self.get_max_height(game_engine)
        
        for row in range(8):
            for col in range(8):
                stack = game_engine.board[row][col]
                if not stack:
                    continue
                    
                height = len(stack)
                top_piece = stack[-1]
                
                # Focus exclusif sur les piles maximales
                if height == current_max_height and top_piece.name == 'Pawn':
                    if top_piece.color == self.color:
                        score += 100
                    else:
                        score -= 100
                
                # Bonus supplémentaire si c'est la pile la plus haute
                if height == max_height and top_piece.name == 'Pawn' and top_piece.color == self.color:
                    score += 50
                
                # Pénalité pour les pions isolés
                if top_piece.name == 'Pawn' and top_piece.color == self.color and self.is_isolated(game_engine, row, col):
                    score -= 30
        
        return score

    def minimax(self, game, depth, maximizing_player, alpha, beta):
        """Algorithme MinMax avec élagage alpha-bêta et tables de transposition, utilisant des paires de coups"""
        # Utilise la table de transposition pour accélérer la recherche
        game_hash = self.zobrist_hash(game)
        if game_hash in self.transposition_table:
            entry = self.transposition_table[game_hash]
            if entry['depth'] >= depth:
                if entry['maximizing'] == maximizing_player:
                    return entry['value'], entry['best_move']
        # Condition d'arrêt : profondeur atteinte ou fin de partie
        if depth == 0 or game.check_game_over():
            eval_score = self.evaluate(game)
            print(f"[MINIMAX EVAL] depth={depth}, maximizing={maximizing_player}, score={eval_score}")
            return eval_score, None
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            valid_move_pairs = self.get_all_move_pairs(game, self.color)
            for move_pair in valid_move_pairs:
                new_game = game.clone()
                for move in move_pair:
                    self.apply_move(new_game, move)
                new_game.current_player = 'white' if game.current_player == 'black' else 'black'
                eval_score, _ = self.minimax(new_game, depth - 1, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move_pair
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Élagage beta
            self.transposition_table[game_hash] = {
                'depth': depth,
                'value': max_eval,
                'best_move': best_move,
                'maximizing': maximizing_player
            }
            return max_eval, best_move
        else:  # minimizing_player
            min_eval = float('inf')
            best_move = None
            valid_move_pairs = self.get_all_move_pairs(game, self.color)
            for move_pair in valid_move_pairs:
                new_game = game.clone()
                for move in move_pair:
                    self.apply_move(new_game, move)
                new_game.current_player = 'white' if game.current_player == 'black' else 'black'
                eval_score, _ = self.minimax(new_game, depth - 1, True, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move_pair
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Élagage alpha
            self.transposition_table[game_hash] = {
                'depth': depth,
                'value': min_eval,
                'best_move': best_move,
                'maximizing': maximizing_player
            }
            return min_eval, best_move

    def apply_move(self, game, move):
        """Applique un coup sur le jeu"""
        action, start, end = move
        if action == 'move_pion':
            # Gérer spécifiquement les captures
            target = game.board[end[0]][end[1]]
            if target and target[-1].name == 'Pawn' and target[-1].color != self.color:
                game.attack_pion(start[0], start[1], end[0], end[1])
            else:
                game.move_pion(start[0], start[1], end[0], end[1])
        elif action == 'stack_pieces':
            game.stack_pieces(start[0], start[1], end[0], end[1])

    def make_decision(self, game_engine):
        try:
            score, move = self.minimax_search(game_engine, self.depth)
            if isinstance(move, (list, tuple)):
                return list(move)
            return []
        except Exception as e:
            print("[MinMaxAI] Exception in minimax_search, falling back to RandomAI:", e)
            random_ai = RandomAI(self.color)
            move = random_ai.make_decision(game_engine)
            return move if move else []


class RandomAI:
    def __init__(self, color, depth=2):
        self.color = color  # 'white' or 'black'

    def make_decision(self, game_engine):
        max_iterations = 50  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:  # Keep trying until we find a valid move
            iteration += 1
            board = game_engine.board
            pion_moves = []
            stack_moves = []
            
            print(f"\n[DEBUG] Starting new move search (iteration {iteration})")
            print(f"[DEBUG] Current player: {self.color}")
            
            # Collect all valid moves
            for i in range(8):
                for j in range(8):
                    if board[i][j]:
                        piece = board[i][j][-1]
                        if hasattr(piece, 'name') and piece.name == 'Pawn' and piece.color == self.color:
                            print(f"[DEBUG] Found {self.color} pawn at ({i},{j})")
                            valid_moves = game_engine.get_pawn_moves(piece, i, j)
                            print(f"[DEBUG] Valid pawn moves from ({i},{j}): {valid_moves}")
                            if valid_moves:
                                for end_pos in valid_moves:
                                    pion_moves.append(('move_pion', (i, j), end_pos))
                        elif hasattr(piece, 'name') and piece.name == 'Pawn':
                            print(f"[DEBUG] Found opponent pawn at ({i},{j})")
                            continue
                        else:
                            print(f"[DEBUG] Checking stack moves at ({i},{j})")
                            valid_moves = game_engine.get_valid_stack_moves(i, j)
                            print(f"[DEBUG] Valid stack moves from ({i},{j}): {valid_moves}")
                            if valid_moves:
                                for end_pos in valid_moves:
                                    stack_moves.append(('stack_pieces', (i, j), end_pos))
            
            print(f"[DEBUG] Found {len(pion_moves)} pawn moves and {len(stack_moves)} stack moves")
            print("pion_moves:", pion_moves)
            print("stack_moves:", stack_moves)
            
            # If no moves at all are found, break out of the loop
            if not pion_moves and not stack_moves:
                print("[DEBUG] No valid moves found at all")
                break
            
            # If we have both types of moves, try to find a valid combination
            if pion_moves and stack_moves:
                # Try to find a valid pawn move first
                move = random.choice(pion_moves)
                print(f"[DEBUG] Selected pawn move: {move}")
                x, y = move[2]
                x1, y1 = move[1]
                long_range = len(game_engine.board[x1][y1]) - 1
                long_range2 = max(x-x1, y-y1)
                
                print(f"[DEBUG] Pawn move validation: long_range={long_range}, long_range2={long_range2}")
                print(f"[DEBUG] Target square ({x},{y}) contains: {game_engine.board[x][y]}")
                
                if game_engine.board[x][y] and hasattr(game_engine.board[x][y][-1], 'name') and game_engine.board[x][y][-1].color != self.color and long_range == long_range2:
                    print("[DEBUG] Pawn move is valid, checking stack moves")
                    # Create a temporary game state to check if stack move is valid after pawn move
                    temp_game = game_engine.clone()
                    # Use move_pion instead of move_piece for pawn moves
                    success, captured, captured_valid_dest = temp_game.attack_pion(
                        move[1][0], move[1][1], move[2][0], move[2][1], None
                    )
                    
                    if not success:
                        # Try regular move if attack fails
                        success, captured = temp_game.move_pion(move[1][0], move[1][1], move[2][0], move[2][1])
                        captured_valid_dest = None
                    
                    if not success:
                        print(f"[DEBUG] Failed to execute pawn move in temp game state")
                        continue
                    
                    # Get the captured pawn destination if it was an attack
                    captured_pawn_dest = None
                    if captured and captured_valid_dest:
                        # The captured pawn was placed at a random destination
                        # We need to find where it was actually placed
                        for i in range(8):
                            for j in range(8):
                                if temp_game.board[i][j]:
                                    for piece in temp_game.board[i][j]:
                                        if (hasattr(piece, 'name') and piece.name == 'Pawn' and 
                                            piece.color != self.color and 
                                            piece.position != (move[2][0], move[2][1])):
                                            # This is likely the captured pawn
                                            captured_pawn_dest = (i, j)
                                            break
                                    if captured_pawn_dest:
                                        break
                            if captured_pawn_dest:
                                break
                    
                    # Collect stack moves from the temporary game state
                    temp_stack_moves = []
                    for i in range(8):
                        for j in range(8):
                            if temp_game.board[i][j]:
                                if hasattr(temp_game.board[i][j][-1], 'name') and temp_game.board[i][j][-1].name == 'Square':
                                    valid_moves = temp_game.get_valid_stack_moves(i, j)
                                    if valid_moves:
                                        for end_pos in valid_moves:
                                            temp_stack_moves.append(('stack_pieces', (i, j), end_pos))
                    
                    print(f"[DEBUG] Stack moves in temp game state: {temp_stack_moves}")
                    print(f"[DEBUG] Captured pawn destination: {captured_pawn_dest}")
                    
                    # Try to find a valid stack move in the temporary game state
                    for stack in temp_stack_moves:
                        print(f"[DEBUG] Checking stack move: {stack}")
                        print(f"[DEBUG] Stack source ({stack[1][0]},{stack[1][1]}) contains: {temp_game.board[stack[1][0]][stack[1][1]]}")
                        
                        # Check if the stack source position doesn't contain a pawn
                        source_piece = temp_game.board[stack[1][0]][stack[1][1]][-1] if temp_game.board[stack[1][0]][stack[1][1]] else None
                        if hasattr(source_piece, 'name') and source_piece.name == 'Pawn':
                            print(f"[DEBUG] Stack source contains pawn, skipping")
                            continue
                            
                        # Check if the stack source conflicts with the captured pawn destination
                        if captured_pawn_dest and stack[1] == captured_pawn_dest:
                            print(f"[DEBUG] Stack source conflicts with captured pawn destination, skipping")
                            continue
                            
                        # Check if the stack move is valid in the temporary game state
                        valid_stack_moves = temp_game.get_valid_stack_moves(stack[1][0], stack[1][1])
                        print(f"[DEBUG] Valid stack moves after pawn move: {valid_stack_moves}")
                        if valid_stack_moves and stack[2] in valid_stack_moves:
                            x, y = stack[2]
                            piece = temp_game.board[x][y][-1] if temp_game.board[x][y] else None
                            print(f"[DEBUG] Stack target square ({x},{y}) contains: {piece}")
                            
                            # Check if the destination doesn't contain a pawn
                            if hasattr(piece, 'name') and piece.name == 'Pawn':
                                print(f"[DEBUG] Stack destination contains pawn, skipping")
                                continue
                                
                            # Check if the stack destination conflicts with the pawn move destination
                            if move[2] == stack[2]:
                                print(f"[DEBUG] Stack destination conflicts with pawn move destination, skipping")
                                continue
                                
                            # Check if the stack destination conflicts with the captured pawn destination
                            if captured_pawn_dest and stack[2] == captured_pawn_dest:
                                print(f"[DEBUG] Stack destination conflicts with captured pawn destination, skipping")
                                continue
                                
                            if move[2] != stack[2] and move[2] != stack[1] and not (hasattr(piece, 'name') and piece.name == 'Pawn'):
                                print("[DEBUG] Found valid move combination!")
                                return [move, stack]
            
            print("[DEBUG] No valid combination found, trying again")
        
        # If we've exhausted all iterations without finding a valid move
        print(f"[DEBUG] Exhausted {max_iterations} iterations without finding a valid move")

        # Fallback: try just a pawn move
        if pion_moves:
            move = random.choice(pion_moves)
            print("[DEBUG] Fallback: returning single pawn move")
            return [move]

        # Fallback: try just a stack move
        if stack_moves:
            move = random.choice(stack_moves)
            print("[DEBUG] Fallback: returning single stack move")
            return [move]

        return None
# AI Difficulty Levels
class EasyAI(RandomAI):
    """
    Level 1 AI - Easy difficulty
    Uses random moves with basic validation
    """
    def __init__(self, color):
        super().__init__(color)
        self.difficulty = "Easy"
        print(f"[AI] Initialized {self.difficulty} AI for {color}")

    def make_decision(self, game_engine):
        print(f"[{self.difficulty} AI] Making random move decision")
        return super().make_decision(game_engine)


class MediumAI(MinMaxAI):
    """
    Level 2 AI - Medium difficulty
    Uses MinMax algorithm with shallow depth (2) for basic strategy
    """
    def __init__(self, color):
        super().__init__(color, depth=1)
        self.difficulty = "Medium"
        print(f"[AI] Initialized {self.difficulty} AI for {color} (depth: {self.depth})")

    def make_decision(self, game_engine):
        print(f"[{self.difficulty} AI] Making strategic move decision (depth: {self.depth})")
        return super().make_decision(game_engine)


class HardAI(MinMaxAI):
    """
    Level 3 AI - Hard difficulty
    Uses MinMax algorithm with deep depth (4) for advanced strategy
    """
    def __init__(self, color):
        super().__init__(color, depth=6)
        self.difficulty = "Hard"
        print(f"[AI] Initialized {self.difficulty} AI for {color} (depth: {self.depth})")

    def make_decision(self, game_engine):
        print(f"[{self.difficulty} AI] Making advanced strategic move decision (depth: {self.depth})")
        return super().make_decision(game_engine)


# AI Factory for easy instantiation
class AIFactory:
    """
    Factory class to create AI instances based on difficulty level
    """
    @staticmethod
    def create_ai(difficulty, color):
        """
        Create an AI instance based on difficulty level
        
        Args:
            difficulty (str): "easy", "medium", or "hard"
            color (str): "white" or "black"
            
        Returns:
            AI instance of the specified difficulty
        """
        difficulty = difficulty.lower()
        
        if difficulty == "easy":
            return EasyAI(color)
        elif difficulty == "medium":
            return MediumAI(color)
        elif difficulty == "hard":
            return HardAI(color)
        else:
            raise ValueError(f"Unknown difficulty level: {difficulty}. Use 'easy', 'medium', or 'hard'")