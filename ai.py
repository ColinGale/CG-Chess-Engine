import random
from constants import *
from square import Square
from move import Move
from board import Board
from piece import Piece
from opening_book import Book
import copy

class AI:
    def __init__(self, depth):
        self.depth = depth
        self.best_move = None

    def random_move(self, board, next_player):
        move_list = self.move_order_analysis(board, next_player)
        random_int = random.randint(0, len(move_list) - 1)
        return move_list[random_int][1]

    def minimax(self, board, next_player, depth, alpha, beta):
        move_list = self.move_order_analysis(board, next_player) if depth > 0 else board.all_capture_moves(next_player)

        if board.checkmate(next_player) or board.stalemate(next_player) or depth == -1 or len(move_list) == 0:
            return self.static_eval(board, next_player)

        else:
            if next_player == "white":
                best = -10000

                for score, move in move_list:
                    temp_board = copy.deepcopy(board)
                    piece = temp_board.squares[move.initial.row][move.initial.col].piece
                    temp_board.move(piece, move, testing=True)
                    val = self.minimax(temp_board, "black", depth - 1, alpha, beta)

                    best = max(best, val)
                    alpha = max(alpha, val)
                    if val == alpha and self.depth == depth:
                        self.best_move = move
                    if beta <= alpha:
                        print("bad for black")
                        break

                return best
            else:
                best = 10000

                for score, move in move_list:
                    temp_board = copy.deepcopy(board)
                    piece = temp_board.squares[move.initial.row][move.initial.col].piece
                    temp_board.move(piece, move, testing=True)
                    val = self.minimax(temp_board, "white", depth - 1, alpha, beta)

                    best = min(best, val)
                    beta = min(beta, val)
                    if val == beta and self.depth == depth:
                        self.best_move = move
                    if beta <= alpha:
                        print("bad for white")
                        break

                return best

    # rewrite as just quiescene function



    def test_minimax(self, board, next_player, depth, alpha, beta):
        move_list = self.move_order_analysis(board, next_player)

        if board.checkmate(next_player) or board.stalemate(next_player) or depth == 0:
            return self.static_eval(board, next_player)

        else:
            if next_player == "white":
                best = -10000

                for score, move in move_list:
                    temp_board = copy.deepcopy(board)
                    piece = temp_board.squares[move.initial.row][move.initial.col].piece
                    temp_board.move(piece, move, testing=True)
                    val = self.minimax(temp_board, "black", depth - 1, alpha, beta)

                    if val > alpha and self.depth == depth:
                        self.best_move = move
                    best = max(best, val)
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        print("bad for black")
                        break

                return best
            else:
                best = 10000

                for score, move in move_list:
                    temp_board = copy.deepcopy(board)
                    piece = temp_board.squares[move.initial.row][move.initial.col].piece
                    temp_board.move(piece, move, testing=True)
                    val = self.minimax(temp_board, "white", depth - 1, alpha, beta)

                    if val < beta and self.depth == depth:
                        self.best_move = move
                    best = min(best, val)
                    beta = min(beta, val)

                    if beta <= alpha:
                        print("bad for white")
                        break

                return best








    def move_order_analysis(self, board, color):
        move_list = board.all_valid_move_list(color)
        priority_moves = []
        last_move = board.last_move
        last_moved_piece = board.squares[last_move.final.row][last_move.final.col].piece
        for move, piece in move_list:
            score = 0
            enemy_piece = board.squares[move.final.row][move.final.col].piece
            initial = (move.initial.row, move.initial.col)
            final = (move.final.row, move.final.col)
            initial = piece.position_value(initial[0], initial[1])
            final = piece.position_value(final[0], final[1])

            if final > initial:
                score += 5

            if enemy_piece:
                score += 100 * abs(enemy_piece.value) - 10 * abs(piece.value)
                if enemy_piece == last_moved_piece:
                    score += 1001

            if piece.name == "king" and abs(move.final.col - move.initial.col) == 2:
                score += 20

            priority_moves.append((score / 500, move))

        priority_moves.sort(key = lambda tup: tup[0], reverse=True)

        return priority_moves


    def static_eval(self, board, next_player):
        if board.checkmate(next_player):
            return 10000 if next_player == "black" else -10000
        elif board.stalemate(next_player):
            return 0
        else:
            s = 0
            for row in range(ROWS):
                for col in range(COLS):
                    if board.squares[row][col].piece != None:
                        p = board.squares[row][col].piece
                        if p.name == "knight":
                            p.k_position_value(row, col)
                        if p.name == "king":
                            p.ki_position_value(row, col)
                        if p.name == "pawn":
                            p.p_position_value(row, col)
                        if p.name == "bishop":
                            p.b_position_value(row, col)
                        if p.name == "rook":
                            p.r_position_value(row, col)
                        if p.name == "queen":
                            p.q_position_value(row, col)
                        s += p.value

            s = round(s, 2)
            if s == -0.0:
                s = 0.0
            return s
