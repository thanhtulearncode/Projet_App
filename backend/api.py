from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from game_engine import GameEngine
from AI import GameAI
from ia import AIFactory
import random
import os
import time

app = FastAPI()
game = GameEngine()

ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://wall-street-game.vercel.app").split(",")

# Configuration CORS pour le développement
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/board")
def get_board(colorPair: str = "black-white"):
    global game
    if game.color_pair != colorPair:
        game = GameEngine(color_pair=colorPair)
    return game.get_state()

@app.get("/ai_difficulty")
def get_ai_difficulty():
    """Get the current AI difficulty level"""
    return {"difficulty": game.get_ai_difficulty()}

@app.post("/set_ai_difficulty")
def set_ai_difficulty(data: dict):
    """Set the AI difficulty level"""
    try:
        difficulty = data.get('difficulty', 'medium')
        if difficulty not in ['easy', 'medium', 'hard']:
            raise HTTPException(status_code=400, detail="Invalid difficulty level. Use 'easy', 'medium', or 'hard'")
        
        game.set_ai_difficulty(difficulty)
        return {
            "success": True,
            "difficulty": difficulty,
            "message": f"AI difficulty set to {difficulty}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
def reset_game(request: Request):
    global game
    colorPair = "black-white"
    ai_difficulty = "medium"
    ai_color = None
    try:
        data = request.query_params
        if 'colorPair' in data:
            colorPair = data['colorPair']
        if 'ai_difficulty' in data:
            ai_difficulty = data['ai_difficulty']
            if ai_difficulty not in ['easy', 'medium', 'hard']:
                ai_difficulty = "medium"  # Default to medium if invalid
        if 'ai_color' in data:
            ai_color = data['ai_color']
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid query parameters")
    game = GameEngine(color_pair=colorPair, ai_difficulty=ai_difficulty, ai_color=ai_color)
    return {
        "status": "Game reset",
        "ai_difficulty": ai_difficulty,
        "color_pair": colorPair,
        "ai_color": ai_color
    }

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
def ai_move(data: dict = {}, colorPair: str = "black-white"):
    global game
    # Re-initialize the game if the colorPair is different
    if hasattr(game, 'color_pair') and game.color_pair != colorPair:
        game = GameEngine(color_pair=colorPair)
    try:
        print(f"[AI] {game.ai.difficulty} AI is thinking...")
        try:
            ai_game = game.clone()  # Clone once for AI search
            move = game.ai.make_decision(ai_game)
            print("aaaaa")
            print(game.ai.depth)

            print(f"[AI] Move decision: {move}")
        except Exception as e:
            print("Exception in make_decision:", e)
            import traceback
            traceback.print_exc()
            raise
        print(f"AI move decision: {move}")
        action_types = [action[0] for action in move]
        start_positions = [action[1] for action in move]
        end_positions = [action[2] for action in move]
        move_position = None
        move_destination = None
        epc_posititon = None    
        epc_destination = None
        captured_destination = None
        if not move:
            return {"success": False, "message": "Aucun coup possible"}
        for action_type, start_pos, end_pos in zip(action_types, start_positions, end_positions):
            if action_type == 'move_pion':
                success, captured = game.move_pion(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
                if not success:
                    success, captured, captured_valid_dest = game.attack_pion(
                        start_pos[0], start_pos[1], end_pos[0], end_pos[1], None
                    )
                    if success and captured and captured_valid_dest:
                        # Si le pion est capturé, choisir une destination valide aléatoire
                        random_dest = random.choice(captured_valid_dest)
                        success, captured, _ = game.attack_pion(
                            start_pos[0], start_pos[1], end_pos[0], end_pos[1], random_dest
                        )
                        print(f"[IA] Attaquez et déplacez les pions capturés vers {random_dest}")
                        captured_destination = random_dest
                    elif success:
                        print(f"[IA] Attaque sans repositionnement : {start_pos} -> {end_pos}")
                move_position = start_pos
                move_destination = end_pos
            elif action_type == 'stack_pieces':
                time.sleep(5)
                success = game.stack_pieces(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
                if not success:
                    print(f"Échec du mouvement de pile: {start_pos} -> {end_pos}")
                    return {"success": False, "message": "Échec du coup AI"}
                epc_posititon = start_pos
                epc_destination = end_pos           
            else:
                print(f"Action inconnue: {action_type}")
                print(f"Action: {action_type}, Start: {start_pos}, End: {end_pos}, Success: {success}")
                success = False
            #print(success)
            #print("qqqqqqqqqqqqqqqqqqqqqqqqqq")
            if not success:
                return {"success": False, "message": "Échec du coup AI"}
        #print("tttttttttttttttttttttttttttt")
        return {
            "success": success,
            "current_player": game.current_player,
            "state": game.get_state(),
            "ai_difficulty": game.get_ai_difficulty(),
            "pawnPosition": move_position,
            "pawnDestination": move_destination,
            "EPCPosition": epc_posititon,
            "EPCDestination": epc_destination,
            "capturedDestination": captured_destination
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))