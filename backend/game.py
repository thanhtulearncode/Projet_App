from game_engine import GameEngine
from AI import GameAI
from Action import Action
from ia import MinMaxAI

class Game:
    def __init__(self, taille=8):
        """
        Initialise une nouvelle partie
        :param taille: Taille du plateau (par défaut 8x8)
        """
        self.game_engine = GameEngine()
        self.ai1 = GameAI('hard', 'white')
        self.ai2 = MinMaxAI('black', depth=2)
        self.current_player = 'white'
        self.game_over = False
        
    def play_turn(self):
        """
        Joue un tour complet (phase 1 et 2)
        :return: True si le jeu continue, False si c'est terminé
        """
        if self.game_over:
            return False
            
        # Déterminer quelle IA joue
        current_ai = self.ai1 if self.current_player == 'white' else self.ai2
        
        # Obtenir la décision de l'IA
        move = current_ai.make_decision(self.game_engine)
        if not move:
            self.game_over = True
            return False
            
        # Exécuter le mouvement
        action = Action(move[0], move[1], move[2])
        if not action.execute(self.game_engine):
            self.game_over = True
            return False
            
        # Vérifier si le jeu est terminé
        if self.game_engine.check_game_over():
            self.game_over = True
            return False
            
        # Changer de joueur
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True
        
    def get_winner(self):
        """
        Détermine le gagnant
        :return: 'white', 'black' ou 'draw'
        """
        if not self.game_over:
            return None
            
        return self.game_engine.get_winner()
        
    def get_board_state(self):
        """
        Retourne l'état actuel du plateau
        :return: État du plateau
        """
        return self.game_engine.get_state()
        
    def reset(self):
        """
        Réinitialise la partie
        """
        self.game_engine = GameEngine()
        self.current_player = 'white'
        self.game_over = False 