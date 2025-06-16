# case.py
class piece:
    def __init__(self):
        self.epc = 1  # Empilement de pièces carrées (1-5)
        self.pion = None  # Reference to the pion on this piece

    def est_vide(self):
        return self.epc == 0

    def est_libre(self):
        return self.pion is None

    def est_occupee(self):
        return self.pion is not None

    def est_building(self):
        return self.epc == 5

    def ajouter_epc(self, quantite):
        # Vérifier si l'ajout ne dépasse pas la limite de 5
        if self.epc + quantite <= 5:
            self.epc += quantite
            return True
        return False

    def retirer_epc(self, quantite):
        if self.epc - quantite >= 0:
            self.epc -= quantite
            return True
        return False

    def placer_pion(self, pion):
        if self.est_libre():
            self.pion = pion
            pion.position = self
            return True
        return False

    def retirer_pion(self):
        pion = self.pion
        self.pion = None
        if pion:
            pion.position = None
        return pion

    def afficher(self):
        p = self.pion.couleur if self.pion else ' '
        return f"{self.epc}{p}"