import copy
import os
from constants import *
from square import Square
from piece import *
from move import Move
from sound import Sound
from opening_book import Book

class Board:

    def __init__(self):
        self.squares = [[0] * COLS for row in range(ROWS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.check = False
        self.over = False
        self.book = Book()
        self.url = OPENING

    def move(self, piece, move, testing=False, ai=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].is_empty()

        # console board move update
        move.captured = self.squares[final.row][final.col].piece
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join("assets/sounds/capture.wav"))
                    sound.play()

            # pawn en passant
            if self.en_passant(initial, final):
                piece.en_passant = True
            # pawn promotion
            self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King) and not testing:
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                if ai:
                    row = 7 if piece.color == "white" else 0
                    cols = (0, 3) if rook == piece.left_rook else (7, 5)
                    initial = Square(row, cols[0])
                    final = Square(row, cols[1])
                    moveR = Move(initial, final)
                    rook.add_move(moveR)


                self.move(rook, rook.moves[-1])
        # move
        piece.moved = True
        piece.sum_moves += 1

        # clear valid moves
        piece.clear_moves()
        self.last_move = move


    def undo_move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = piece
        self.squares[final.row][final.col].piece = move.captured

        piece.sum_moves -= 1
        if piece.sum_moves == 0:
            piece.moved = False








    def valid_move(self, piece, move):
        return move in piece.moves

    def all_valid_moves(self, color):
        valid_move_count = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.calc_moves(piece, row, col)
                    for move in piece.moves:
                        valid_move_count += 1

                    piece.clear_moves()

        return valid_move_count

    def all_capture_moves(self, color):
        all_capture_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.calc_moves(piece, row, col)
                    for move in piece.moves:
                        if self.squares[move.final.row][move.final.col].piece:
                            all_capture_moves.append((piece, move))
                    piece.clear_moves()

        return all_capture_moves


    def all_valid_move_list(self, color):
        all_valid_moves_l = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.calc_moves(piece, row, col)
                    for move in piece.moves:
                        all_valid_moves_l.append((move, piece))

                    piece.clear_moves()

        return all_valid_moves_l

    def checkmate(self, color):
        if self.all_valid_moves(color) == 0 and self.current_in_check(color):
            self.over = True
            return True
        else:
            return False

    def stalemate(self, color):
        if self.all_valid_moves(color) == 0 and self.current_in_check(color) is False:
            self.over = True
            return True
        else:
            return False

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def en_passant(self, initial, final):
        return abs(initial.row - final.row) == 2

    def set_false_en_passant(self):
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    pawn = self.squares[row][col].piece
                    if self.last_move:
                        if self.last_move.final.piece != pawn:
                            pawn.en_passant = False
                        if pawn.can_en_passant:
                            pawn.can_en_passant = False
                        elif not pawn.can_en_passant:
                            pawn.clear_moves()


    def current_in_check(self, color):
        temp_board = copy.deepcopy(self)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False


    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False


    def calc_moves(self, piece, row, col, bool=True):
        '''
        This method will calculate all the valid moves of a specific piece
        on a specific position.
        '''

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.direction
            end = row + (piece.direction * (1 + steps))
            for move_row in range(start, end, piece.direction):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)

                    # pawn is blocked
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal move
            possible_move_row = row + piece.direction
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        piece.add_move(move)

            # en passant moves
            r = 3 if piece.color == "white" else 4
            fr = 2 if piece.color == "white" else 5
            # left
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_rival_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            piece.can_en_passant = True
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            move = Move(initial, final)
                            piece.add_move(move)

            # right
            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col+1].has_rival_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            piece.can_en_passant = True
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            move = Move(initial, final)
                            piece.add_move(move)

            # checks for checks
            if bool:
                index = 0
                while index < len(piece.moves):
                    if self.in_check(piece, piece.moves[index]):
                        piece.moves.pop(index)
                        index -= 1
                    index += 1









        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row - 2, col - 1),
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        piece.add_move(move)

                if bool:
                    index = 0
                    while index < len(piece.moves):
                        if self.in_check(piece, piece.moves[index]):
                            piece.moves.pop(index)
                            index -= 1
                        index += 1

        def straight_line_moves(incrs):
            for increment in incrs:
                row_incr, column_incr = increment
                possible_move_row = row + row_incr
                possible_move_col = col + column_incr

                # while True
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            piece.add_move(move)

                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break

                        else:
                            break


                    else:
                        break

                    possible_move_row += row_incr
                    possible_move_col += column_incr

            if bool:
                index = 0
                while index < len(piece.moves):
                    if self.in_check(piece, piece.moves[index]):
                        piece.moves.pop(index)
                        index -= 1
                    index += 1


        def king_moves():
            adj = [
                (row + 1, col + 0),
                (row + 1, col + 1),
                (row + 0, col + 1),
                (row - 1, col + 1),
                (row - 1, col + 0),
                (row - 1, col - 1),
                (row + 0, col - 1),
                (row + 1, col - 1)
            ]
            # normal moves
            for possible_move in adj:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)  # piece = piece
                        move = Move(initial, final)

                        piece.add_move(move)

            # castling moves
            if not piece.moved:

                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): #  No castling
                                break

                            if c == 3:
                                # adds left rook to king piece
                                piece.left_rook = left_rook
                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                left_rook.add_move(moveR)
                                piece.add_move(moveK)


                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():  # No castling
                                break

                            if c == 6:
                                # adds right rook to king piece
                                piece.right_rook = right_rook
                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                right_rook.add_move(moveR)
                                piece.add_move(moveK)

            if bool:
                index = 0
                while index < len(piece.moves):
                    if self.in_check(piece, piece.moves[index]):
                        piece.moves.pop(index)
                        index -= 1
                    index += 1



        if piece.name == "pawn":
            pawn_moves()
        elif piece.name == "knight":
            knight_moves()
        elif piece.name == "bishop":
            straight_line_moves([(-1, 1),  # up right
                                 (1, 1),  # down right
                                 (-1, -1),  # up left
                                 (1, -1)  # down left
                                 ])
        elif piece.name == "rook":
            straight_line_moves([(-1, 0),  # up
                                 (0, 1),  # right
                                 (1, 0),  # down
                                 (0, -1)  # left
                                 ])
        elif piece.name == "queen":
            straight_line_moves([(-1, 1),  # up right
                                 (1, 1),  # down right
                                 (-1, -1),  # up left
                                 (1, -1),  # down left
                                 (-1, 0),  # up
                                 (0, 1),  # right
                                 (1, 0),  # down
                                 (0, -1)  # left
                                 ])
        elif piece.name == "king":
            king_moves()

    def move_to_string(self):
        last_move = self.last_move
        piece = self.squares[last_move.final.row][last_move.final.col].piece

        # capture move
        if last_move.captured:
            if piece.name == "pawn":
                return str(last_move.initial.col_name) + "x" + last_move.notation
            elif piece.name == "knight":
                notation = piece.name[1].upper() + "x" + last_move.notation
                return notation
            else:
                notation = piece.name[0].upper() + "x" + last_move.notation
                return notation
        else:
            if piece.name == "pawn":
                return last_move.notation
            elif piece.name == "knight":
                notation = piece.name[1].upper() + last_move.notation
                return notation
            else:
                notation = piece.name[0].upper() + last_move.notation
                return notation

    def string_to_move(self, game, string):
        R_ALPHACOLS = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        # pawn move
        if string[0].islower():
            # forward move
            if "x" not in string:
                col = R_ALPHACOLS[string[0]]
                row = 8 - int(string[-1])

                initial_row = row + 1 if game.next_player == "white" else row - 1
                piece = self.squares[initial_row][col].piece
                if piece is None:
                    initial_row = row + 2 if game.next_player == "white" else row - 2
                    piece = self.squares[initial_row][col].piece

                initial = Square(initial_row, col)
                final = Square(row, col)
                move = Move(initial, final)

                return piece, move

            # capture move
            else:
                initial_col = R_ALPHACOLS[string[0]]
                final_col = R_ALPHACOLS[string[2]]
                final_row = 8 - int(string[-1])
                initial_row = final_row + 1 if game.next_player == "white" else final_row - 1

                piece = self.squares[initial_row][initial_col].piece
                initial = Square(initial_row, initial_col)
                final = Square(final_row, final_col)
                move = Move(initial, final)

                return piece, move

        else:
            # king move
            if string[0] == "K":
                final_col = R_ALPHACOLS[string[-2]]
                final_row = 8 - int(string[-1])
                piece = None
                initial_row, initial_col = -1, -1
                for row in range(ROWS):
                    for col in range(COLS):
                        piece = self.squares[row][col].piece
                        if piece != None and piece.name == "king" and piece.color == game.next_player:
                            initial_row, initial_col = row, col
                            break

                    if initial_row != -1:
                        break

                initial = Square(initial_row, initial_col)
                final = Square(final_row, final_col)
                move = Move(initial, final)

                return piece, move

            # queen move
            if string[0] == "Q":
                final_col = R_ALPHACOLS[string[-2]]
                final_row = 8 - int(string[-1])
                piece = None
                initial_row, initial_col = -1, -1
                for row in range(ROWS):
                    for col in range(COLS):
                        piece = self.squares[row][col].piece
                        if piece != None and piece.name == "queen" and piece.color == game.next_player:
                            initial_row, initial_col = row, col
                            break

                    if initial_row != -1:
                        break

                initial = Square(initial_row, initial_col)
                final = Square(final_row, final_col)
                move = Move(initial, final)

                return piece, move

            # rook move
            if string[0] == "R":
                final_col = R_ALPHACOLS[string[-2]]
                final_row = 8 - int(string[-1])
                piece = None
                initial_row, initial_col = -1, -1
                if len(string) == 4 and "x" not in string:
                    if string[1].isnumeric():
                        initial_row = 8 - int(string[1])
                        initial_col = final_col
                    else:
                        initial_col = R_ALPHACOLS[string[1]]
                        initial_row = final_row
                    piece = self.squares[initial_row][initial_col].piece
                else:
                    for row in range(ROWS):
                        piece = self.squares[row][final_col].piece
                        if piece != None and piece.name == "rook" and piece.color == game.next_player:
                            initial_row, initial_col = row, final_col
                            break

                    if initial_row == -1:
                        for col in range(COLS):
                            piece = self.squares[final_row][col].piece
                            if piece != None and piece.name == "rook" and piece.color == game.next_player:
                                initial_row, initial_col = final_row, col
                                break

                initial = Square(initial_row, initial_col)
                final = Square(final_row, final_col)
                move = Move(initial, final)

                return piece, move

            # bishop move
            if string[0] == "B":
                final_col = R_ALPHACOLS[string[-2]]
                final_row = 8 - int(string[-1])
                piece = None
                mod1 = (final_row + final_col) % 2

                initial_row, initial_col = -1, -1
                for row in range(ROWS):
                    for col in range(COLS):
                        piece = self.squares[row][col].piece
                        if (row + col) % 2 == mod1:
                            if piece != None and piece.name == "bishop" and piece.color == game.next_player:
                                initial_row, initial_col = row, col
                                break

                    if initial_row != -1:
                        break

                initial = Square(initial_row, initial_col)
                final = Square(final_row, final_col)
                move = Move(initial, final)

                return piece, move

            # knight move
            if string[0] == "N":
                final_col = R_ALPHACOLS[string[-2]]
                final_row = 8 - int(string[-1])
                piece = None

                # more than one knight can move to square
                if len(string) == 4 and "x" not in string:
                    if string[1].isnumeric():
                        initial_row = 8 - int(string[1])
                        for col in range(COLS):
                            piece = self.squares[initial_row][col].piece
                            if piece != None and piece.name == "knight" and piece.color == game.next_player:
                                initial_col = col
                                break
                    else:
                        initial_col = R_ALPHACOLS[string[1]]
                        for row in range(ROWS):
                            piece = self.squares[row][initial_col].piece
                            if piece != None and piece.name == "knight" and piece.color == game.next_player:
                                initial_row = row
                                break

                # only one knight can move to square
                else:
                    possible_moves = [
                        (final_row - 2, final_col - 1),
                        (final_row - 2, final_col + 1),
                        (final_row - 1, final_col + 2),
                        (final_row + 1, final_col + 2),
                        (final_row + 2, final_col + 1),
                        (final_row + 2, final_col - 1),
                        (final_row + 1, final_col - 2),
                        (final_row - 1, final_col - 2)
                    ]

                    for tup in possible_moves:
                        # checks if on board
                        if Square.in_range(tup[0], tup[1]):
                            piece = self.squares[tup[0]][tup[1]].piece

                        if piece != None and piece.name == "knight" and piece.color == game.next_player:
                            initial_row, initial_col = tup[0], tup[1]
                            break

                initial = Square(initial_row, initial_col)
                final = Square(final_row, final_col)
                move = Move(initial, final)

                return piece, move

            # castling move
            if string[0] == "O":
                final_row = 0 if game.next_player == "black" else 7
                piece = self.squares[final_row][4].piece
                final_col = 6 if len(string) == 3 else 2

                initial = Square(final_row, 4)
                final = Square(final_row, final_col)
                # the king's move
                move = Move(initial, final)

                return piece, move

    def print_board(self):
        for row in self.squares:
            for column in row:
                if column.piece is None:
                    print('None', end="|")
                else:
                    print(column.piece.name, end="|")
            print("")

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # Creates all pawns
        for col in range(ROWS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Creates all knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 1, Knight(color))

        # Creates all bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Creates all rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Creates queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # Creates king
        self.squares[row_other][4] = Square(row_other, 4, King(color))


    def __str__(self):
        return str(self.squares)