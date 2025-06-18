#!/usr/bin/env python3
"""
AI vs AI Testing Script
This script allows two AIs to play against each other quickly for testing purposes.
"""

import time
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from game_engine import GameEngine
from ia import MinMaxAI, RandomAI

class AIVsAITester:
    def __init__(self, white_ai_type='random', black_ai_type='minmax', max_turns=100):
        """
        Initialize the AI vs AI tester
        
        Args:
            white_ai_type: 'random' or 'minmax'
            black_ai_type: 'random' or 'minmax'
            max_turns: Maximum number of turns to prevent infinite games
        """
        self.game = GameEngine()
        self.max_turns = max_turns
        self.turn_count = 0
        
        # Initialize AIs
        if white_ai_type == 'random':
            self.white_ai = RandomAI('white')
        elif white_ai_type == 'minmax':
            self.white_ai = MinMaxAI('white', depth=2)
        else:
            raise ValueError(f"Unknown AI type: {white_ai_type}")
            
        if black_ai_type == 'random':
            self.black_ai = RandomAI('black')
        elif black_ai_type == 'minmax':
            self.black_ai = MinMaxAI('black', depth=2)
        else:
            raise ValueError(f"Unknown AI type: {black_ai_type}")
    
    def print_board(self):
        """Print the current board state"""
        print("\n" + "="*50)
        print(f"Turn {self.turn_count} - Current Player: {self.game.current_player}")
        print("="*50)
        
        # Print board with coordinates
        print("  0 1 2 3 4 5 6 7")
        for row in range(8):
            line = f"{row} "
            for col in range(8):
                if not self.game.board[row][col]:
                    line += ". "
                else:
                    top_piece = self.game.board[row][col][-1]
                    if hasattr(top_piece, 'name'):
                        if top_piece.name == 'Pawn':
                            line += f"{top_piece.color[0].upper()} "
                        elif top_piece.name == 'Square':
                            line += f"S{len(self.game.board[row][col])} "
                        else:
                            line += "? "
                    else:
                        line += "? "
            print(line)
        print()
    
    def make_ai_move(self, ai):
        """Make a move for the given AI"""
        try:
            move = ai.make_decision(self.game)
            if not move:
                print(f"[ERROR] {ai.color} AI returned no move")
                return False
            
            print(f"[AI] {ai.color} AI move: {move}")
            
            # Execute the move
            for action_type, start_pos, end_pos in move:
                if action_type == 'move_pion':
                    # First try attack move
                    success, captured, captured_valid_dest = self.game.attack_pion(
                        start_pos[0], start_pos[1], end_pos[0], end_pos[1], None
                    )
                    
                    if success and captured and captured_valid_dest:
                        # Choose a destination that won't interfere with subsequent stack moves
                        # Check if there are any stack moves in the move list
                        stack_moves = [m for m in move if m[0] == 'stack_pieces']
                        
                        # Find a safe destination for the captured pawn
                        safe_dest = None
                        for dest in captured_valid_dest:
                            # Check if this destination conflicts with any stack move
                            conflicts = False
                            for stack_move in stack_moves:
                                if dest == stack_move[1] or dest == stack_move[2]:
                                    conflicts = True
                                    break
                            if not conflicts:
                                safe_dest = dest
                                break
                        
                        # If no safe destination found, use the first available
                        if not safe_dest and captured_valid_dest:
                            safe_dest = captured_valid_dest[0]
                        
                        if safe_dest:
                            success, captured, _ = self.game.attack_pion(
                                start_pos[0], start_pos[1], end_pos[0], end_pos[1], safe_dest
                            )
                            print(f"[AI] {ai.color} captured pawn moved to {safe_dest}")
                        else:
                            print(f"[AI] {ai.color} attack without repositioning")
                    elif success:
                        print(f"[AI] {ai.color} attack without repositioning")
                    else:
                        # Try regular move if attack fails
                        success, captured = self.game.move_pion(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
                        if not success:
                            print(f"[ERROR] Failed to execute pawn move: {action_type}, {start_pos}, {end_pos}")
                            return False
                        
                elif action_type == 'stack_pieces':
                    success = self.game.stack_pieces(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
                    if not success:
                        print(f"[ERROR] Failed to execute stack move: {action_type}, {start_pos}, {end_pos}")
                        return False
                        
            return True
            
        except Exception as e:
            print(f"[ERROR] Exception during {ai.color} AI move: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_game(self, delay=0.1):
        """
        Run the AI vs AI game
        
        Args:
            delay: Delay between moves in seconds (0 for no delay)
        """
        print(f"Starting AI vs AI game: {self.white_ai.__class__.__name__} vs {self.black_ai.__class__.__name__}")
        print(f"Max turns: {self.max_turns}")
        print(f"Delay between moves: {delay}s")
        
        while self.turn_count < self.max_turns:
            self.turn_count += 1
            
            # Print current board state
            self.print_board()
            
            # Check if game is over
            if self.game.check_game_over():
                print(f"\n[GAME OVER] Game ended after {self.turn_count} turns")
                winner = self.game.get_winner()
                print(f"[WINNER] {winner}")
                break
            
            # Determine which AI to use
            current_ai = self.white_ai if self.game.current_player == 'white' else self.black_ai
            
            # Make AI move
            print(f"\n[AI] {current_ai.color} AI is thinking...")
            start_time = time.time()
            
            success = self.make_ai_move(current_ai)
            
            end_time = time.time()
            print(f"[AI] {current_ai.color} AI took {end_time - start_time:.2f}s")
            
            if not success:
                print(f"[ERROR] Failed to make move for {current_ai.color} AI")
                break
            
            # Add delay if specified
            if delay > 0:
                time.sleep(delay)
        
        if self.turn_count >= self.max_turns:
            print(f"\n[GAME OVER] Maximum turns ({self.max_turns}) reached")
            winner = self.game.get_winner()
            print(f"[WINNER] {winner}")
        
        # Final board state
        self.print_board()
        
        # Print final statistics
        self.print_statistics()
    
    def print_statistics(self):
        """Print game statistics"""
        print("\n" + "="*50)
        print("GAME STATISTICS")
        print("="*50)
        print(f"Total turns: {self.turn_count}")
        print(f"Final player: {self.game.current_player}")
        print(f"Game over: {self.game.game_over}")
        
        # Count pieces on board
        white_pawns = 0
        black_pawns = 0
        squares = 0
        
        for row in range(8):
            for col in range(8):
                for piece in self.game.board[row][col]:
                    if hasattr(piece, 'name'):
                        if piece.name == 'Pawn':
                            if piece.color == 'white':
                                white_pawns += 1
                            elif piece.color == 'black':
                                black_pawns += 1
                        elif piece.name == 'Square':
                            squares += 1
        
        print(f"White pawns: {white_pawns}")
        print(f"Black pawns: {black_pawns}")
        print(f"Total squares: {squares}")


def main():
    """Main function to run AI vs AI testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI vs AI Testing Script')
    parser.add_argument('--white', choices=['random', 'minmax'], default='random',
                       help='AI type for white player (default: random)')
    parser.add_argument('--black', choices=['random', 'minmax'], default='minmax',
                       help='AI type for black player (default: minmax)')
    parser.add_argument('--max-turns', type=int, default=100,
                       help='Maximum number of turns (default: 100)')
    parser.add_argument('--delay', type=float, default=0.1,
                       help='Delay between moves in seconds (default: 0.1)')
    parser.add_argument('--no-delay', action='store_true',
                       help='Run without delay between moves')
    
    args = parser.parse_args()
    
    # Set delay to 0 if --no-delay is specified
    delay = 0 if args.no_delay else args.delay
    
    # Create and run the tester
    tester = AIVsAITester(
        white_ai_type=args.white,
        black_ai_type=args.black,
        max_turns=args.max_turns
    )
    
    try:
        tester.run_game(delay=delay)
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Game stopped by user")
        tester.print_statistics()


if __name__ == "__main__":
    main() 