from game import Game
import time

def main():
    # Créer une nouvelle partie
    game = Game()
    turn = 1
    
    print("Début de la partie AI vs AI")
    print("=" * 30)
    
    # Boucle principale du jeu
    while True:
        print(f"\nTour {turn}")
        print("-" * 20)
        
        # Afficher l'état actuel du plateau
        board_state = game.get_board_state()
        for row in board_state:
            print(" ".join(str(cell) for cell in row))
        
        # Jouer un tour
        if not game.play_turn():
            break
            
        # Attendre un peu pour voir le déroulement
        time.sleep(1)
        turn += 1
    
    # Afficher le résultat final
    print("\nFin de la partie")
    print("=" * 30)
    winner = game.get_winner()
    if winner == 'draw':
        print("Match nul!")
    else:
        print(f"Le gagnant est: {winner}")
    
    # Afficher l'état final du plateau
    print("\nÉtat final du plateau:")
    board_state = game.get_board_state()
    for row in board_state:
        print(" ".join(str(cell) for cell in row))

if __name__ == "__main__":
    main() 