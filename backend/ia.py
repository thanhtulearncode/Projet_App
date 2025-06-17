import copy

class MinMaxAI:
    def __init__(self, color, depth=2):
        self.color = color  # 'white' ou 'black'
        self.depth = depth

    def make_decision(self, game_engine):
        """
        Prend une décision pour le tour actuel
        :param game_engine: Instance de GameEngine
        :return: (type_move, start_pos, end_pos) où type_move est 'move_pion' ou 'stack_pieces'
        """
        move = self.get_best_move(game_engine)
        if move:
            kind, (start_row, start_col, end_row, end_col) = move
            if kind == "pawn":
                return ('move_pion', (start_row, start_col), (end_row, end_col))
            else:  # stack
                return ('stack_pieces', (start_row, start_col), (end_row, end_col))
        return None

    def get_best_move(self, game_engine):
        best_score = float('-inf')
        best_move = None
        for move in self.get_all_moves(game_engine, self.color):
            new_game = copy.deepcopy(game_engine)
            self.apply_move(new_game, move)
            score = self.minmax(new_game, self.depth - 1, False, float('-inf'), float('inf'))
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minmax(self, game_engine, depth, maximizing, alpha, beta):
        if depth == 0 or game_engine.check_game_over():
            return self.evaluate(game_engine)
        color = self.color if maximizing else ('black' if self.color == 'white' else 'white')
        moves = self.get_all_moves(game_engine, color)
        if maximizing:
            max_eval = float('-inf')
            for move in moves:
                new_game = copy.deepcopy(game_engine)
                self.apply_move(new_game, move)
                eval = self.minmax(new_game, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                new_game = copy.deepcopy(game_engine)
                self.apply_move(new_game, move)
                eval = self.minmax(new_game, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_all_moves(self, game_engine, color):
        # À compléter : générer tous les coups légaux pour 'color' en utilisant game_engine
        # Exemples : [("pawn", (start_row, start_col, end_row, end_col)), ("stack", (src_row, src_col, dst_row, dst_col))]
        moves = []
        for row in range(8):
            for col in range(8):
                # Pions
                for move in game_engine.get_valid_moves(row, col):
                    if move and game_engine.board[row][col] and hasattr(game_engine.board[row][col][-1], 'name') and game_engine.board[row][col][-1].name == 'Pawn' and game_engine.board[row][col][-1].color == color:
                        moves.append(("pawn", (row, col, move[0], move[1])))
                # Empilements
                for move in getattr(game_engine, 'get_valid_stack_moves', lambda r, c: [])(row, col):
                    if move:
                        moves.append(("stack", (row, col, move[0], move[1])))
        return moves

    def apply_move(self, game_engine, move):
        kind, params = move
        if kind == "pawn":
            game_engine.move_pion(*params)
        elif kind == "stack":
            game_engine.stack_pieces(*params)

    def evaluate(self, game_engine):
        # Fonction d'évaluation simple : différence de pions
        white, black = 0, 0
        for row in range(8):
            for col in range(8):
                for piece in game_engine.board[row][col]:
                    if hasattr(piece, 'name') and piece.name == 'Pawn':
                        if piece.color == 'white':
                            white += 1
                        elif piece.color == 'black':
                            black += 1
        if self.color == 'white':
            return white - black
        else:
            return black - white
