import copy
import random

class MinMaxAI:
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth

    def evaluate(self, game_engine):
        score = 0
        for row in range(8):
            for col in range(8):
                for i, piece in enumerate(game_engine.board[row][col]):
                    if hasattr(piece, 'name') and piece.name == 'Pawn':
                        value = 10 + i  
                        if piece.color == self.color:
                            score += value
                        else:
                            score -= value
        return score


    def get_all_moves(self, game_engine, color):
        moves = []
        for row in range(8):
            for col in range(8):
                if game_engine.board[row][col]:
                    top_piece = game_engine.board[row][col][-1]
                    if hasattr(top_piece, 'name') and top_piece.name == 'Pawn' and top_piece.color == color:
                        for move in game_engine.get_pawn_moves(top_piece, row, col):
                            moves.append(("move_pion", (row, col), (move[0], move[1])))
                    elif top_piece.name != "Pawn":
                        valid_moves = game_engine.get_valid_stack_moves(row, col)
                        if valid_moves:
                            for end_pos in valid_moves:
                                moves.append(("stack_pieces", (row, col), end_pos))
        return moves


    def is_valid_combo(self, pawn_move, stack_move):
        # pawn_move: ("move_pion", (row, col), (to_row, to_col))
        # stack_move: ("stack_pieces", (row, col), (to_row, to_col))
        return (
            pawn_move[2][0] == stack_move[1][0] and  # Pawn moves to the square where stack move starts
            pawn_move[2][1] == stack_move[1][1]
        )

    def get_best_move(self, game_engine):
        all_moves = self.get_all_moves(game_engine, self.color)
        pawn_moves = [m for m in all_moves if m[0] == 'move_pion']
        stack_moves = [m for m in all_moves if m[0] == 'stack_pieces']

        best_eval = float('-inf')
        best_combo = None

        print(f"[AI] Calculating best combo for {self.color} (depth {self.depth})")

        for pawn in pawn_moves:
            for stack in stack_moves:
                if self.is_valid_combo(pawn, stack):
                    temp_game = game_engine.clone()
                    temp_game.move_piece(pawn[1][0], pawn[1][1], pawn[2][0], pawn[2][1])
                    valid_stack_moves = temp_game.get_valid_stack_moves(stack[1][0], stack[1][1])
                    
                    if stack[2] in valid_stack_moves:
                        temp_game.stack_pieces(stack[1][0], stack[1][1], stack[2][0], stack[2][1])
                        temp_game.current_player = 'white' if self.color == 'black' else 'black'

                        eval_score, _ = self.minimax(
                            temp_game,
                            self.depth - 1,
                            maximizing_player=False,
                            alpha=float('-inf'),
                            beta=float('inf')
                        )
                        print(f"[DEBUG] Combo: {pawn}, {stack} => Eval = {eval_score}")
                        
                        if eval_score > best_eval:
                            best_eval = eval_score
                            best_combo = (pawn, stack)

        if best_combo:
            print(f"[AI] Best combo: {best_combo} with eval = {best_eval}")
            return [best_combo[0], best_combo[1]]
        else:
            # Fallback: use RandomAI logic to get a random valid pair
            print("[AI] No valid combo found, fallback to RandomAI")
            random_ai = RandomAI(self.color)
            random_move = random_ai.make_decision(game_engine)
            if random_move is None:
                print("[ERROR] No valid moves found in MinimaxAI")
                # Try to find any valid move, even if it's not optimal
                for i in range(8):
                    for j in range(8):
                        if game_engine.board[i][j]:
                            piece = game_engine.board[i][j][-1]
                            if hasattr(piece, 'name') and piece.name == 'Pawn' and piece.color == self.color:
                                valid_moves = game_engine.get_pawn_moves(piece, i, j)
                                if valid_moves:
                                    move = ('move_pion', (i, j), valid_moves[0])
                                    print(f"[AI] Emergency fallback move: {move}")
                                    return [move]
                return None
            return random_move


    def minimax(self, game, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or game.game_over:
            eval_score = self.evaluate(game)
            print(f"[DEBUG] Eval at depth 0 (or terminal): {eval_score}")
            return eval_score, None

        valid_moves = self.get_all_moves(game, game.current_player)

        if not valid_moves:
            print(f"[DEBUG] No valid moves for {game.current_player}")
            return self.evaluate(game), None

        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                new_game = game.clone()
                if move[0] == 'move_pion':
                    new_game.move_piece(move[1][0], move[1][1], move[2][0], move[2][1])
                elif move[0] == 'stack_pieces':
                    new_game.stack_pieces(move[1][0], move[1][1], move[2][0], move[2][1])
                new_game.current_player = 'white' if new_game.current_player == 'black' else 'black'

                eval_score, _ = self.minimax(new_game, depth - 1, False, alpha, beta)
                print(f"[DEBUG] Max: Trying move {move}, Eval = {eval_score}, Alpha = {alpha}, Beta = {beta}")

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    print(f"[DEBUG] Max: Pruning branch at move {move} with Alpha = {alpha}, Beta = {beta}")
                    break

            print(f"[DEBUG] Max: Chose move {best_move} with score {max_eval}")
            return max_eval, best_move

        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_game = game.clone()
                if move[0] == 'move_pion':
                    new_game.move_piece(move[1][0], move[1][1], move[2][0], move[2][1])
                elif move[0] == 'stack_pieces':
                    new_game.stack_pieces(move[1][0], move[1][1], move[2][0], move[2][1])
                new_game.current_player = 'white' if new_game.current_player == 'black' else 'black'

                eval_score, _ = self.minimax(new_game, depth - 1, True, alpha, beta)
                print(f"[DEBUG] Min: Trying move {move}, Eval = {eval_score}, Alpha = {alpha}, Beta = {beta}")

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)

                if beta <= alpha:
                    print(f"[DEBUG] Min: Pruning branch at move {move} with Alpha = {alpha}, Beta = {beta}")
                    break

            print(f"[DEBUG] Min: Chose move {best_move} with score {min_eval}")
            return min_eval, best_move


    def make_decision(self, game_engine):
        return self.get_best_move(game_engine)


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
