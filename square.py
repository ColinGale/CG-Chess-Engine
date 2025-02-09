class Square:

    ALPHACOLS = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    def __init__(self, row, col, piece=None):
        ALPHACOLS = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        self.row = row
        self.col = col
        self.piece = piece
        self.col_name = ALPHACOLS[col]


    def has_piece(self):
        return self.piece is not None

    def is_empty(self):
        return self.piece is None

    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_rival(self, color):
        return self.has_rival_piece(color) or not self.has_piece()

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True


    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        return ALPHACOLS[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col