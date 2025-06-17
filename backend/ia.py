import copy
import random

class MinMaxAI:
    def __init__(self, color, depth=2):
        self.color = color  # 'white' or 'black'
        self.depth = depth

    def make_decision(self, game_engine):
        """
        Selects and returns the best possible pair of actions (move_pion and stack_pieces).
        :param game_engine: Instance of GameEngine
        :return: [(type_move, start_pos, end_pos), (type_move, start_pos, end_pos)]
        """
        all_moves = self.get_all_moves(game_engine, self.color)

        best_pair = None
        best_score = float('-inf')

        for move in all_moves:
            for stack in all_moves:
                if move[0] == 'pawn' and stack[0] == 'stack':
                    new_game = copy.deepcopy(game_engine)
                    self.apply_move(new_game, move)
                    self.apply_move(new_game, stack)
                    score = self.minmax(new_game, self.depth - 1, False, float('-inf'), float('inf'))
                    if score > best_score:
                        best_score = score
                        best_pair = (move, stack)

        if best_pair:
            m, s = best_pair
            move_action = ('move_pion', (m[1], m[2]), (m[3], m[4])) if len(m) == 5 else ('move_pion', (m[1][0], m[1][1]), (m[1][2], m[1][3]))
            stack_action = ('stack_pieces', (s[1], s[2]), (s[3], s[4])) if len(s) == 5 else ('stack_pieces', (s[1][0], s[1][1]), (s[1][2], s[1][3]))
            return [move_action, stack_action]

        return []

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
        moves = []
        for row in range(8):
            for col in range(8):
                # Pawn moves
                for move in game_engine.get_valid_moves(row, col):
                    if move and game_engine.board[row][col] and hasattr(game_engine.board[row][col][-1], 'name') and game_engine.board[row][col][-1].name == 'Pawn' and game_engine.board[row][col][-1].color == color:
                        moves.append(("pawn", row, col, move[0], move[1]))
                        break
                # Stack moves
                for move in getattr(game_engine, 'get_valid_stack_moves', lambda r, c: [])(row, col):
                    if move:
                        moves.append(("stack", row, col, move[0], move[1]))
                        break
                break
            break
        return moves

    def apply_move(self, game_engine, move):
        kind = move[0]
        params = move[1:]
        if kind == "pawn":
            game_engine.move_pion(*params)
        elif kind == "stack":
            game_engine.stack_pieces(*params)

    def evaluate(self, game_engine):
        white, black = 0, 0
        for row in range(8):
            for col in range(8):
                for piece in game_engine.board[row][col]:
                    if hasattr(piece, 'name') and piece.name == 'Pawn':
                        if piece.color == 'white':
                            white += 1
                        elif piece.color == 'black':
                            black += 1
        return white - black if self.color == 'white' else black - white


class RandomAI:
    def __init__(self, color, depth=2):
        self.color = color  # 'white' or 'black'

    def make_decision(self, game_engine):
        board = game_engine.board
        pion_moves = []
        stack_moves = []
        for i in range(8):
            for j in range(8):
                # Check pawn moves
                if board[i][j]:
                    piece = board[i][j][-1]
                    if hasattr(piece, 'name') and piece.name == 'Pawn' and piece.color == self.color:
                        valid_moves = game_engine.get_pawn_moves(piece, i, j)
                        end_pos = random.choice(valid_moves)
                        print("ccccccccccccccccccccccccccccccccccccc")
                        pion_moves.append(('move_pion', (i, j), end_pos))
                    elif hasattr(piece, 'name') and piece.name == 'Pawn':
                        break
                    else:
                        # Check stack moves
                        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                        valid_moves = game_engine.get_valid_stack_moves(i, j)
                        if valid_moves:
                            end_pos = random.choice(valid_moves)
                            stack_moves.append(('stack_pieces', (i, j), end_pos))
        
        if pion_moves and stack_moves:
            move = random.choice(pion_moves)
            stack = random.choice(stack_moves)
            return [move, stack]
