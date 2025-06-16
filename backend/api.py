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