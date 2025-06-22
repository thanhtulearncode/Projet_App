"""tester le mode IA directement sur le terminal sans frontend"""
import math
import random

BOARD_SIZE = 8  

MAX_EPC_HEIGHT = 5

EMPTY = None
WHITE = 'W'
BLACK = 'B'

def initial_state():
    """
    Crée un état de jeu initial.
    Chaque case contient un EPC (empilement de 1).
    Les pions sont placés selon une configuration définie.
    """
    epcs = [[1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    pions = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for col in range(8):
        row = (col + 1) % 2
        if (col < 4) == (col % 2 == 0):
            pions[row][col] = BLACK
            pions[7-row][col] = WHITE
        else:
            pions[row][col] = WHITE
            pions[7-row][col] = BLACK

    return {"epcs": epcs, "pions": pions, "player": WHITE}

#print(initial_state())

def is_terminal(state):
    return len(possible_epc_moves(state)) == 0

def winner(state):
    """
    Determine the winner based on the number of pawns on buildings (EPCs of height 5),
    then 4, then 3, etc. Returns WHITE, BLACK, or None for draw.
    """
    epcs = state["epcs"]
    pions = state["pions"]
    counts = {WHITE: [0]*5, BLACK: [0]*5}  # index 0: height 1, ..., index 4: height 5
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            h = epcs[i][j]
            if h >= 1 and pions[i][j] in (WHITE, BLACK):
                counts[pions[i][j]][h-1] += 1
    # Compare from height 5 down to 1
    for h in range(4, -1, -1):
        if counts[WHITE][h] > counts[BLACK][h]:
            return WHITE
        elif counts[BLACK][h] > counts[WHITE][h]:
            return BLACK
    return None  # Draw

def evaluate_position(state):
    """
    Comprehensive evaluation function that considers:
    1. Piece values based on EPC height
    2. Position evaluation (center control, mobility)
    3. Piece structures (mutual protection)
    4. Tactical factors (offensive/defensive capabilities)
    5. Future advantages (move potential)
    """
    epcs = state["epcs"]
    pions = state["pions"]
    score = 0
    
    # 1. Piece Values and Position Evaluation
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if pions[i][j] in (WHITE, BLACK):
                piece_value = evaluate_piece_value(i, j, epcs[i][j], pions[i][j])
                position_bonus = evaluate_position_value(i, j, epcs[i][j])
                if pions[i][j] == WHITE:
                    score += piece_value + position_bonus
                else:
                    score -= piece_value + position_bonus
    
    # 2. Piece Structures (Mutual Protection)
    structure_score = evaluate_piece_structures(state)
    score += structure_score
    
    # 3. Tactical Factors
    tactical_score = evaluate_tactical_factors(state)
    score += tactical_score
    
    # 4. Mobility and Future Advantages
    mobility_score = evaluate_mobility(state)
    score += mobility_score
    
    return score

def evaluate_piece_value(i, j, epc_height, player):
    """Evaluate piece value based on EPC height with exponential scaling."""
    base_value = 10 ** (epc_height - 1)  # Height 1: 1, Height 2: 10, Height 3: 100, etc.
    return base_value

def evaluate_position_value(i, j, epc_height):
    """Evaluate position value - center control and strategic positions."""
    # Center control bonus
    center_distance = abs(i - 3.5) + abs(j - 3.5)  # Distance from center
    center_bonus = max(0, (7 - center_distance) * 5)  # Closer to center = higher bonus
    
    # Edge penalty for high EPCs (buildings should be in center)
    if epc_height >= 4:
        edge_penalty = 0
        if i == 0 or i == 7 or j == 0 or j == 7:
            edge_penalty = -50 * epc_height
    
    return center_bonus + edge_penalty

def evaluate_piece_structures(state):
    """Evaluate mutual protection and piece coordination."""
    epcs = state["epcs"]
    pions = state["pions"]
    score = 0
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if pions[i][j] in (WHITE, BLACK):
                player = pions[i][j]
                protection_bonus = 0
                
                # Check for adjacent friendly pieces (mutual protection)
                for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE:
                        if pions[ni][nj] == player:
                            # Adjacent friendly piece - mutual protection bonus
                            protection_bonus += 20
                            # Extra bonus for high EPCs protecting each other
                            if epcs[i][j] >= 3 and epcs[ni][nj] >= 3:
                                protection_bonus += 50
                
                if player == WHITE:
                    score += protection_bonus
                else:
                    score -= protection_bonus
    
    return score

def evaluate_tactical_factors(state):
    """Evaluate offensive and defensive capabilities."""
    epcs = state["epcs"]
    pions = state["pions"]
    score = 0
    
    # Control of center squares
    center_squares = [(3,3), (3,4), (4,3), (4,4)]
    for i, j in center_squares:
        if pions[i][j] in (WHITE, BLACK):
            center_control = epcs[i][j] * 100  # Higher EPC = more control
            if pions[i][j] == WHITE:
                score += center_control
            else:
                score -= center_control
    
    # Attack potential (pieces that can capture)
    attack_potential = evaluate_attack_potential(state)
    score += attack_potential
    
    # Defensive formation (pieces protecting each other)
    defensive_score = evaluate_defensive_formation(state)
    score += defensive_score
    
    return score

def evaluate_attack_potential(state):
    """Evaluate potential to capture opponent pieces."""
    epcs = state["epcs"]
    pions = state["pions"]
    score = 0
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if pions[i][j] in (WHITE, BLACK):
                player = pions[i][j]
                attack_value = 0
                
                # Check if this piece can attack opponent pieces
                for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                    for d in range(1, epcs[i][j] + 1):
                        ni, nj = i + d*di, j + d*dj
                        if not (0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE):
                            break
                        if pions[ni][nj] == player:
                            break  # Can't attack through friendly piece
                        if pions[ni][nj] in (WHITE, BLACK) and pions[ni][nj] != player:
                            # Can attack opponent piece
                            attack_value += epcs[ni][nj] * 50  # Value of target
                            break
                
                if player == WHITE:
                    score += attack_value
                else:
                    score -= attack_value
    
    return score

def evaluate_defensive_formation(state):
    """Evaluate defensive formation and safety."""
    epcs = state["epcs"]
    pions = state["pions"]
    score = 0
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if pions[i][j] in (WHITE, BLACK):
                player = pions[i][j]
                safety_bonus = 0
                
                # Check if piece is safe from immediate capture
                is_safe = True
                for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                    for d in range(1, 6):  # Check up to max EPC height
                        ni, nj = i + d*di, j + d*dj
                        if not (0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE):
                            break
                        if pions[ni][nj] in (WHITE, BLACK) and pions[ni][nj] != player:
                            # Opponent piece can reach this square
                            if epcs[ni][nj] >= d:  # Can actually reach here
                                is_safe = False
                                break
                        if pions[ni][nj] == player:
                            break
                
                if is_safe:
                    safety_bonus = epcs[i][j] * 30  # Higher EPC = more valuable to protect
                
                if player == WHITE:
                    score += safety_bonus
                else:
                    score -= safety_bonus
    
    return score

def evaluate_mobility(state):
    """Evaluate mobility and future move potential."""
    white_mobility = len(possible_pion_moves(state)) if state["player"] == WHITE else 0
    black_mobility = len(possible_pion_moves(state)) if state["player"] == BLACK else 0
    
    # Also consider EPC mobility
    white_epc_mobility = len(possible_epc_moves(state)) if state["player"] == WHITE else 0
    black_epc_mobility = len(possible_epc_moves(state)) if state["player"] == BLACK else 0
    
    total_white_mobility = white_mobility + white_epc_mobility
    total_black_mobility = black_mobility + black_epc_mobility
    
    return (total_white_mobility - total_black_mobility) * 10

def utility(state):
    """
    Returns the evaluation score for the current state.
    Positive values favor WHITE, negative values favor BLACK.
    """
    return evaluate_position(state)

def actions(state):
    """
    Renvoie la liste des actions possibles sous forme de tuples :
    ('move_pion', (i_from, j_from), (i_to, j_to))
    ('move_epc', (i_from, j_from), (i_to, j_to))
    """
    return possible_pion_moves(state) + possible_epc_moves(state)

def possible_pion_moves(state):
    moves = []
    epcs = state["epcs"]
    pions = state["pions"]
    player = state["player"]

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if pions[i][j] == player:
                max_dist = epcs[i][j]

                for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                    for d in range(1, max_dist + 1):
                        ni, nj = i + d*di, j + d*dj
                        if not (0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE):
                            break
                        if pions[ni][nj] == player:
                            break  # ne peut pas traverser un pion allié
                        if pions[ni][nj] == EMPTY or d == max_dist:
                            moves.append(('move_pion', (i, j), (ni, nj)))
                        if pions[ni][nj] is not EMPTY:
                            break
    return moves

def possible_epc_moves(state):
    epcs = state["epcs"]
    pions = state["pions"]
    moves = []

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if epcs[i][j] > 0 and pions[i][j] is EMPTY:
                for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE:
                        if pions[ni][nj] is EMPTY and epcs[ni][nj] + 1 <= MAX_EPC_HEIGHT:
                            moves.append(('move_epc', (i, j), (ni, nj)))
    return moves

def move_pion(state, i_from, j_from, i_to, j_to):
    """
    Effectue le déplacement d'un pion du joueur de (i_from, j_from) à (i_to, j_to).
    Retourne le nouvel état après le déplacement.
    """
    new_state = {
        "epcs": [row[:] for row in state["epcs"]],
        "pions": [row[:] for row in state["pions"]],
        "player": state["player"]
    }
    player = state["player"]
    new_state["pions"][i_from][j_from] = EMPTY
    new_state["pions"][i_to][j_to] = player
    return new_state

def attak_pion(state, i_from, j_from, i_to, j_to, is_ai=False):
    """
    Gère la capture d'un pion adverse et son placement sur une case vide.
    Si is_ai est False, demande à l'utilisateur où placer le pion capturé.
    Si is_ai est True, place le pion capturé aléatoirement sur une case vide.
    Retourne le nouvel état après la capture et le placement.
    """
    new_state = move_pion(state, i_from, j_from, i_to, j_to)
    captured = state["pions"][i_to][j_to]
    empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if new_state["pions"][i][j] is EMPTY]
    if not empty_positions:
        return new_state  # No empty position, just return
    if is_ai:
        pos = random.choice(empty_positions)
        new_state["pions"][pos[0]][pos[1]] = captured
    else:
        print_board(new_state)
        while True:
            try:
                print(f"Où placer le pion capturé ({captured}) ? Entrez i j : ", end="")
                move = input().strip().split()
                if len(move) != 2:
                    print("⛔ Format invalide. Essayez encore.")
                    continue
                i, j = map(int, move)
                if (i, j) in empty_positions:
                    new_state["pions"][i][j] = captured
                    break
                else:
                    print("⛔ Position non vide ou hors du plateau. Essayez encore.")
            except Exception:
                print("⛔ Entrée invalide. Essayez encore.")
    return new_state

def move_epc(state, i_from, j_from, i_to, j_to):
    """
    Effectue le déplacement d'un EPC d'une case à une autre.
    Retourne le nouvel état après le déplacement.
    """
    new_state = {
        "epcs": [row[:] for row in state["epcs"]],
        "pions": [row[:] for row in state["pions"]],
        "player": state["player"]
    }
    new_state["epcs"][i_from][j_from] -= 1
    new_state["epcs"][i_to][j_to] += 1
    return new_state

def result(state, pawn_action, epc_action, player, is_ai=False):
    """
    Execute both phases of a turn: pawn move followed by EPC move.
    """
    # Phase 1: Pawn move
    kind, src, dst = pawn_action
    new_state = {
        "epcs": [row[:] for row in state["epcs"]],
        "pions": [row[:] for row in state["pions"]],
        "player": state["player"]
    }

    if kind == "move_pion":
        i_from, j_from = src
        i_to, j_to = dst
        if state["pions"][i_to][j_to] in (WHITE, BLACK):
            # Attack
            new_state = attak_pion(state, i_from, j_from, i_to, j_to, is_ai=is_ai)
        else:
            new_state = move_pion(state, i_from, j_from, i_to, j_to)
    
    # Phase 2: EPC move
    kind, src, dst = epc_action
    if kind == "move_epc":
        i_from, j_from = src
        i_to, j_to = dst
        new_state = move_epc(new_state, i_from, j_from, i_to, j_to)

    # Update player turn
    new_state["player"] = BLACK if player == WHITE else WHITE
    return new_state

############################################################################
def minimax(state, player, depth=2, action_list=None, is_ai=False, pawn_move=None):
    if action_list is None:
        action_list = possible_pion_moves(state)  # Default to pawn moves
    if player == WHITE:
        best_value = -math.inf
        best_action = None
        alpha, beta = -math.inf, math.inf
        for action in action_list:
            # For pawn moves, use dummy EPC. For EPC moves, use the actual pawn move.
            if action[0] == "move_pion":
                dummy_epc = ("move_epc", (0, 0), (0, 0))
                value = min_value(result(state, action, dummy_epc, player, is_ai=is_ai), alpha, beta, depth-1, action_list=None, is_ai=not is_ai)
            else:  # EPC move
                value = min_value(result(state, pawn_move, action, player, is_ai=is_ai), alpha, beta, depth-1, action_list=None, is_ai=not is_ai)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)
        return best_action
    else:
        best_value = math.inf
        best_action = None
        alpha, beta = -math.inf, math.inf
        for action in action_list:
            # For pawn moves, use dummy EPC. For EPC moves, use the actual pawn move.
            if action[0] == "move_pion":
                dummy_epc = ("move_epc", (0, 0), (0, 0))
                value = max_value(result(state, action, dummy_epc, player, is_ai=is_ai), alpha, beta, depth-1, action_list=None, is_ai=not is_ai)
            else:  # EPC move
                value = max_value(result(state, pawn_move, action, player, is_ai=is_ai), alpha, beta, depth-1, action_list=None, is_ai=not is_ai)
            if value < best_value:
                best_value = value
                best_action = action
            beta = min(beta, best_value)
        return best_action

def max_value(state, alpha, beta, depth, action_list=None, is_ai=False, pawn_move=None):
    if is_terminal(state) or depth == 0:
        return utility(state)
    v = -math.inf
    if action_list is None:
        action_list = possible_pion_moves(state)  # Default to pawn moves
    for action in action_list:
        # For pawn moves, use dummy EPC. For EPC moves, use the actual pawn move.
        if action[0] == "move_pion":
            dummy_epc = ("move_epc", (0, 0), (0, 0))
            v = max(v, min_value(result(state, action, dummy_epc, WHITE, is_ai=is_ai), alpha, beta, depth-1, action_list=None, is_ai=not is_ai))
        else:  # EPC move
            v = max(v, min_value(result(state, pawn_move, action, WHITE, is_ai=is_ai), alpha, beta, depth-1, action_list=None, is_ai=not is_ai))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(state, alpha, beta, depth, action_list=None, is_ai=False, pawn_move=None):
    if is_terminal(state) or depth == 0:
        return utility(state)
    v = math.inf
    if action_list is None:
        action_list = possible_pion_moves(state)  # Default to pawn moves
    for action in action_list:
        # For pawn moves, use dummy EPC. For EPC moves, use the actual pawn move.
        if action[0] == "move_pion":
            dummy_epc = ("move_epc", (0, 0), (0, 0))
            v = min(v, max_value(result(state, action, dummy_epc, BLACK, is_ai=is_ai), alpha, beta, depth-1, action_list=None, is_ai=not is_ai))
        else:  # EPC move
            v = min(v, max_value(result(state, pawn_move, action, BLACK, is_ai=is_ai), alpha, beta, depth-1, action_list=None, is_ai=not is_ai))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def print_board(state):
    epcs = state["epcs"]
    pions = state["pions"]
    print("   " + "  ".join(str(j) for j in range(BOARD_SIZE)))
    for i in range(BOARD_SIZE):
        row = []
        for j in range(BOARD_SIZE):
            cell = "_"
            if pions[i][j] == WHITE:
                cell = f"W{epcs[i][j]}"
            elif pions[i][j] == BLACK:
                cell = f"B{epcs[i][j]}"
            else:
                cell = f".{epcs[i][j]}"
            row.append(cell)
        print(f"{i} " + " ".join(row))
    print()

def get_player_move(state):
    pions = state["pions"]
    epcs = state["epcs"]
    player = state["player"]
    # Phase 1: Pawn move
    while True:
        try:
            print("Entrez le mouvement de pion (i_from j_from i_to j_to): ", end="")
            move = input().strip().split()
            if len(move) != 4:
                print("⛔ Format invalide. Essayez encore.")
                continue
            i_from, j_from, i_to, j_to = map(int, move)
            action = ("move_pion", (i_from, j_from), (i_to, j_to))
            if action in possible_pion_moves(state):
                break
            else:
                print("⛔ Mouvement de pion invalide. Essayez encore.")
        except Exception:
            print("⛔ Entrée invalide. Essayez encore.")
    # Phase 2: EPC move
    while True:
        try:
            print("Entrez le mouvement d'EPC (i_from j_from i_to j_to): ", end="")
            move = input().strip().split()
            if len(move) != 4:
                print("⛔ Format invalide. Essayez encore.")
                continue
            i_from, j_from, i_to, j_to = map(int, move)
            action_epc = ("move_epc", (i_from, j_from), (i_to, j_to))
            # Create temporary state after pawn move to validate EPC move
            temp_state = result(state, action, ("move_epc", (0, 0), (0, 0)), player, is_ai=False)  # dummy EPC move
            if action_epc in possible_epc_moves(temp_state):
                break
            else:
                print("⛔ Mouvement d'EPC invalide. Essayez encore.")
        except Exception:
            print("⛔ Entrée invalide. Essayez encore.")
    return action, action_epc

def choose_mode():
    """Demande à l'utilisateur qui joue en premier (White)."""
    while True:
        choice = input("Qui joue White ?\n1 - Vous\n2 - L'IA\nVotre choix : ")
        if choice in ['1', '2']:
            return choice == '1'  # True si utilisateur joue X, False si IA joue X
        print("⛔ Entrée invalide. Entrez 1 ou 2.")

# --- EXÉCUTION DU JEU ---
print("🎮 Bienvenue au Wall Street avec Minimax & Alpha-Bêta !")
user_is_white = choose_mode()
board = initial_state()
player = WHITE

AI_DEPTH = 2  # You can increase for stronger AI, but it will be slower

while not is_terminal(board):
    print_board(board)
    if player == WHITE:
        if user_is_white:
            move, move_epc_action = get_player_move(board)
            board = result(board, move, move_epc_action, WHITE, is_ai=False)
        else:
            print("IA (WHITE) joue...")
            # Calculate pawn move
            move = minimax(board, WHITE, depth=AI_DEPTH, action_list=possible_pion_moves(board), is_ai=True)
            print(f"IA (WHITE) déplace le pion : {move}")
            # Calculate EPC move based on state after pawn move, passing the actual pawn move
            temp_state = result(board, move, ("move_epc", (0, 0), (0, 0)), WHITE, is_ai=True)  # dummy EPC move
            move_epc_action = minimax(temp_state, WHITE, depth=AI_DEPTH, action_list=possible_epc_moves(temp_state), is_ai=True, pawn_move=move)
            print(f"IA (WHITE) déplace l'EPC : {move_epc_action}")
            # Execute both phases
            board = result(board, move, move_epc_action, WHITE, is_ai=True)
    else:
        if user_is_white:
            print("IA (BLACK) joue...")
            # Calculate pawn move
            move = minimax(board, BLACK, depth=AI_DEPTH, action_list=possible_pion_moves(board), is_ai=True)
            print(f"IA (BLACK) déplace le pion : {move}")
            # Calculate EPC move based on state after pawn move, passing the actual pawn move
            temp_state = result(board, move, ("move_epc", (0, 0), (0, 0)), BLACK, is_ai=True)  # dummy EPC move
            move_epc_action = minimax(temp_state, BLACK, depth=AI_DEPTH, action_list=possible_epc_moves(temp_state), is_ai=True, pawn_move=move)
            print(f"IA (BLACK) déplace l'EPC : {move_epc_action}")
            # Execute both phases
            board = result(board, move, move_epc_action, BLACK, is_ai=True)
        else:
            move, move_epc_action = get_player_move(board)
            board = result(board, move, move_epc_action, BLACK, is_ai=False)
    player = WHITE if player == BLACK else BLACK

print_board(board)
if winner(board):
    print(f"🎉 Le joueur {winner(board)} a gagné !")
else:
    print("🤝 Match nul !")