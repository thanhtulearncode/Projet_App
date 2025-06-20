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
                # 1. Main win condition: pawns on high stacks
                if top_piece.name == 'Pawn':
                    if height == 5:
                        bonus = 100
                    elif height == 4:
                        bonus = 40
                    elif height == 3:
                        bonus = 20
                    elif height == 2:
                        bonus = 10
                    else:
                        bonus = 0
                    if top_piece.color == self.color:
                        score += bonus
                    elif top_piece.color == 'null':
                        score += bonus // 2
                    else:
                        score -= bonus
                # 2. Tactical/positional factors
                # Mutual protection (adjacent friendly pawns)
                if top_piece.name == 'Pawn' and top_piece.color == self.color:
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        r, c = row + dr, col + dc
                        if 0 <= r < 8 and 0 <= c < 8:
                            adj_stack = game_engine.board[r][c]
                            if adj_stack and adj_stack[-1].name == 'Pawn':
                                if adj_stack[-1].color == self.color:
                                    score += 5
                                else:
                                    # Offensive potential: can attack if in range
                                    long_range = sum(1 for p in stack if getattr(p, 'name', None) == 'Square')
                                    if max(abs(r-row), abs(c-col)) == long_range:
                                        score += 10
                # Mobility and open lanes
                if top_piece.name == 'Pawn' and top_piece.color == self.color:
                    moves = game_engine.get_pawn_moves(top_piece, row, col)
                    score += len(moves) * 2
                    if len(moves) >= 3:
                        score += 5
                # Threats to opponent pawns
                if top_piece.name == 'Pawn' and top_piece.color != self.color:
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        r, c = row + dr, col + dc
                        if 0 <= r < 8 and 0 <= c < 8:
                            adj_stack = game_engine.board[r][c]
                            if adj_stack and adj_stack[-1].name == 'Pawn' and adj_stack[-1].color == self.color:
                                score += 8
                # SPCs (Squares) mobility and blocking
                if top_piece.name == 'Square':
                    if not any(p.name == 'Pawn' for p in stack):
                        valid_spc_moves = game_engine.get_valid_stack_moves(row, col)
                        if valid_spc_moves:
                            score += 3
                        for end_pos in valid_spc_moves:
                            dest_stack = game_engine.board[end_pos[0]][end_pos[1]]
                            dest_height = len(dest_stack)
                            if dest_height + height == 5:
                                score += 8
                    else:
                        score -= 5  # Penalize blocked SPCs
                # Discourage early tall stacks blocking own pawns
                if height == 5 and top_piece.name == 'Square':
                    if any(p.name == 'Pawn' and p.color == self.color for p in stack):
                        score -= 20
                # Isolated pawns
                if top_piece.name == 'Pawn' and top_piece.color == self.color:
                    if self.is_isolated(game_engine, row, col):
                        score -= 10
                # Penalize illegal stacks
                if height > 5:
                    score -= 1000

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
        """Retourne les coups ordonnés par potentiel, en limitant à 3 de chaque type pour la performance et la diversité."""
        move_pion_moves = []
        stack_pieces_moves = []
        for row, col in getattr(game_engine, 'pawns', []):
            if game_engine.board[row][col]:
                top_piece = game_engine.board[row][col][-1]
                if top_piece.name == 'Pawn' and top_piece.color == color:
                    pawn_moves = game_engine.get_pawn_moves(top_piece, row, col)
                    for move in pawn_moves:
                        target_stack = game_engine.board[move[0]][move[1]]
                        is_capture = target_stack and target_stack[-1].name == 'Pawn' and target_stack[-1].color != color
                        move_pion_moves.append(("move_pion", (row, col), (move[0], move[1]), is_capture))
        for row, col in getattr(game_engine, 'stacks', []):
            if game_engine.board[row][col]:
                top_piece = game_engine.board[row][col][-1]
                if top_piece.name == 'Square':
                    valid_moves = game_engine.get_valid_stack_moves(row, col)
                    for end_pos in valid_moves:
                        new_height = len(game_engine.board[row][col]) + len(game_engine.board[end_pos[0]][end_pos[1]])
                        stack_pieces_moves.append(("stack_pieces", (row, col), end_pos, new_height))
        # Sort and limit each type
        move_pion_moves.sort(key=lambda x: (-1 if x[3] else 0, random.random()), reverse=True)
        stack_pieces_moves.sort(key=lambda x: (-x[3], random.random()), reverse=True)
        random.shuffle(move_pion_moves)
        random.shuffle(stack_pieces_moves)
        limited_moves = move_pion_moves[:3] + stack_pieces_moves[:3]  # adjust 3 as needed
        random.shuffle(limited_moves)
        return [(m[0], m[1], m[2]) for m in limited_moves]

    def is_valid_combo(self, pawn_move, stack_move):
        """Vérifie si une combinaison de coups est valide"""
        return (
            pawn_move[2] != stack_move[1] and
            pawn_move[2] != stack_move[2]
        )

    def get_all_move_pairs(self, game_engine, color):
        pawn_moves = []
        for row, col in game_engine.pawns:
            if game_engine.board[row][col]:
                top_piece = game_engine.board[row][col][-1]
                if top_piece.name == 'Pawn' and top_piece.color == color:
                    for move in game_engine.get_pawn_moves(top_piece, row, col):
                        pawn_moves.append(('move_pion', (row, col), move))
        random.shuffle(pawn_moves)
        print(f"[DEBUG] Found {(pawn_moves)} pawn moves for color {color}")
        pairs = []
        scored_pairs = []
        # Use apply/undo instead of clone for efficiency
        for pawn in pawn_moves:
            undo_pawn = game_engine.apply_move(pawn)
            found_valid = False
            pawn_end = pawn[2]
            for row, col in game_engine.stacks:
                print(f"[DEBUG] Evaluating stack moves for pawn {pawn} at {row}, {col}")
                if game_engine.board[row][col]:
                    top_piece = game_engine.board[row][col][-1]
                    if top_piece.name == 'Square' and (row, col) != pawn[2]:
                        for end_pos in game_engine.get_square_moves(top_piece,row, col):
                            print(f"[DEBUG] Evaluating stack move: {end_pos} for pawn move {pawn}")
                            if end_pos == pawn_end or (row, col) == pawn_end:
                                print(f"[DEBUG] Skipping invalid stack move: {end_pos} for pawn move {pawn}")
                                continue
                            stack_move = ('stack_pieces', (row, col), end_pos)
                            undo_stack = game_engine.apply_move(stack_move)
                            valid = True
                            if undo_pawn is None or undo_stack is None:
                                valid = False
                            if valid:
                                score = self.evaluate(game_engine)
                                scored_pairs.append((score, [pawn, stack_move]))
                            game_engine.undo_move(stack_move, undo_stack)
                            found_valid = True
            if not found_valid:
                if undo_pawn is not None:
                    score = self.evaluate(game_engine)
                    scored_pairs.append((score, [pawn]))
            game_engine.undo_move(pawn, undo_pawn)
        # Stack-only moves if no pawn moves are possible
        if not scored_pairs:
            for row, col in getattr(game_engine, 'stacks', []):
                if game_engine.board[row][col]:
                    top_piece = game_engine.board[row][col][-1]
                    if top_piece.name == 'Square':
                        for end_pos in game_engine.get_valid_stack_moves(row, col):
                            stack_move = ('stack_pieces', (row, col), end_pos)
                            undo_stack = game_engine.apply_move(stack_move)
                            if undo_stack is not None:
                                score = self.evaluate(game_engine)
                                scored_pairs.append((score, [stack_move]))
                            game_engine.undo_move(stack_move, undo_stack)
        scored_pairs.sort(reverse=True, key=lambda x: x[0])
        pairs = [pair for score, pair in scored_pairs]
        return pairs


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
                game_engine, 
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
        print("[DEBUG] Endgame strategy activated")
        best_combo = None
        best_score = float('-inf')
        max_height = self.get_max_height(game_engine)
        pawn_moves = [m for m in self.get_all_moves(game_engine, self.color) if m[0] == 'move_pion']
        stack_moves = [m for m in self.get_all_moves(game_engine, self.color) if m[0] == 'stack_pieces']
        print("[DEBUG] pawn_moves:", pawn_moves)
        print("[DEBUG] stack_moves:", stack_moves)
        for pawn in pawn_moves:
            pawn_end = pawn[2]
            for stack in stack_moves:
                stack_end = stack[2]
                stack_start = stack[1]
                print(f"[DEBUG] Evaluating pawn {pawn} with stack {stack}")
                if pawn_end == stack_start or pawn_end == stack_end:
                    print(f"[DEBUG] Skipping invalid combo: {pawn} with {stack}")
                    continue
                if self.is_valid_combo(pawn, stack):
                    undo_pawn = game_engine.apply_move(pawn)
                    undo_stack = game_engine.apply_move(stack)
                    if undo_pawn is not None and undo_stack is not None:
                        score = self.endgame_evaluate(game_engine, max_height)
                        if score > best_score:
                            best_score = score
                            best_combo = (pawn, stack)
                    if undo_stack is not None:
                        game_engine.undo_move(stack, undo_stack)
                    if undo_pawn is not None:
                        game_engine.undo_move(pawn, undo_pawn)
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
        print("Minimax is used")
        game_hash = self.zobrist_hash(game)
        if game_hash in self.transposition_table:
            entry = self.transposition_table[game_hash]
            if entry['depth'] >= depth:
                if entry['maximizing'] == maximizing_player:
                    return entry['value'], entry['best_move']
        if depth == 0 or game.check_game_over():
            eval_score = self.evaluate(game)
            print(f"[MINIMAX EVAL] depth={depth}, maximizing={maximizing_player}, score={eval_score}")
            return eval_score, None
        
        # Get current position score for relative thresholds
        current_score = self.evaluate(game)
        
        # Count remaining pieces for dynamic optimization
        num_stacks = len(getattr(game, 'stacks', []))
        num_pawns = len(getattr(game, 'pawns', []))
        total_pieces = num_stacks + num_pawns
        
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            valid_move_pairs = self.get_all_move_pairs(game, self.color)
            
            # Dynamic move limiting based on game phase
            print("AAAA")
            print(total_pieces)
            if depth >= 2:
                if total_pieces <= 10:  # Late game - be thorough
                    valid_move_pairs = valid_move_pairs[:15]
                elif total_pieces <= 75:  # Mid game - moderate
                    valid_move_pairs = valid_move_pairs[:20]
                else:  # Early game - keep current optimization
                    valid_move_pairs = valid_move_pairs[:4]
            
            for move_pair in valid_move_pairs:
                undo_infos = []
                valid = True
                for move in move_pair:
                    undo_info = game.apply_move(move)
                    if undo_info is None:
                        valid = False
                        break
                    undo_infos.append((move, undo_info))
                if valid:
                    game.current_player = 'white' if game.current_player == 'black' else 'black'
                    eval_score, _ = self.minimax(game, depth - 1, False, alpha, beta)
                    game.current_player = 'white' if game.current_player == 'black' else 'black'
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = move_pair
                    # Early termination only in early/mid game
                    if total_pieces > 10 and eval_score >= current_score + 10:
                        for move, undo_info in reversed(undo_infos):
                            game.undo_move(move, undo_info)
                        return eval_score, move_pair
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        for move, undo_info in reversed(undo_infos):
                            game.undo_move(move, undo_info)
                        break
                for move, undo_info in reversed(undo_infos):
                    game.undo_move(move, undo_info)
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
            
            # Dynamic move limiting based on game phase
            if depth >= 2:
                if total_pieces <= 50:  # Late game - be thorough
                    valid_move_pairs = valid_move_pairs[:25]
                elif total_pieces <= 75:  # Mid game - moderate
                    valid_move_pairs = valid_move_pairs[:20]
                else:  # Early game - keep current optimization
                    valid_move_pairs = valid_move_pairs[:2]
            
            for move_pair in valid_move_pairs:
                undo_infos = []
                valid = True
                for move in move_pair:
                    undo_info = game.apply_move(move)
                    if undo_info is None:
                        valid = False
                        break
                    undo_infos.append((move, undo_info))
                if valid:
                    game.current_player = 'white' if game.current_player == 'black' else 'black'
                    eval_score, _ = self.minimax(game, depth - 1, True, alpha, beta)
                    game.current_player = 'white' if game.current_player == 'black' else 'black'
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = move_pair
                    # Early termination only in early/mid game
                    if total_pieces > 50 and eval_score <= current_score - 10:
                        for move, undo_info in reversed(undo_infos):
                            game.undo_move(move, undo_info)
                        return eval_score, move_pair
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        for move, undo_info in reversed(undo_infos):
                            game.undo_move(move, undo_info)
                        break
                for move, undo_info in reversed(undo_infos):
                    game.undo_move(move, undo_info)
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
            if not move:
                print('[MinMaxAI] No move found by minimax, falling back to RandomAI')
                random_ai = RandomAI(self.color)
                move = random_ai.make_decision(game_engine)
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
        pawns = getattr(game_engine, 'pawns', [])
        stacks = getattr(game_engine, 'stacks', [])
        while iteration < max_iterations:
            iteration += 1
            pion_moves = []
            stack_moves = []
            # Use fast sets for pawns
            for i, j in pawns:
                if game_engine.board[i][j]:
                    piece = game_engine.board[i][j][-1]
                    if hasattr(piece, 'name') and piece.name == 'Pawn' and piece.color == self.color:
                        valid_moves = game_engine.get_pawn_moves(piece, i, j)
                        if valid_moves:
                            for end_pos in valid_moves:
                                pion_moves.append(('move_pion', (i, j), end_pos))
            # Use fast sets for stacks
            for i, j in stacks:
                if game_engine.board[i][j]:
                    piece = game_engine.board[i][j][-1]
                    if piece.name == 'Square':
                        valid_moves = game_engine.get_square_moves(piece, i, j)
                        if valid_moves:
                            for end_pos in valid_moves:
                                stack_moves.append(('stack_pieces', (i, j), end_pos))
            if not pion_moves and not stack_moves:
                pion_move = random.choice(pion_moves)
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                for stack_move in stack_moves:
                    if pion_move[2] != stack_move[1] and pion_move[2] != stack_move[2]:
                        print(f"[RandomAI] Found valid move pair: {pion_move[2]}, {stack_move[1]}, {stack_move[2]}")
                        return [pion_move, stack_move]
                    else:
                        continue
                
                               
            
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
        super().__init__(color, depth=2)
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