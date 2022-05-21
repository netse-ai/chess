from collections import OrderedDict


COLS = ["1", "2", "3", "4", "5", "6", "7", "8"]
ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]

COLORS = {
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
    "UNDERLINE": "\033[4m",
    "RESET": "\033[0m",
}

class Square(object):
    """
    Square is a container class for each tile on the board.
    It holds the piece and its corresponding icon
    """
    def __init__(self, piece):
        self.piece = piece
        self.icon = piece.icon


class State(object):
    """"
    State manages all aspects of the game
    """
    def __init__(self):
        self.piece_positions = OrderedDict()
        for i in ROWS:
            for j in COLS:
                sq = Square(Piece(COLORS["BLUE"], i + j))
                self.piece_positions[i + j] = sq

    def init_board(self):
        black_pawn_labels = [ROWS[i] + "7" for i in range(8)]
        white_pawn_labels = [ROWS[i] + "2" for i in range(8)]
        castle_labels = [
            Castle(COLORS["WHITE"], "A1"),
            Castle(COLORS["WHITE"], "H1"),
            Castle(COLORS["BLACK"], "A8"),
            Castle(COLORS["BLACK"], "H8"),
        ]
        
        knight_labels = [
            Knight(COLORS["WHITE"], "B1"),
            Knight(COLORS["WHITE"], "G1"),
            Knight(COLORS["BLACK"], "B8"),
            Knight(COLORS["BLACK"], "G8"),
        ]
        bishop_labels = [
            Bishop(COLORS["WHITE"], "C1"),
            Bishop(COLORS["WHITE"], "F1"),
            Bishop(COLORS["BLACK"], "C8"),
            Bishop(COLORS["BLACK"], "F8"),
        ]
        queen_labels = [
            Queen(COLORS["WHITE"], "D1"),
            Queen(COLORS["BLACK"], "E8"),
        ]
        king_labels = [
            King(COLORS["WHITE"], "E1"),
            King(COLORS["BLACK"], "D8"),
        ]
        for i in black_pawn_labels:
            self.piece_positions[i].piece = Pawn(COLORS["BLACK"], i)
            self.piece_positions[i].icon = self.piece_positions[i].piece.icon
        for i in white_pawn_labels:
            self.piece_positions[i].piece = Pawn(COLORS["WHITE"], i)
            self.piece_positions[i].icon = self.piece_positions[i].piece.icon
        for i in castle_labels:
            self.piece_positions[i.pos].piece = i
            self.piece_positions[i.pos].icon = i.icon
        for i in knight_labels:
            self.piece_positions[i.pos].piece = i
            self.piece_positions[i.pos].icon = i.icon
        for i in bishop_labels:
            self.piece_positions[i.pos].piece = i
            self.piece_positions[i.pos].icon = i.icon
        for i in queen_labels:
            self.piece_positions[i.pos].piece = i
            self.piece_positions[i.pos].icon = i.icon
        for i in king_labels:
            self.piece_positions[i.pos].piece = i
            self.piece_positions[i.pos].icon = i.icon


class Piece(object):
    """
    Base class for each chess pieces.
    """
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.points = None
        self.is_removed_from_play = False
        self.icon = "."
        self.moves = OrderedDict()
        self.state = None

    def update_state(self, state):
        self.state = state

    def can_move(self, move):
        if self.state[move].piece.color == self.color:
            return False
        return True
        
    def clear_moves(self):
        self.moves = OrderedDict()


class Pawn(Piece):
    def __init__(self, color, pos):
        Piece.__init__(self, color, pos)
        self.points = 0
        self.icon = "P"

    def get_moves(self):
        move_left_diag = str(chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) + 1))
        move_right_diag = str(chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) + 1))
        move_up = self.pos[0] + str(int(self.pos[1]) + 1)

        if self.pos[0] == "A":
            if self.state[move_right_diag].piece.icon != ".":
                self.moves[move_left_diag] = move_left_diag
            if self.state[move_up].piece.icon == ".":
                self.moves[move_up] = move_up
        elif self.pos[0] == "H":
            if self.state[move_left_diag].piece.icon != ".":
                self.moves[move_left_diag] = move_left_diag
            if self.state[move_up].piece.icon == ".":
                self.moves[move_up] = move_up
        else:
            self.moves[move_up] = move_up
        return self.moves


class Castle(Piece):
    def __init__(self, color, pos):
        Piece.__init__(self, color, pos)
        self.points = 1
        self.icon = "C"

    def get_moves(self):
        moves_forward = [move for move in self.state if move[0] == self.pos[0] and int(move[1]) > int(self.pos[1]) or int(move[1]) < int(self.pos[1])]
        idx = 0
        for move in moves_forward:
            square = self.state[move]
            if square.piece.pos != self.pos and square.piece.icon != "." and square.piece.color == self.color:
                print("here:", square.piece.color, self.color)
                break
            idx += 1
            
        moves = []
        if idx > 0:
            moves = moves_forward[:idx]
        self.moves = moves
        print(idx)
        print(self.moves)
        return self.moves


class Knight(Piece):
    def __init__(self, color, pos):
        Piece.__init__(self, color, pos)
        self.points = 2
        self.icon = "K"

    def get_moves(self):
        move_top_left = str(chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) + 2))
        move_top_right = str(chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) + 2))
        move_mid_right_up = str(chr(ord(self.pos[0]) + 2) + str(int(self.pos[1]) + 1))
        move_mid_right_down = str(chr(ord(self.pos[0]) + 2) + str(int(self.pos[1]) - 1))
        move_mid_left_up = str(chr(ord(self.pos[0]) - 2) + str(int(self.pos[1]) + 1))
        move_mid_left_down = str(chr(ord(self.pos[0]) - 2) + str(int(self.pos[1]) - 1))
        move_back_left = str(chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) - 2))
        move_back_right = str(chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) - 2))

        moves = [
            move_top_left,
            move_top_right,
            move_mid_right_up,
            move_mid_right_down,
            move_mid_left_up,
            move_mid_left_down,
            move_back_left,
            move_back_right,
        ]
        for move in moves:
            if move[0] in ROWS and move[1] in COLS:
                if self.can_move(move):
                    self.moves[move] = move

        return self.moves


class Bishop(Piece):
    def __init__(self, color, pos):
        Piece.__init__(self, color, pos)
        self.points = 3
        self.icon = "B"


class Queen(Piece):
    def __init__(self, color, pos):
        Piece.__init__(self, color, pos)
        self.points = 4
        self.icon = "Q"


class King(Piece):
    def __init__(self, color, pos):
        Piece.__init__(self, color, pos)
        self.points = 5
        self.icon = "K"


class Board(object):
    def __init__(self, state):
        self.colLabels = COLS
        self.rowLabels = ROWS
        if state:
            self.state = state
            self._grid = self.state.piece_positions
            self.state.init_board()
            self.update_board()

    def update_board(self):
        for key in self._grid.keys():
            self._grid[key].piece.update_state(self.state.piece_positions)

    def update_board_with_move(self, choice, move):
        for m in self._grid[choice].piece.get_moves():
            print(m)
            if m != move:
                self.state.piece_positions[m] = Square(
                    Piece(COLORS["BLUE"], self._grid[choice].piece.pos)
                )
        self.state.piece_positions[move] = self._grid[choice]
        self.state.piece_positions[move].piece.pos = move
        self.state.piece_positions[choice] = Square(
            Piece(COLORS["BLUE"], self._grid[choice].piece.pos)
        )
        self.state.piece_positions[move].piece.update_state(self.state.piece_positions)
        self.state.piece_positions[move].piece.state[move].piece.clear_moves()
        self._grid = self.state.piece_positions
        self.update_board()

    def render_board(self, choice=None):
        if choice != None:
            print(self._grid[choice])
            moves = self._grid[choice].piece.get_moves()
            print()
            m_str = COLORS["GREEN"]
            for m in moves:
                self._grid[m].piece.color = COLORS["GREEN"]
                m_str += m
                m_str += " "
            print(COLORS["WHITE"] + "Available Moves: ", m_str)
        print()
        for i in range(len(self.rowLabels)):
            for j in range(len(self.colLabels)):
                label_i = self.rowLabels[i]
                label_j = self.colLabels[j]
                target = self._grid[label_i + label_j]
                print(target.piece.color + target.icon, end=" ")
            print()


state = State()
board = Board(state)
board.render_board()

print(COLORS["WHITE"])

while True:
    choice = input("Choose Peice: ")
    board.render_board(choice)
    print(COLORS["WHITE"])
    move = input("Choose Move: ")
    board.update_board_with_move(choice, move)
    board.render_board()
    print(COLORS["WHITE"])
