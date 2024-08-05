import pygame
from constants import *
from board import Board
from piece import *
from dragger import Dragger
from config import Config
from square import Square
from ai import AI
from opening_book import Book
class Game:

    def __init__(self):
        self.board = Board()
        self.hovered_square = None
        self.dragger = Dragger()
        self.next_player = "white"
        self.config = Config()
        self.ai = AI(2)
        self.player_turn = True
        self.ai_game = False


    # show methods
    def show_background(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for column in range(COLS):
                if (row + column) % 2 == 0:
                    color = theme.bg.light
                else:
                    color = theme.bg.dark
                rect = ((row * SQSIZE, column * SQSIZE), (SQSIZE, SQSIZE))
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if column == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    label = self.config.font.render(str(ROWS - row), 1, color)
                    label_pos = (5, 5 + row * SQSIZE)
                    surface.blit(label, label_pos)

                if row == 7:
                    color = theme.bg.light if column % 2 == 0 else theme.bg.dark
                    label = self.config.font.render(Square.get_alphacol(column), 1, color)
                    label_pos = ((column + 1) * SQSIZE - 20, 8 * SQSIZE - 20)
                    surface.blit(label, label_pos)


    def show_pieces(self, surface):
        board = self.board
        for row in range(ROWS):
            for column in range(COLS):
                if board.squares[row][column].has_piece():
                    piece = board.squares[row][column].piece

                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = column * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_move(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface,):
        if self.hovered_square:
            color = (180, 180, 180)
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods
    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"
        if self.ai_game:
            self.player_turn = False if self.player_turn is True else True

    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, capture=False):
        if capture:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()