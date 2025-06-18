#!/usr/bin/env python3
"""
Test script for AI difficulty levels and execution time tracking
This script demonstrates the different AI levels and their performance characteristics.
"""

import time
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from game_engine import GameEngine
from ia import AIFactory, EasyAI, MediumAI, HardAI

def test_ai_performance(ai_difficulty, color, num_tests=5):
    """
    Test the performance of a specific AI difficulty level
    
    Args:
        ai_difficulty (str): 'easy', 'medium', or 'hard'
        color (str): 'white' or 'black'
        num_tests (int): Number of test moves to perform
        
    Returns:
        dict: Performance statistics
    """
    print(f"\n{'='*50}")
    print(f"Testing {ai_difficulty.upper()} AI ({color})")
    print(f"{'='*50}")
    
    # Create AI using factory
    ai = AIFactory.create_ai(ai_difficulty, color)
    
    # Performance tracking
    move_times = []
    successful_moves = 0
    
    for test_num in range(num_tests):
        # Create a fresh game for each test
        game = GameEngine()
        
        print(f"\nTest {test_num + 1}/{num_tests}")
        print(f"Board state: {count_pieces(game)}")
        
        # Time the AI decision
        start_time = time.time()
        move = ai.make_decision(game)
        end_time = time.time()
        
        execution_time = end_time - start_time
        move_times.append(execution_time)
        
        if move:
            successful_moves += 1
            print(f"Move: {move}")
            print(f"Execution time: {execution_time:.3f}s")
        else:
            print("No valid move found")
            print(f"Execution time: {execution_time:.3f}s")
    
    # Calculate statistics
    if move_times:
        avg_time = sum(move_times) / len(move_times)
        min_time = min(move_times)
        max_time = max(move_times)
        total_time = sum(move_times)
    else:
        avg_time = min_time = max_time = total_time = 0
    
    stats = {
        'difficulty': ai_difficulty,
        'color': color,
        'total_tests': num_tests,
        'successful_moves': successful_moves,
        'success_rate': (successful_moves / num_tests) * 100,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'total_time': total_time,
        'move_times': move_times
    }
    
    # Print results
    print(f"\nResults for {ai_difficulty.upper()} AI:")
    print(f"  Successful moves: {successful_moves}/{num_tests} ({stats['success_rate']:.1f}%)")
    print(f"  Average time: {avg_time:.3f}s")
    print(f"  Min time: {min_time:.3f}s")
    print(f"  Max time: {max_time:.3f}s")
    print(f"  Total time: {total_time:.3f}s")
    
    return stats

def count_pieces(game):
    """Count pieces on the board for a quick state summary"""
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
    
    return f"W:{white_pawns} B:{black_pawns} S:{squares}"

def compare_ai_levels():
    """Compare all AI difficulty levels"""
    print("AI Difficulty Level Performance Comparison")
    print("="*60)
    
    difficulties = ['easy', 'medium', 'hard']
    all_stats = []
    
    # Test each difficulty level
    for difficulty in difficulties:
        stats = test_ai_performance(difficulty, 'white', num_tests=3)
        all_stats.append(stats)
    
    # Print comparison table
    print(f"\n{'='*80}")
    print("PERFORMANCE COMPARISON TABLE")
    print(f"{'='*80}")
    print(f"{'Difficulty':<10} {'Success Rate':<12} {'Avg Time':<10} {'Min Time':<10} {'Max Time':<10} {'Total Time':<12}")
    print("-" * 80)
    
    for stats in all_stats:
        print(f"{stats['difficulty']:<10} {stats['success_rate']:<11.1f}% {stats['avg_time']:<9.3f}s {stats['min_time']:<9.3f}s {stats['max_time']:<9.3f}s {stats['total_time']:<11.3f}s")
    
    # Find fastest and most successful
    fastest_ai = min(all_stats, key=lambda x: x['avg_time'])
    most_successful = max(all_stats, key=lambda x: x['success_rate'])
    
    print(f"\nFastest AI: {fastest_ai['difficulty']} (avg: {fastest_ai['avg_time']:.3f}s)")
    print(f"Most Successful: {most_successful['difficulty']} ({most_successful['success_rate']:.1f}% success rate)")

def quick_ai_vs_ai_demo():
    """Quick demonstration of AI vs AI with different difficulty levels"""
    print(f"\n{'='*60}")
    print("QUICK AI vs AI DEMO")
    print(f"{'='*60}")
    
    # Import the AI vs AI tester
    from ai_vs_ai import AIVsAITester
    
    # Test Easy vs Medium
    print("\nDemo 1: Easy AI vs Medium AI (5 turns)")
    tester1 = AIVsAITester('easy', 'medium', max_turns=5)
    tester1.run_game(delay=0.5)
    
    # Test Medium vs Hard
    print("\nDemo 2: Medium AI vs Hard AI (5 turns)")
    tester2 = AIVsAITester('medium', 'hard', max_turns=5)
    tester2.run_game(delay=0.5)

def main():
    """Main function to run AI tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Difficulty Level Testing Script')
    parser.add_argument('--mode', choices=['performance', 'comparison', 'demo'], default='comparison',
                       help='Test mode (default: comparison)')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'], default='medium',
                       help='AI difficulty to test (for performance mode)')
    parser.add_argument('--tests', type=int, default=3,
                       help='Number of tests to run (default: 3)')
    
    args = parser.parse_args()
    
    if args.mode == 'performance':
        # Test specific difficulty level
        test_ai_performance(args.difficulty, 'white', args.tests)
    elif args.mode == 'comparison':
        # Compare all difficulty levels
        compare_ai_levels()
    elif args.mode == 'demo':
        # Quick AI vs AI demo
        quick_ai_vs_ai_demo()

if __name__ == "__main__":
    main() 