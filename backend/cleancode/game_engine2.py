BOARD_SIZE = 8  

MAX_EPC_HEIGHT = 5

EMPTY = None
WHITE = 'W'
BLACK = 'B'

class GameEngine:
    def __init__(self, color_pair='black-white'):
        self.color_pair = color_pair
        self.board = self.create_initial_board()
        self.movable_epcs = set()
        self.pions = {
            WHITE: set(),
            BLACK: set()
        }
        self.current_player, self.ai_color = self.get_color_pair()

    def create_initial_board(self):
        board = [[1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.movable_epcs = {(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if board[row][col] == 1}
        for col in range(8):
            row = (col + 1) % 2
            if (col < 4) == (col % 2 == 0):
                self.pions[BLACK].add((row, col))
                self.movable_epcs.discard((row, col))
                self.pions[WHITE].add((7-row, col))
                self.movable_epcs.discard((7-row, col))
            else:
                self.pions[WHITE].add((row, col))
                self.movable_epcs.discard((row, col))
                self.pions[BLACK].add((7-row, col))
                self.movable_epcs.discard((7-row, col))

        return board
    
    def get_color_pair(self):
        if self.color_pair == 'black-white':
            return WHITE, BLACK
        elif self.color_pair == 'white-black':
            return BLACK, WHITE
        else:
            raise ValueError("Invalid color pair. Use 'black-white' or 'white-black'.")

    def get_state(self):
        return {
            'board': self.board,
            'movable_epcs': list(self.movable_epcs),
            'pions': {
                WHITE: list(self.pions[WHITE]),
                BLACK: list(self.pions[BLACK])
            },
            'current_player': self.current_player,
            'ai_color': self.ai_color
        }

    def set_state(self, state):
        self.board = state['board']
        self.movable_epcs = set(tuple(epc) for epc in state['movable_epcs'])
        self.pions[WHITE] = set(tuple(pion) for pion in state['pions'][WHITE])
        self.pions[BLACK] = set(tuple(pion) for pion in state['pions'][BLACK])
        self.current_player = state['current_player']
        self.ai_color = state['ai_color']

    def get_current_player(self):
        return self.current_player
    
    def set_current_player(self, color):
        if color not in (WHITE, BLACK):
            raise ValueError("Invalid color. Use 'W' for white or 'B' for black.")
        self.current_player = color

    def update(self, state, current_player=None):
        pass