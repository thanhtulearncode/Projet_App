class Piece:
    def __init__(self, name: str, color: str, position: tuple):
        self.name = name
        self.color = color
        self.position = position

    def move(self, new_position: tuple):
        self.position = new_position

    def __repr__(self):
        return f"{self.color} {self.name} at {self.position}"
    
class Square(Piece):
    def __init__(self, color: str, position: tuple):
        super().__init__("Square", color, position)

    def can_move(self, new_position: tuple):
        # Logic for square movement
        return True  # Placeholder logic

class Pawn(Piece):
    def __init__(self, color: str, position: tuple):
        super().__init__("Pawn", color, position)

    def can_move(self, new_position: tuple):
        # Logic for pawn movement
        return True  # Placeholder logic