import random
import math

class GameAI:
    def __init__(self, difficulty_level, couleur):
        self.difficulty_level = difficulty_level
        self.couleur = couleur  # 'AI1' ou 'AI2'
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
        
    def make_decision(self, board, possible_moves):
        # Obtenir la probabilité basée sur le niveau de difficulté
        correct_probability = self.probability_map[self.difficulty_level]
        
        # Décider si on prend la bonne décision ou non
        if random.random() < correct_probability:
            # Prendre la bonne décision (optimale)
            return self._get_best_move(board, possible_moves)
        else:
            # Prendre une mauvaise décision (aléatoire)
            return random.choice(possible_moves)
    
    def _get_best_move(self, board, possible_moves):
        """
        Trouve le meilleur mouvement en utilisant l'algorithme MinMax
        :param board: Le plateau de jeu
        :param possible_moves: Liste des mouvements possibles
        :return: Meilleur mouvement
        """
        best_score = float('-inf')
        best_move = None
        depth = self.max_depth[self.difficulty_level]
        
        # Élagage alpha-beta
        alpha = float('-inf')
        beta = float('inf')
        
        for move in possible_moves:
            # Simuler le mouvement
            new_board = self._simulate_move(board, move)
            # Calculer le score avec MinMax
            score = self._minmax(new_board, depth - 1, False, alpha, beta)
            
            if score > best_score:
                best_score = score
                best_move = move
                
            alpha = max(alpha, best_score)
            
        return best_move if best_move else random.choice(possible_moves)
    
    def _minmax(self, board, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        """
        Implémentation de l'algorithme MinMax avec élagage alpha-beta
        :param board: Le plateau de jeu
        :param depth: Profondeur de recherche restante
        :param is_maximizing: True si c'est le tour du joueur maximisant
        :param alpha: Valeur alpha pour l'élagage
        :param beta: Valeur beta pour l'élagage
        :return: Score du meilleur mouvement
        """
        # Si on atteint la profondeur maximale ou un état terminal
        if depth == 0 or self._is_terminal_state(board):
            return self._evaluate_state(board)
            
        if is_maximizing:
            max_eval = float('-inf')
            moves = self._get_possible_moves(board)
            
            for move in moves:
                # Simuler le mouvement
                new_board = self._simulate_move(board, move)
                # Évaluer récursivement
                eval = self._minmax(new_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Élagage beta
            return max_eval
        else:
            min_eval = float('inf')
            moves = self._get_possible_moves(board)
            
            for move in moves:
                # Simuler le mouvement
                new_board = self._simulate_move(board, move)
                # Évaluer récursivement
                eval = self._minmax(new_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Élagage alpha
            return min_eval
    
    def _evaluate_state(self, board):
        """
        Évalue l'état du jeu en tenant compte des deux phases
        """
        pieces_avec_epc = 0
        epc_ia1 = 0
        epc_ia2 = 0
        positions_strategiques_ia1 = 0
        positions_strategiques_ia2 = 0
        
        # Parcourir toutes les cases du plateau
        for i in range(board.taille):
            for j in range(board.taille):
                piece = board.obtenir_cell(i, j)
                if piece.epc > 0:
                    pieces_avec_epc += 1
                    # Si la case est occupée par un pion
                    if piece.est_occupee():
                        # Ajouter l'EPC au score du joueur correspondant
                        if piece.pion.couleur == 'AI1':
                            epc_ia1 += piece.epc
                            # Bonus pour les positions stratégiques (près du centre)
                            distance_centre = abs(i - board.taille//2) + abs(j - board.taille//2)
                            positions_strategiques_ia1 += (board.taille - distance_centre)
                        elif piece.pion.couleur == 'AI2':
                            epc_ia2 += piece.epc
                            distance_centre = abs(i - board.taille//2) + abs(j - board.taille//2)
                            positions_strategiques_ia2 += (board.taille - distance_centre)
        
        # Si c'est un état terminal (plus de mouvements possibles)
        if self._is_terminal_state(board):
            # Retourner la différence des scores en fonction de la couleur de l'IA
            return (epc_ia1 - epc_ia2) if self.couleur == 'AI1' else (epc_ia2 - epc_ia1)
            
        # Sinon, calculer un score qui prend en compte l'EPC et les positions stratégiques
        score_ia1 = epc_ia1 + (positions_strategiques_ia1 * 0.1)
        score_ia2 = epc_ia2 + (positions_strategiques_ia2 * 0.1)
        
        return (score_ia1 - score_ia2) if self.couleur == 'AI1' else (score_ia2 - score_ia1)
    
    def _is_terminal_state(self, board):
        """
        Vérifie si l'état du jeu est terminal (plus de mouvements possibles)
        :param board: Le plateau de jeu
        :return: True si l'état est terminal
        """
        # Vérifier s'il y a des mouvements possibles pour chaque pion
        for i in range(board.taille):
            for j in range(board.taille):
                piece = board.obtenir_cell(i, j)
                if piece.est_occupee():
                    # Vérifier les mouvements possibles en phase 1
                    for dx in range(-piece.epc, piece.epc + 1):
                        for dy in range(-piece.epc, piece.epc + 1):
                            if dx == 0 and dy == 0:
                                continue
                            x_arrivee = i + dx
                            y_arrivee = j + dy
                            if board.est_valide_position(x_arrivee, y_arrivee):
                                if piece.pion.peut_deplacer_vers(board, x_arrivee, y_arrivee):
                                    return False
                
                # Vérifier les mouvements possibles en phase 2 pour chaque case avec EPC > 0
                if piece.epc > 0:
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    for dx, dy in directions:
                        x_adjacent = i + dx
                        y_adjacent = j + dy
                        if board.est_valide_position(x_adjacent, y_adjacent):
                            piece_adjacente = board.obtenir_cell(x_adjacent, y_adjacent)
                            if not piece_adjacente.est_occupee() and piece.epc + piece_adjacente.epc <= 5:
                                return False
        
        # Si aucun mouvement n'est possible, c'est un état terminal
        return True
    
    def _get_possible_moves(self, board):
        """
        Trouve tous les mouvements possibles pour le pion actuel, incluant la phase 2
        :param board: Le plateau de jeu
        :return: Liste des mouvements possibles [(x_depart, y_depart, x_arrivee, y_arrivee, phase)]
        """
        moves = []
        
        # Parcourir toutes les cases du plateau
        for i in range(board.taille):
            for j in range(board.taille):
                piece = board.obtenir_cell(i, j)
                
                # Si la case contient un pion de la couleur de l'IA
                if piece.est_occupee() and piece.pion.couleur == self.couleur:
                    # Obtenir l'EPC de la case
                    epc = piece.epc
                    
                    # Phase 1: Vérifier toutes les cases dans la zone de déplacement
                    for dx in range(-epc, epc + 1):
                        for dy in range(-epc, epc + 1):
                            # Ignorer la case actuelle
                            if dx == 0 and dy == 0:
                                continue
                                
                            # Calculer la nouvelle position
                            x_arrivee = i + dx
                            y_arrivee = j + dy
                            
                            # Vérifier si la position est valide
                            if not board.est_valide_position(x_arrivee, y_arrivee):
                                continue
                                
                            # Vérifier si le déplacement est valide
                            if piece.pion.peut_deplacer_vers(board, x_arrivee, y_arrivee, phase=1):
                                moves.append((i, j, x_arrivee, y_arrivee, 1))
                    
                    # Phase 2: Vérifier les cases adjacentes pour le transfert d'EPC
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # droite, bas, gauche, haut
                    for dx, dy in directions:
                        x_adjacent = i + dx
                        y_adjacent = j + dy
                        
                        if board.est_valide_position(x_adjacent, y_adjacent):
                            piece_adjacente = board.obtenir_cell(x_adjacent, y_adjacent)
                            if piece_adjacente.epc > 0 and piece.epc + piece_adjacente.epc <= 5:
                                moves.append((i, j, x_adjacent, y_adjacent, 2))
        
        return moves

    def _get_possible_moves_phase2(self, board, x_pion, y_pion):
        """
        Trouve tous les mouvements possibles pour la phase 2
        :param board: Le plateau de jeu
        :param x_pion, y_pion: Position du pion après la phase 1 (non utilisé pour la phase 2)
        :return: Liste des mouvements possibles [(x_depart, y_depart, x_arrivee, y_arrivee)]
        """
        moves = []
        
        # Parcourir toutes les cases du plateau
        for i in range(board.taille):
            for j in range(board.taille):
                piece_source = board.obtenir_cell(i, j)
                
                # Vérifier si la case source a un EPC > 0
                if piece_source.epc <= 0:
                    continue
                
                # Vérifier les 4 cases adjacentes
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # droite, bas, gauche, haut
                for dx, dy in directions:
                    x_adjacent = i + dx
                    y_adjacent = j + dy
                    
                    if not board.est_valide_position(x_adjacent, y_adjacent):
                        continue
                        
                    piece_destination = board.obtenir_cell(x_adjacent, y_adjacent)
                    
                    # Vérifier si la case destination est libre
                    if piece_destination.est_occupee():
                        continue
                        
                    # Vérifier si la somme des EPC est ≤ 5
                    if piece_destination.epc + piece_source.epc > 5:
                        continue
                        
                    moves.append((i, j, x_adjacent, y_adjacent))
                    
        return moves

    def _simulate_move(self, board, move):
        """
        Simule un mouvement sur le plateau, incluant la phase 2
        :param board: Le plateau de jeu
        :param move: Le mouvement à simuler (x_depart, y_depart, x_arrivee, y_arrivee)
        :return: Une copie du plateau avec le mouvement effectué
        """
        # Créer une copie profonde du plateau
        new_board = board.__class__(board.taille)
        for i in range(board.taille):
            for j in range(board.taille):
                piece_original = board.obtenir_cell(i, j)
                piece_copie = new_board.obtenir_cell(i, j)
                piece_copie.epc = piece_original.epc
                if piece_original.est_occupee():
                    pion_copie = pion(piece_original.pion.couleur)
                    piece_copie.placer_pion(pion_copie)

        # Simuler la phase 1
        x_depart, y_depart, x_arrivee, y_arrivee = move
        new_board.deplacer_piece_phase1(x_depart, y_depart, x_arrivee, y_arrivee)
        
        # Simuler la phase 2
        moves_phase2 = self._get_possible_moves_phase2(new_board, x_arrivee, y_arrivee)
        if moves_phase2:
            # Choisir le meilleur mouvement de phase 2
            best_move_phase2 = self._get_best_move_phase2(new_board, moves_phase2)
            if best_move_phase2:
                x2_depart, y2_depart, x2_arrivee, y2_arrivee = best_move_phase2
                new_board.deplacer_epc_phase2(x2_depart, y2_depart, x2_arrivee, y2_arrivee)
        
        return new_board

    def _get_best_move_phase2(self, board, possible_moves):
        """
        Trouve le meilleur mouvement pour la phase 2
        :param board: Le plateau de jeu
        :param possible_moves: Liste des mouvements possibles
        :return: Meilleur mouvement
        """
        best_score = float('-inf')
        best_move = None
        
        for move in possible_moves:
            # Créer une copie du plateau pour la simulation
            temp_board = board.__class__(board.taille)
            for i in range(board.taille):
                for j in range(board.taille):
                    piece_original = board.obtenir_cell(i, j)
                    piece_copie = temp_board.obtenir_cell(i, j)
                    piece_copie.epc = piece_original.epc
                    if piece_original.est_occupee():
                        pion_copie = pion(piece_original.pion.couleur)
                        piece_copie.placer_pion(pion_copie)
            
            # Simuler le mouvement
            x_depart, y_depart, x_arrivee, y_arrivee = move
            temp_board.deplacer_epc_phase2(x_depart, y_depart, x_arrivee, y_arrivee)
            
            # Évaluer le résultat
            score = self._evaluate_state(temp_board)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move if best_move else (possible_moves[0] if possible_moves else None)


