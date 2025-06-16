from backend.piece2 import piece
from backend.pion import pion

class board:
    def __init__(self, taille=8):
        self.taille = taille
        self.grille = [[piece() for _ in range(taille)] for _ in range(taille)]

    def est_valide_position(self, x, y):
        return 0 <= x < self.taille and 0 <= y < self.taille

    def obtenir_cell(self, x, y):
        if self.est_valide_position(x, y):
            return self.grille[x][y]
        return None

    def deplacer_piece_phase1(self, x_depart, y_depart, x_arrivee, y_arrivee):
        cell_depart = self.obtenir_cell(x_depart, y_depart)
        cell_arrivee = self.obtenir_cell(x_arrivee, y_arrivee)
        
        if not cell_depart or not cell_arrivee:
            return False
            
        pion = cell_depart.pion
        if not pion:
            return False

        # Vérifier si le déplacement est valide
        if not pion.peut_deplacer_vers(self, x_arrivee, y_arrivee, phase=1):
            return False

        # Si la case d'arrivée est occupée par une pièce adverse, la capturer
        pion_capture = None
        if cell_arrivee.est_occupee():
            pion_capture = cell_arrivee.retirer_pion()

        # Déplacer la piece
        cell_depart.retirer_pion()
        cell_arrivee.placer_pion(pion)

        # Exécuter immédiatement la phase 2
        self.deplacer_epc_phase2(x_arrivee, y_arrivee)

        return pion_capture  # Retourner la pièce capturée pour la replacer plus tard

    def deplacer_epc_phase2(self, x_depart, y_depart, x_arrivee, y_arrivee):
        cell_depart = self.obtenir_cell(x_depart, y_depart)
        cell_arrivee = self.obtenir_cell(x_arrivee, y_arrivee)
        
        if not cell_depart or not cell_arrivee:
            return False
            
        # Vérifier que la case de départ a un EPC et n'est pas occupée
        if cell_depart.est_occupee() or cell_depart.est_vide():
            return False

        # Vérifier la distance (1 case)
        if abs(x_arrivee - x_depart) + abs(y_arrivee - y_depart) != 1:
            return False

        # Vérifier si l'EPC de destination peut accepter plus d'EPC
        if cell_arrivee.epc + cell_depart.epc > 5:
            return False

        # Vérifier si la case d'arrivée est occupée
        if cell_arrivee.est_occupee():
            return False

        # Déplacer l'EPC
        if cell_arrivee.ajouter_epc(cell_depart.epc):
            cell_depart.epc = 0  # La case de départ devient vide
            return True
        return False

    def chemin_libre_phase1(self, x1, y1, x2, y2):
        # Vérifier si le chemin est horizontal ou vertical
        if x1 != x2 and y1 != y2:
            return False

        # Vérifier chaque case entre le départ et l'arrivée
        # On peut sauter par-dessus les cases vides
        if x1 == x2:  # Déplacement horizontal
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                if self.grille[x1][y].est_occupee():
                    return False
        else:  # Déplacement vertical
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                if self.grille[x][y1].est_occupee():
                    return False
        return True

    def afficher(self):
        for i in range(self.taille):
            ligne = ""
            for j in range(self.taille):
                ligne += self.grille[i][j].afficher() + " "
            print(ligne)