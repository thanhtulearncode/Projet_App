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
    return game.board

@app.get("/valid_moves/{row}/{col}")
def get_valid_moves(row: int, col: int):
    try:
        return game.get_valid_moves(row, col)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/move")
async def make_move(data: dict):
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
def reset_game():
    global game
    game = GameEngine()
    return {"status": "Game reset"}