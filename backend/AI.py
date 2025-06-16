import random
import math
from game_engine import GameEngine

class GameAI:
    def __init__(self, difficulty_level, couleur):
        self.difficulty_level = difficulty_level
        self.couleur = couleur  # 'white' ou 'black'
        self.probability_map = {
            'easy': 0.3,    # 30% de probabilité de prendre la bonne décision
            'medium': 0.6,  # 60% de probabilité de prendre la bonne décision
            'hard': 0.9     # 90% de probabilité de prendre la bonne décision
        }
        self.max_depth = {
            'easy': 2,      # Profondeur de recherche pour niveau facile
            'medium': 3,    # Profondeur de recherche pour niveau moyen
            'hard': 4       # Profondeur de recherche pour niveau difficile
        }
        
    def make_decision(self, game_engine):
        """
        Prend une décision pour le tour actuel
        :param game_engine: Instance de GameEngine
        :return: (type_move, start_pos, end_pos) où type_move est 'move_pion' ou 'stack_pieces'
        """
        # Obtenir la probabilité basée sur le niveau de difficulté
        correct_probability = self.probability_map[self.difficulty_level]
        
        # Décider si on prend la bonne décision ou non
        if random.random() < correct_probability:
            return self._get_best_move(game_engine)
        else:
            return self._get_random_move(game_engine)
    
    def _get_best_move(self, game_engine):
        """
        Trouve le meilleur mouvement en utilisant l'algorithme MinMax
        :param game_engine: Instance de GameEngine
        :return: (type_move, start_pos, end_pos)
        """
        best_score = float('-inf')
        best_move = None
        depth = self.max_depth[self.difficulty_level]
        
        # Obtenir tous les mouvements possibles
        possible_moves = self._get_all_possible_moves(game_engine)
        
        for move in possible_moves:
            # Simuler le mouvement
            new_engine = self._simulate_move(game_engine, move)
            # Calculer le score avec MinMax
            score = self._minmax(new_engine, depth - 1, False)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move if best_move else self._get_random_move(game_engine)
    
    def _get_all_possible_moves(self, game_engine):
        """
        Trouve tous les mouvements possibles pour le joueur actuel
        :param game_engine: Instance de GameEngine
        :return: Liste des mouvements possibles [(type_move, start_pos, end_pos)]
        """
        moves = []
        
        # Parcourir toutes les cases du plateau
        for i in range(8):
            for j in range(8):
                # Vérifier les mouvements de pion
                if game_engine.board[i][j]:
                    piece = game_engine.board[i][j][-1]
                    if hasattr(piece, 'name') and piece.name == 'Pawn' and piece.color == self.couleur:
                        valid_moves = game_engine.get_pawn_moves(piece, i, j)
                        for end_pos in valid_moves:
                            moves.append(('move_pion', (i, j), end_pos))
                
                # Vérifier les mouvements d'EPC
                if game_engine.can_stack(self.couleur):
                    valid_moves = game_engine.get_valid_stack_moves(i, j)
                    for end_pos in valid_moves:
                        moves.append(('stack_pieces', (i, j), end_pos))
        
        return moves
    
    def _simulate_move(self, game_engine, move):
        """
        Simule un mouvement sur le plateau
        :param game_engine: Instance de GameEngine
        :param move: (type_move, start_pos, end_pos)
        :return: Nouvelle instance de GameEngine avec le mouvement effectué
        """
        new_engine = GameEngine()
        new_engine.board = [row[:] for row in game_engine.board]
        new_engine.current_player = game_engine.current_player
        
        type_move, start_pos, end_pos = move
        if type_move == 'move_pion':
            new_engine.move_pion(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
        else:  # stack_pieces
            new_engine.stack_pieces(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
            
        return new_engine
    
    def _minmax(self, game_engine, depth, is_maximizing):
        """
        Implémentation de l'algorithme MinMax
        :param game_engine: Instance de GameEngine
        :param depth: Profondeur de recherche restante
        :param is_maximizing: True si c'est le tour du joueur maximisant
        :return: Score du meilleur mouvement
        """
        if depth == 0 or game_engine.check_game_over():
            return self._evaluate_state(game_engine)
            
        if is_maximizing:
            max_eval = float('-inf')
            moves = self._get_all_possible_moves(game_engine)
            
            for move in moves:
                new_engine = self._simulate_move(game_engine, move)
                eval = self._minmax(new_engine, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            moves = self._get_all_possible_moves(game_engine)
            
            for move in moves:
                new_engine = self._simulate_move(game_engine, move)
                eval = self._minmax(new_engine, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval
    
    def _evaluate_state(self, game_engine):
        """
        Évalue l'état du jeu en fonction du total d'EPC contrôlé par chaque équipe
        :param game_engine: Instance de GameEngine
        :return: Score de l'état (positif si avantage pour l'IA, négatif sinon)
        """
        total_epc_ia = 0
        total_epc_adversaire = 0
        
        # Parcourir toutes les cases du plateau
        for i in range(8):
            for j in range(8):
                if game_engine.board[i][j]:
                    # Compter le nombre de pièces carrées (EPC) dans la pile
                    pile = [p for p in game_engine.board[i][j] if hasattr(p, 'name') and p.name == 'Square']
                    epc = len(pile)
                    
                    # Vérifier si un pion contrôle cette pile
                    for piece in game_engine.board[i][j]:
                        if hasattr(piece, 'name') and piece.name == 'Pawn':
                            if piece.color == self.couleur:
                                total_epc_ia += epc
                            else:
                                total_epc_adversaire += epc
                            break
        
        # Retourner la différence des EPC
        return total_epc_ia - total_epc_adversaire
    
    def _get_random_move(self, game_engine):
        """
        Retourne un mouvement aléatoire valide
        :param game_engine: Instance de GameEngine
        :return: (type_move, start_pos, end_pos)
        """
        moves = self._get_all_possible_moves(game_engine)
        return random.choice(moves) if moves else None


