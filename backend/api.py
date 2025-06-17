from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from game_engine import GameEngine
from AI import GameAI

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
def get_board():
    return game.get_state()

@app.get("/valid_moves/{row}/{col}")
def get_valid_moves(row: int, col: int):
    try:
        return game.get_valid_moves(row, col)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/move_pawn")
async def make_move(data: dict):
    try:
        start_row = data['start_row']
        start_col = data['start_col']
        end_row = data['end_row']
        end_col = data['end_col']
        
        success, captured = game.move_pion(start_row, start_col, end_row, end_col)
        return {
            "success": success,
            "captured": captured,
            "current_player": game.current_player
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/reset")
def reset_game():
    global game
    game = GameEngine()
    return {"status": "Game reset"}

@app.post("/move_square")
def move_square(data: dict):
    try:
        src_row = data['src_row']
        src_col = data['src_col']
        dst_row = data['dst_row']
        dst_col = data['dst_col']
        success = game.stack_pieces(src_row, src_col, dst_row, dst_col)
        return {
            "success": success,
            "current_player": game.current_player,
            "state": game.get_state()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/attack_pion")
def attack_pion_api(data: dict):
    try:
        start_row = data['start_row']
        start_col = data['start_col']
        end_row = data['end_row']
        end_col = data['end_col']
        captured_dest = data.get('captured_dest')  # [x, y] ou None
        print("API /attack_pion params:", start_row, start_col, end_row, end_col, captured_dest)
        success, captured, captured_valid_dest = game.attack_pion(start_row, start_col, end_row, end_col, captured_dest)
        return {
            "success": success,
            "captured": bool(captured),
            "captured_valid_dest": captured_valid_dest,
            "current_player": game.current_player,
            "state": game.get_state()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/is_game_over")
def is_game_over():
    # Utilise la méthode check_game_over existante
    if game.check_game_over():
        return {"game_over": True, "winner": game.get_winner()}
    return {"game_over": False, "winner": None}

@app.post("/ai_move")
def ai_move(data: dict = {}):
    cnt = 0
    if cnt > 0:
         return {"success": False, "message": "L'IA a déjà joué ce tour"}
    try:
        # On suppose que l'IA joue la couleur du joueur courant
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")   
        move = game.ai.make_decision(game)
        print(f"AI move decision: {move}")
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        action_types = [action[0] for action in move]
        start_positions = [action[1] for action in move]
        end_positions = [action[2] for action in move]
        if not move:
            return {"success": False, "message": "Aucun coup possible"}
        for action_type, start_pos, end_pos in zip(action_types, start_positions, end_positions):
            if action_type == 'move_pion':
                success, captured = game.move_pion(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
            elif action_type == 'stack_pieces':
                success = game.stack_pieces(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
                cnt += 1            
            else:
                success = False
            print("qqqqqqqqqqqqqqqqqqqqqqqqqq")
            if not success:
                return {"success": False, "message": "Échec du coup AI"}
        print("tttttttttttttttttttttttttttt")
        return {
            "success": success,
            "current_player": game.current_player,
            "state": game.get_state()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))