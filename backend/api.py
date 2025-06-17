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