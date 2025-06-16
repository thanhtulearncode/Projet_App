from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from game_engine import GameEngine

app = FastAPI()
game = GameEngine()

# Configuration CORS pour le développement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/board")
<<<<<<< HEAD
def get_board():
    return game.get_state()
=======
def get_board(colorPair: str = 'black-white'):
    global game
    # Créer une nouvelle instance si les couleurs ont changé
    if game.color_pair != colorPair:
        game = GameEngine(color_pair=colorPair)
    return game.board
>>>>>>> fafe2110 (Ajout de la fonctionnalité de choix de couleurs pour les pions)

@app.get("/valid_moves/{row}/{col}")
def get_valid_moves(row: int, col: int, colorPair: str = 'black-white', mode: str = 'local', difficulty: str = 'medium'):
    global game
    # Vérifier si les couleurs ont changé
    if game.color_pair != colorPair:
        game = GameEngine(color_pair=colorPair)
    try:
        return game.get_valid_moves(row, col)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/move")
async def make_move(data: dict, colorPair: str = 'black-white'):
    global game
    # Vérifier si les couleurs ont changé
    if game.color_pair != colorPair:
        game = GameEngine(color_pair=colorPair)
    try:
        start_row = data['start_row']
        start_col = data['start_col']
        end_row = data['end_row']
        end_col = data['end_col']
        
        success, captured = game.move_piece(start_row, start_col, end_row, end_col)
        return {
            "success": success,
            "captured": captured,
            "current_player": game.current_player
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reset")
def reset_game(colorPair: str = 'black-white'):
    global game
<<<<<<< HEAD
    game = GameEngine()
    return {"status": "Game reset"}

@app.post("/turn")
def play_turn(data: dict):
    try:
        # 1. Déplacement du pion rond
        pion = data.get('pion')  # {"start_row": int, "start_col": int, "end_row": int, "end_col": int}
        stack = data.get('stack')  # {"src_row": int, "src_col": int, "dst_row": int, "dst_col": int}
        pion_result = None
        stack_result = None
        if pion:
            pion_result = game.move_pion(
                pion['start_row'], pion['start_col'], pion['end_row'], pion['end_col']
            )
        # 2. Empilage
        if stack:
            stack_result = game.stack_pieces(
                stack['src_row'], stack['src_col'], stack['dst_row'], stack['dst_col']
            )
        # 3. Vérification fin de partie
        game_over = game.check_game_over()
        winner = game.get_winner() if game_over else None
        return {
            "pion_result": pion_result,
            "stack_result": stack_result,
            "game_over": game_over,
            "winner": winner,
            "state": game.get_state(),
            "current_player": game.current_player
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
=======
    game = GameEngine(color_pair=colorPair)
    return {"status": "Game reset", "colorPair": colorPair}

def get_valid_moves(self, row, col):
    """Obtenir tous les mouvements valides pour une pièce à la position (row, col)"""
    valid_moves = []
    
    # Vérifier si la case contient un pion et s'il appartient au joueur actuel
    stack = self.board[row][col]
    has_piece = False
    piece_color = None
    
    for piece in stack:
        if piece['type'] == 'round':
            has_piece = True
            piece_color = piece['color']
            break
    
    if not has_piece or piece_color != self.current_player:
        return {"validMoves": []}
    
    # Calculer la hauteur de l'empilement des pièces carrées
    stack_height = sum(1 for piece in stack if piece['type'] == 'square')
    
    # Définir les directions (haut, droite, bas, gauche)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    for dr, dc in directions:
        for distance in range(1, stack_height + 1):
            new_row, new_col = row + dr * distance, col + dc * distance
            
            # Vérifier si la nouvelle position est dans les limites du plateau
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_stack = self.board[new_row][new_col]
                
                # Vérifier si la case cible a une pièce carrée
                has_square = False
                for piece in target_stack:
                    if piece['type'] == 'square':
                        has_square = True
                        break
                
                if has_square:
                    # Vérifier si la case cible contient un pion
                    target_has_piece = False
                    target_piece_color = None
                    
                    for piece in target_stack:
                        if piece['type'] == 'round':
                            target_has_piece = True
                            target_piece_color = piece['color']
                            break
                    
                    # Si la case est vide, c'est un mouvement valide
                    if not target_has_piece:
                        valid_moves.append((new_row, new_col))
                    # Si la case contient un pion adverse et qu'on a parcouru la distance maximale, c'est un mouvement valide
                    elif target_piece_color != self.current_player and distance == stack_height:
                        valid_moves.append((new_row, new_col))
                    else:
                        # Arrêter la recherche dans cette direction si on rencontre un obstacle
                        break
                else:
                    # Ignorer les cases sans pièce carrée et continuer la recherche dans cette direction
                    continue
            else:
                # Arrêter la recherche si on sort des limites du plateau
                break
    
    return {"validMoves": valid_moves}
>>>>>>> fafe2110 (Ajout de la fonctionnalité de choix de couleurs pour les pions)
