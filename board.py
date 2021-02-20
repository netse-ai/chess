from collections import OrderedDict


COLS = ["1", "2", "3", "4", "5", "6", "7", "8"]
ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]

COLORS = {
    "BLACK": '\033[30m',
    "RED": '\033[31m',
    "GREEN": '\033[32m',
    "YELLOW": '\033[33m',
    "BLUE": '\033[34m',
    "MAGENTA": '\033[35m',
    "CYAN": '\033[36m',
    "WHITE": '\033[37m',
    "UNDERLINE": '\033[4m',
    "RESET": '\033[0m'
}


class Square(object):
    def __init__(self, piece):
        self.piece = piece
        self.icon = piece.icon


class State(object):
    def __init__(self):
        self.piece_positions = OrderedDict()
        for i in ROWS:
            for j in COLS:
                sq = Square(Piece(COLORS["BLUE"], i+j))
                self.piece_positions[i+j] = sq

    def init_board(self):
        black_pawn_labels = [ROWS[i] + "7" for i in range(8)]
        white_pawn_labels = [ROWS[i] + "2" for i in range(8)]
        castle_labels = [
            Castle(COLORS["WHITE"], "A1"), Castle(COLORS["WHITE"], "H1"),
            Castle(COLORS["BLACK"], "A8"), Castle(COLORS["BLACK"], "H8")
        ]
        knight_labels = [
            Knight(COLORS["WHITE"], "B1"), Knight(COLORS["WHITE"], "G1"),
            Knight(COLORS["BLACK"], "B8"), Knight(COLORS["BLACK"], "G8")
        ]
        bishop_labels = [
            Bishop(COLORS["WHITE"], "C1"), Bishop(COLORS["WHITE"], "F1"),
            Bishop(COLORS["BLACK"], "C8"), Bishop(COLORS["BLACK"], "F8")
        ]
        queen_labels = [
            Queen(COLORS["WHITE"], "D1"), Queen(COLORS["BLACK"], "E8"),
        ]
        king_labels = [
            King(COLORS["WHITE"], "E1"), King(COLORS["BLACK"], "D8"),
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
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.points = None
        self.is_removed_from_play = False
        self.icon = "."
        self.moves = []
        self.state = None

    def update_state(self, state):
        self.state = state


class Pawn(Piece):
    def __init__(self, color, pos):
        Piece.__init__(self, color, pos)
        self.points = 0
        self.icon = "P"

    def get_moves(self):
        move_left_diag = (
            str(chr(ord(self.pos[0])-1) + str(int(self.pos[1]) + 1))
            )
        move_right_diag = (
            str(chr(ord(self.pos[0])+1) + str(int(self.pos[1]) + 1))
            )
        move_up = self.pos[0] + str(int(self.pos[1]) + 1)
        if (self.pos[0] == "A"):
            if (self.state[move_right_diag].piece.icon != "."):
                self.moves.append(move_right_diag)
            if (self.state[move_up].piece.icon == "."):
                self.moves.append(move_up)
        elif (self.pos[0] == "H"):
            if (self.state[move_left_diag].piece.icon != "."):
                self.moves.append(move_left_diag)
            if (self.state[move_up].piece.icon == "."):
                self.moves.append(move_up)
        else:
            self.moves.append(move_up)
        return self.moves


class Castle(Piece):
    def __init__(self, color, pos):
        Piece.__init__(self, color, pos)
        self.points = 1
        self.icon = "C"


class Knight(Piece):
    def __init__(self, color, pos):
        Piece.__init__(self, color, pos)
        self.points = 2
        self.icon = "K"

    def get_moves(self):
        move_top_left = (
            str(chr(ord(self.pos[0])-1) + str(int(self.pos[1]) + 2))
            )
        move_top_right = (
            str(chr(ord(self.pos[0])+1) + str(int(self.pos[1]) + 2))
            )
        if (self.pos[0] == "A"):
            if (self.state[move_top_right].piece.icon):
                self.moves.append(move_top_right)
        elif (self.pos[0] == "H"):
            if (self.state[move_top_left].piece.icon):
                self.moves.append(move_top_left)
        else:
            self.moves.append(move_top_left)
            self.moves.append(move_top_right)
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
        if (state):
            self.state = state
            self._grid = self.state.piece_positions
            self.state.init_board()
            self.populate_board()

    def populate_board(self):
        for key in self._grid.keys():
            self._grid[key].piece.update_state(self.state.piece_positions)

    def render_board(self):
        print()
        for i in range(len(self.rowLabels)):
            for j in range(len(self.colLabels)):
                label_i = self.rowLabels[i]
                label_j = self.colLabels[j]
                target = self._grid[label_i + label_j]
                print(
                    target.piece.color + target.icon,
                    end=" "
                )
            print()

    def render_board_with_moves(self, choice):
        moves = self._grid[choice].piece.get_moves()
        print()
        m_str = COLORS["GREEN"]
        for m in moves:
            self._grid[m].piece.color = COLORS["GREEN"]
            m_str += m
        print(COLORS["WHITE"] + "Available Moves: ", m_str)
        print()
        for i in range(len(self.rowLabels)):
            for j in range(len(self.colLabels)):
                label_i = self.rowLabels[i]
                label_j = self.colLabels[j]
                target = self._grid[label_i + label_j]
                print(
                    target.piece.color + target.icon,
                    end=" "
                )
            print()
        print()


state = State()
board = Board(state)
board.render_board()

print(COLORS["WHITE"])

choice = input("Choose Peice: ")
board.render_board_with_moves(choice)

print(COLORS["WHITE"])
