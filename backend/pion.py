class pion:
    def __init__(self, couleur):
        self.couleur = couleur
        self.position = None
    
    def __str__(self):
        return self.couleur
    
    def deplacer(self, nouvelle_position):
        self.position = nouvelle_position

    def peut_deplacer_vers(self, board, x_arrivee, y_arrivee):
        if not self.position:
            return False

        x_depart = self.position.x
        y_depart = self.position.y
        cell_depart = board.obtenir_cell(x_depart, y_depart)
        cell_arrivee = board.obtenir_cell(x_arrivee, y_arrivee)
        
        if not cell_depart or not cell_arrivee:
            return False

        # Calculer la distance de déplacement
        distance = abs(x_arrivee - x_depart) + abs(y_arrivee - y_depart)
        
        # Vérifier si la distance est valide (≤ EPC)
        if distance > cell_depart.epc:
            return False

        # Vérifier si le chemin est libre (peut sauter par-dessus les cases vides)
        if not self.chemin_libre(board, x_depart, y_depart, x_arrivee, y_arrivee):
            return False

        # Si la case d'arrivée est occupée
        if cell_arrivee.est_occupee():
            # Ne peut pas capturer sa propre pièce
            if cell_arrivee.pion.couleur == self.couleur:
                return False
            # Pour capturer, la distance doit être exactement égale à l'EPC
            if distance != cell_depart.epc:
                return False

        return True

    def chemin_libre(self, board, x1, y1, x2, y2):
        # Vérifier si le chemin est horizontal ou vertical
        if x1 != x2 and y1 != y2:
            return False

        # On peut sauter par-dessus les cases vides
        if x1 == x2:  # Déplacement horizontal
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                if board.grille[x1][y].est_occupee():
                    return False
        else:  # Déplacement vertical
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                if board.grille[x][y1].est_occupee():
                    return False
        return True