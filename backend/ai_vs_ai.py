#!/usr/bin/env python3
"""
AI vs AI Testing Script
This script allows two AIs to play against each other quickly for testing purposes.
Updated to use the new AI difficulty levels with execution time tracking.
"""

import time
import sys
import os
from statistics import mean, median

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from game_engine import GameEngine
from ia import AIFactory, EasyAI, MediumAI, HardAI

class AIVsAITester:
    def __init__(self, white_ai_difficulty='easy', black_ai_difficulty='medium', max_turns=100):
        """
        Initialize the AI vs AI tester
        
        Args:
            white_ai_difficulty: 'easy', 'medium', or 'hard'
            black_ai_difficulty: 'easy', 'medium', or 'hard'
            max_turns: Maximum number of turns to prevent infinite games
        """
        self.game = GameEngine()
        self.max_turns = max_turns
        self.turn_count = 0
        
        # Initialize AIs using the factory
        self.white_ai = AIFactory.create_ai(white_ai_difficulty, 'white')
        self.black_ai = AIFactory.create_ai(black_ai_difficulty, 'black')
        
        # Execution time tracking
        self.white_move_times = []
        self.black_move_times = []
        self.total_game_time = 0
        
        print(f"[AI vs AI] Initialized: {self.white_ai.difficulty} AI (White) vs {self.black_ai.difficulty} AI (Black)")
    
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
        """Make a move for the given AI and track execution time"""
        try:
            start_time = time.time()
            move = ai.make_decision(self.game)
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            # Store execution time
            if ai.color == 'white':
                self.white_move_times.append(execution_time)
            else:
                self.black_move_times.append(execution_time)
            
            if not move:
                print(f"[ERROR] {ai.color} AI returned no move")
                return False
            
            print(f"[AI] {ai.color} AI ({ai.difficulty}) move: {move}")
            print(f"[TIME] {ai.color} AI took {execution_time:.3f}s")
            
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
        print(f"Starting AI vs AI game: {self.white_ai.difficulty} AI vs {self.black_ai.difficulty} AI")
        print(f"Max turns: {self.max_turns}")
        print(f"Delay between moves: {delay}s")
        
        game_start_time = time.time()
        
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
            print(f"\n[AI] {current_ai.color} AI ({current_ai.difficulty}) is thinking...")
            
            success = self.make_ai_move(current_ai)
            
            if not success:
                print(f"[ERROR] Failed to make move for {current_ai.color} AI")
                break
            
            # Add delay if specified
            if delay > 0:
                time.sleep(delay)
        
        game_end_time = time.time()
        self.total_game_time = game_end_time - game_start_time
        
        if self.turn_count >= self.max_turns:
            print(f"\n[GAME OVER] Maximum turns ({self.max_turns}) reached")
            winner = self.game.get_winner()
            print(f"[WINNER] {winner}")
        
        # Final board state
        self.print_board()
        
        # Print final statistics
        self.print_statistics()
    
    def print_statistics(self):
        """Print comprehensive game statistics including execution times"""
        print("\n" + "="*60)
        print("GAME STATISTICS")
        print("="*60)
        print(f"Total turns: {self.turn_count}")
        print(f"Final player: {self.game.current_player}")
        print(f"Game over: {self.game.game_over}")
        print(f"Total game time: {self.total_game_time:.3f}s")
        
        # AI Performance Statistics
        print(f"\n{self.white_ai.difficulty} AI (White) Performance:")
        if self.white_move_times:
            print(f"  Total moves: {len(self.white_move_times)}")
            print(f"  Average move time: {mean(self.white_move_times):.3f}s")
            print(f"  Median move time: {median(self.white_move_times):.3f}s")
            print(f"  Fastest move: {min(self.white_move_times):.3f}s")
            print(f"  Slowest move: {max(self.white_move_times):.3f}s")
            print(f"  Total thinking time: {sum(self.white_move_times):.3f}s")
        else:
            print("  No moves recorded")
        
        print(f"\n{self.black_ai.difficulty} AI (Black) Performance:")
        if self.black_move_times:
            print(f"  Total moves: {len(self.black_move_times)}")
            print(f"  Average move time: {mean(self.black_move_times):.3f}s")
            print(f"  Median move time: {median(self.black_move_times):.3f}s")
            print(f"  Fastest move: {min(self.black_move_times):.3f}s")
            print(f"  Slowest move: {max(self.black_move_times):.3f}s")
            print(f"  Total thinking time: {sum(self.black_move_times):.3f}s")
        else:
            print("  No moves recorded")
        
        # Overall AI comparison
        if self.white_move_times and self.black_move_times:
            white_avg = mean(self.white_move_times)
            black_avg = mean(self.black_move_times)
            print(f"\nAI Performance Comparison:")
            print(f"  {self.white_ai.difficulty} AI average: {white_avg:.3f}s")
            print(f"  {self.black_ai.difficulty} AI average: {black_avg:.3f}s")
            if white_avg < black_avg:
                print(f"  {self.white_ai.difficulty} AI is {black_avg/white_avg:.1f}x faster")
            else:
                print(f"  {self.black_ai.difficulty} AI is {white_avg/black_avg:.1f}x faster")
        
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
        
        print(f"\nFinal Board State:")
        print(f"  White pawns: {white_pawns}")
        print(f"  Black pawns: {black_pawns}")
        print(f"  Total squares: {squares}")


def main():
    """Main function to run AI vs AI testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI vs AI Testing Script with Difficulty Levels')
    parser.add_argument('--white', choices=['easy', 'medium', 'hard'], default='easy',
                       help='AI difficulty for white player (default: easy)')
    parser.add_argument('--black', choices=['easy', 'medium', 'hard'], default='medium',
                       help='AI difficulty for black player (default: medium)')
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
        white_ai_difficulty=args.white,
        black_ai_difficulty=args.black,
        max_turns=args.max_turns
    )
    
    try:
        tester.run_game(delay=delay)
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Game stopped by user")
        tester.print_statistics()


if __name__ == "__main__":
    main() 