from game import Game
from AI import GameAI
from ia import MinMaxAI
import time

def main():
    # Créer une nouvelle partie
    game = Game()
    # IA1 = GameAI (aléatoire/heuristique), IA2 = MinMaxAI
    game.ai1 = GameAI('hard', 'white')
    game.ai2 = MinMaxAI('black', depth=2)
    turn = 1
    print("Début de la partie AI vs AI (GameAI vs MinMaxAI)")
    print("=" * 30)
    while True:
        print(f"\nTour {turn}")
        print("-" * 20)
        board_state = game.get_board_state()
        for row in board_state:
            print(" ".join(str(cell) for cell in row))
        # Jouer un tour
        if not game.play_turn():
            break
        time.sleep(1)
        turn += 1
    print("\nFin de la partie")
    print("=" * 30)
    winner = game.get_winner()
    if winner == 'draw':
        print("Match nul!")
    else:
        print(f"Le gagnant est: {winner}")
    print("\nÉtat final du plateau:")
    board_state = game.get_board_state()
    for row in board_state:
        print(" ".join(str(cell) for cell in row))

if __name__ == "__main__":
    main()