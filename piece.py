import math
import os
from constants import *

class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == "white" else -1
        self.value = value_sign * value
        self.last_move = None
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        self.sum_moves = 0

    def position_value(self, row, col):
        if self.name == "knight":
            self.k_position_value(row, col)
            return self.value
        if self.name == "king":
            self.ki_position_value(row, col)
            return self.value
        if self.name == "pawn":
            self.p_position_value(row, col)
            return self.value
        if self.name == "bishop":
            self.b_position_value(row, col)
            return self.value
        if self.name == "rook":
            self.r_position_value(row, col)
            return self.value
        if self.name == "queen":
            self.q_position_value(row, col)
            return self.value

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'Assets/Images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):

    def __init__(self, color):
        self.direction = -1 if color == "white" else 1  # pygame coords
        self.en_passant = False
        self.can_en_passant = False
        super().__init__('pawn', color, 1.0)

    def p_position_value(self, row, col, p_value=1.0):
        pawn_array = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                        [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
                        [0.05, 0.05, 0.1, 0.25, 0.25, 0.1, 0.05, 0.05],
                        [0.0, 0.0, 0.0, 0.2, 0.2, 0.0, 0.0, 0.0],
                        [0.05, -0.05, -0.1, 0.0, 0.0, -0.1, -0.05, 0.05],
                        [0.05, 0.1, 0.1, -0.2, -0.2, 0.1, 0.1, 0.05],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

        if self.color == "white":
            self.value = p_value + pawn_array[row][col]
        elif self.color == "black":
            pawn_array = pawn_array[::-1]
            self.value = -p_value - pawn_array[row][col]

class Knight(Piece):

    def __init__(self, color):
        super().__init__("knight", color, 3.0)

    def k_position_value(self, row, col, k_value=3.0):
        knight_array = [[-0.5, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.5],
                        [-0.4, -0.2, 0.0, 0.0, 0.0, 0.0, -0.2, -0.4],
                        [-0.4, 0.0, 0.1, 0.2, 0.2, 0.1, 0.0, -0.4],
                        [-0.4, 0.0, 0.2, 0.25, 0.25, 0.2, 0.0, -0.4],
                        [-0.4, 0.0, 0.2, 0.25, 0.25, 0.2, 0.0, -0.4],
                        [-0.4, 0.0, 0.1, 0.2, 0.2, 0.1, 0.0, -0.4],
                        [-0.4, -0.2, 0.0, 0.0, 0.0, 0.0, -0.2, -0.4],
                        [-0.5, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.5]]

        if self.color == "white":
            self.value = k_value + knight_array[row][col]
        elif self.color == "black":
            self.value = -k_value - knight_array[row][col]




class Bishop(Piece):

    def __init__(self, color):
        super().__init__("bishop", color, 3.0)

    def b_position_value(self, row, col, b_value=3.0):
        bishop_array = [[-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
                        [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
                        [-0.1, 0.0, 0.05, 0.1, 0.1, 0.05, 0.0, -0.1],
                        [-0.1, 0.05, 0.05, 0.1, 0.1, 0.05, 0.05, -0.1],
                        [-0.1, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, -0.1],
                        [-0.1, 0.0, 0.1, 0.1, 0.1, 0.1, 0.1, -0.1],
                        [-0.1, 0.05, 0.0, 0.0, 0.0, 0.0, 0.05, -0.1],
                        [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2]]

        if self.color == "white":
            self.value = b_value + bishop_array[row][col]
        elif self.color == "black":
            bishop_array = bishop_array[::-1]
            self.value = -b_value - bishop_array[row][col]

class Rook(Piece):

    def __init__(self, color):
        super().__init__("rook", color, 5.0)

    def r_position_value(self, row, col, r_value=3.0):
        rook_array = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05],
                      [-0.05, 0.0, 0.0, 0.05, 0.05, 0.0, 0.0, -0.05],
                      [-0.05, 0.0, 0.0, 0.05, 0.05, 0.0, 0.0, -0.05],
                      [-0.05, 0.0, 0.0, 0.05, 0.05, 0.0, 0.0, -0.05],
                      [-0.05, 0.0, 0.0, 0.05, 0.05, 0.0, 0.0, -0.05],
                      [-0.05, 0.0, 0.0, 0.05, 0.05, 0.0, 0.0, -0.05],
                      [0.0, 0.0, 0.0, 0.05, 0.05, 0.0, 0.0, 0.0]]

        if self.color == "white":
            self.value = r_value + rook_array[row][col]
        elif self.color == "black":
            rook_array = rook_array[::-1]
            self.value = -r_value - rook_array[row][col]

class Queen(Piece):

    def __init__(self, color):
        super().__init__("queen", color, 9.0)

    def q_position_value(self, row, col, q_value=9.0):
        queen_array = [[-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2],
                      [0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
                      [-0.05, 0.0, 0.05, 0.05, 0.05, 0.05, 0.0, -0.1],
                      [-0.05, 0.0, 0.05, 0.05, 0.05, 0.05, 0.0, -0.05],
                      [-0.05, 0.0, 0.05, 0.05, 0.05, 0.05, 0.0, -0.05],
                      [-0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.0, -0.1],
                      [-0.1, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, -0.1],
                      [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2]]

        if self.color == "white":
            self.value = q_value + queen_array[row][col]
        elif self.color == "black":
            queen_array = queen_array[::-1]
            self.value = -q_value - queen_array[row][col]

class King(Piece):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__("king", color, 1000.0)

    def ki_position_value(self, row, col, ki_value=1000.0):
        king_array = [[-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                        [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                        [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                        [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                        [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                        [-0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2],
                        [0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
                        [0.2, 0.3, 0.1, 0.0, 0.0, 0.1, 0.3, 0.2]]

        if self.color == "white":
            self.value = ki_value + king_array[row][col]
        elif self.color == "black":
            king_array = king_array[::-1]
            self.value = -ki_value - king_array[row][col]

