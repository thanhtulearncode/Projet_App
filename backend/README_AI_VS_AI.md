# AI vs AI Testing with Difficulty Levels

This document explains how to use the updated AI vs AI testing functionality with the new difficulty levels and execution time tracking.

## Overview

The AI system now supports 3 difficulty levels:

1. **Easy AI** - Random moves with basic validation
2. **Medium AI** - MinMax algorithm with depth=2 (basic strategy)
3. **Hard AI** - MinMax algorithm with depth=4 (advanced strategy)

## Files

- `ai_vs_ai.py` - Main AI vs AI testing script
- `test_ai_levels.py` - AI performance testing and comparison script
- `ia.py` - Contains the AI difficulty level classes and factory

## Usage

### Basic AI vs AI Game

```bash
# Easy vs Medium AI
python ai_vs_ai.py --white easy --black medium

# Medium vs Hard AI
python ai_vs_ai.py --white medium --black hard

# Hard vs Easy AI
python ai_vs_ai.py --white hard --black easy

# No delay between moves (faster execution)
python ai_vs_ai.py --white medium --black hard --no-delay

# Custom number of turns
python ai_vs_ai.py --white easy --black hard --max-turns 50
```

### Command Line Options

- `--white`: AI difficulty for white player (`easy`, `medium`, `hard`)
- `--black`: AI difficulty for black player (`easy`, `medium`, `hard`)
- `--max-turns`: Maximum number of turns (default: 100)
- `--delay`: Delay between moves in seconds (default: 0.1)
- `--no-delay`: Run without delay between moves

### AI Performance Testing

```bash
# Test all difficulty levels
python test_ai_levels.py --mode comparison

# Test specific difficulty level
python test_ai_levels.py --mode performance --difficulty hard --tests 5

# Quick AI vs AI demo
python test_ai_levels.py --mode demo
```

## Output Features

### Execution Time Tracking

The system tracks detailed execution time statistics:

- **Per-move timing**: Each AI move is timed individually
- **Average/Median times**: Statistical analysis of move times
- **Fastest/Slowest moves**: Performance extremes
- **Total thinking time**: Cumulative time spent by each AI
- **Performance comparison**: Relative speed between AIs

### Example Output

```
[AI] white AI (Easy) move: [('move_pion', (1, 0), (2, 1))]
[TIME] white AI took 0.002s

[AI] black AI (Hard) move: [('move_pion', (6, 1), (5, 2)), ('stack_pieces', (5, 2), (4, 3))]
[TIME] black AI took 1.234s

============================================================
GAME STATISTICS
============================================================
Total turns: 15
Total game time: 8.456s

Easy AI (White) Performance:
  Total moves: 7
  Average move time: 0.003s
  Median move time: 0.002s
  Fastest move: 0.001s
  Slowest move: 0.008s
  Total thinking time: 0.021s

Hard AI (Black) Performance:
  Total moves: 8
  Average move time: 1.054s
  Median move time: 0.987s
  Fastest move: 0.234s
  Slowest move: 2.156s
  Total thinking time: 8.432s

AI Performance Comparison:
  Easy AI average: 0.003s
  Hard AI average: 1.054s
  Easy AI is 351.3x faster
```

## AI Difficulty Characteristics

### Easy AI
- **Strategy**: Random moves with validation
- **Speed**: Very fast (< 0.01s per move)
- **Depth**: No lookahead
- **Use case**: Beginners, testing, quick games

### Medium AI
- **Strategy**: MinMax with depth=2
- **Speed**: Moderate (0.1-1s per move)
- **Depth**: 2 moves ahead
- **Use case**: Intermediate players, balanced gameplay

### Hard AI
- **Strategy**: MinMax with depth=4
- **Speed**: Slower (1-10s per move)
- **Depth**: 4 moves ahead
- **Use case**: Advanced players, strategic gameplay

## Performance Tips

1. **For fast testing**: Use `--no-delay` flag
2. **For performance analysis**: Use `test_ai_levels.py`
3. **For balanced games**: Use different difficulty levels
4. **For debugging**: Monitor execution times to identify bottlenecks

## Integration

The AI classes can be used in your own code:

```python
from ia import AIFactory

# Create AIs
easy_ai = AIFactory.create_ai('easy', 'white')
medium_ai = AIFactory.create_ai('medium', 'black')
hard_ai = AIFactory.create_ai('hard', 'white')

# Use in games
move = easy_ai.make_decision(game_engine)
```

## Troubleshooting

- **Slow performance**: Hard AI can be slow on complex positions
- **No moves found**: Check if the game state is valid
- **Import errors**: Ensure all dependencies are installed
- **Memory issues**: Reduce max_turns for very long games 