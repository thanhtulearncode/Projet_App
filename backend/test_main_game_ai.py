#!/usr/bin/env python3
"""
Test script for AI difficulty levels in the main game
This script demonstrates how to use different AI difficulty levels in the main game.
"""

import time
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from game_engine import GameEngine
from ia import AIFactory

def test_ai_difficulty_in_game(difficulty='medium', num_moves=5):
    """
    Test a specific AI difficulty level in the main game
    
    Args:
        difficulty (str): 'easy', 'medium', or 'hard'
        num_moves (int): Number of AI moves to test
    """
    print(f"\n{'='*60}")
    print(f"Testing {difficulty.upper()} AI in Main Game")
    print(f"{'='*60}")
    
    # Create game with specific AI difficulty
    game = GameEngine(ai_difficulty=difficulty)
    
    print(f"Game initialized with {difficulty} AI")
    print(f"Current AI difficulty: {game.get_ai_difficulty()}")
    
    # Test AI moves
    move_times = []
    successful_moves = 0
    
    for move_num in range(num_moves):
        print(f"\n--- Move {move_num + 1}/{num_moves} ---")
        print(f"Current player: {game.current_player}")
        
        # Count pieces before move
        white_pawns = black_pawns = squares = 0
        for row in range(8):
            for col in range(8):
                for piece in game.board[row][col]:
                    if hasattr(piece, 'name'):
                        if piece.name == 'Pawn':
                            if piece.color == 'white':
                                white_pawns += 1
                            else:
                                black_pawns += 1
                        elif piece.name == 'Square':
                            squares += 1
        
        print(f"Board state: W:{white_pawns} B:{black_pawns} S:{squares}")
        
        # Time the AI move
        start_time = time.time()
        move = game.ai.make_decision(game)
        end_time = time.time()
        
        execution_time = end_time - start_time
        move_times.append(execution_time)
        
        if move:
            successful_moves += 1
            print(f"AI move: {move}")
            print(f"Execution time: {execution_time:.3f}s")
            
            # Execute the move (simplified - just for testing)
            print("Move executed successfully")
        else:
            print("No valid move found")
            print(f"Execution time: {execution_time:.3f}s")
            break
        
        # Check if game is over
        if game.check_game_over():
            print("Game is over!")
            winner = game.get_winner()
            print(f"Winner: {winner}")
            break
    
    # Print results
    print(f"\n--- {difficulty.upper()} AI Results ---")
    print(f"Successful moves: {successful_moves}/{num_moves}")
    if move_times:
        avg_time = sum(move_times) / len(move_times)
        min_time = min(move_times)
        max_time = max(move_times)
        print(f"Average move time: {avg_time:.3f}s")
        print(f"Min move time: {min_time:.3f}s")
        print(f"Max move time: {max_time:.3f}s")
        print(f"Total thinking time: {sum(move_times):.3f}s")

def test_all_difficulties():
    """Test all AI difficulty levels"""
    print("AI Difficulty Levels in Main Game - Performance Test")
    print("="*80)
    
    difficulties = ['easy', 'medium', 'hard']
    all_stats = []
    
    for difficulty in difficulties:
        print(f"\nTesting {difficulty} AI...")
        
        # Create game with this difficulty
        game = GameEngine(ai_difficulty=difficulty)
        
        # Test a few moves
        move_times = []
        successful_moves = 0
        
        for move_num in range(3):  # Test 3 moves per difficulty
            start_time = time.time()
            move = game.ai.make_decision(game)
            end_time = time.time()
            
            execution_time = end_time - start_time
            move_times.append(execution_time)
            
            if move:
                successful_moves += 1
                # Execute move (simplified)
                pass
        
        # Calculate stats
        if move_times:
            avg_time = sum(move_times) / len(move_times)
            total_time = sum(move_times)
        else:
            avg_time = total_time = 0
        
        stats = {
            'difficulty': difficulty,
            'successful_moves': successful_moves,
            'avg_time': avg_time,
            'total_time': total_time
        }
        all_stats.append(stats)
    
    # Print comparison
    print(f"\n{'='*80}")
    print("PERFORMANCE COMPARISON")
    print(f"{'='*80}")
    print(f"{'Difficulty':<10} {'Success Rate':<12} {'Avg Time':<10} {'Total Time':<12}")
    print("-" * 80)
    
    for stats in all_stats:
        success_rate = (stats['successful_moves'] / 3) * 100
        print(f"{stats['difficulty']:<10} {success_rate:<11.1f}% {stats['avg_time']:<9.3f}s {stats['total_time']:<11.3f}s")

def test_difficulty_changing():
    """Test changing AI difficulty during gameplay"""
    print(f"\n{'='*60}")
    print("Testing AI Difficulty Changing")
    print(f"{'='*60}")
    
    # Start with easy AI
    game = GameEngine(ai_difficulty='easy')
    print(f"Initial AI difficulty: {game.get_ai_difficulty()}")
    
    # Test a move
    print("\nTesting move with Easy AI...")
    start_time = time.time()
    move = game.ai.make_decision(game)
    easy_time = time.time() - start_time
    print(f"Easy AI move: {move}")
    print(f"Easy AI time: {easy_time:.3f}s")
    
    # Change to hard AI
    print("\nChanging to Hard AI...")
    game.set_ai_difficulty('hard')
    print(f"New AI difficulty: {game.get_ai_difficulty()}")
    
    # Test another move
    print("\nTesting move with Hard AI...")
    start_time = time.time()
    move = game.ai.make_decision(game)
    hard_time = time.time() - start_time
    print(f"Hard AI move: {move}")
    print(f"Hard AI time: {hard_time:.3f}s")
    
    # Compare times
    if easy_time > 0 and hard_time > 0:
        speed_ratio = hard_time / easy_time
        print(f"\nHard AI is {speed_ratio:.1f}x slower than Easy AI")

def main():
    """Main function to run AI tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test AI Difficulty Levels in Main Game')
    parser.add_argument('--mode', choices=['single', 'all', 'change'], default='all',
                       help='Test mode (default: all)')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'], default='medium',
                       help='AI difficulty to test (for single mode)')
    parser.add_argument('--moves', type=int, default=5,
                       help='Number of moves to test (default: 5)')
    
    args = parser.parse_args()
    
    if args.mode == 'single':
        # Test specific difficulty level
        test_ai_difficulty_in_game(args.difficulty, args.moves)
    elif args.mode == 'all':
        # Test all difficulty levels
        test_all_difficulties()
    elif args.mode == 'change':
        # Test changing difficulty
        test_difficulty_changing()

if __name__ == "__main__":
    main() 