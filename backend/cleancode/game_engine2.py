from backend.cleancode.ai_simulation2 import possible_epc_moves


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
        self.set_state(state)
        if current_player is not None:
            self.set_current_player(current_player)

    def is_terminal(self):
        return len(self.movable_epcs) == 0

    def winner(self):
        """
        Determine the winner based on the number of pawns on buildings (EPCs of height 5),
        then 4, then 3, etc. Returns WHITE, BLACK, or None for draw.
        """
        white_pions = self.pions[WHITE]
        black_pions = self.pions[BLACK]
        counts = {WHITE: [0]*5, BLACK: [0]*5}
        # Count the number of pions on each height of EPCs
        for pion in white_pions:
            epc_height = self.board[pion[0]][pion[1]]
            if epc_height > 0:
                counts[WHITE][epc_height - 1] += 1
        for pion in black_pions:
            epc_height = self.board[pion[0]][pion[1]]
            if epc_height > 0:
                counts[BLACK][epc_height - 1] += 1
        # Compare counts from highest to lowest
        for height in range(MAX_EPC_HEIGHT - 1, -1, -1):
            if counts[WHITE][height] > counts[BLACK][height]:
                return WHITE
            elif counts[BLACK][height] > counts[WHITE][height]:
                return BLACK
        return None  # Draw

    def possible_epc_moves(self, epc):
        moves = []
        if epc not in self.movable_epcs:
            return moves
        row, col = epc
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dx, col + dy
            while 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if self.board[new_row][new_col] == 0:
                    new_row += dx
                    new_col += dy
                    continue
                elif (new_row, new_col) not in self.movable_epcs: # Il a un pion
                    break
                elif self.board[row][col] + self.board[new_row][new_col] <= MAX_EPC_HEIGHT:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves
    
    def possible_pion_moves(self, pion):
        moves = []
        long_range = self.board[pion[0]][pion[1]]
        row, col = pion
        color = self.current_player if pion in self.pions[self.current_player] else self.ai_color
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            temp_row, temp_col = row + dx, col + dy
            while 0 <= temp_row < BOARD_SIZE and 0 <= temp_col < BOARD_SIZE:
                if self.board[temp_row][temp_col] == 0:
                    temp_row += dx
                    temp_col += dy
                    continue
                else:
                    for i in range(long_range):
                        new_row = temp_row + i * dx
                        new_col = temp_col + i * dy
                        if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                            if (new_row, new_col) in self.pions[color]:
                                pass