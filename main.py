import pygame
import sys

import pygame.display
from constants import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def main_loop(self):
        ai_game = input("Play against a bot? (y/n): ")
        url = OPENING

        game = self.game
        screen = self._screen
        board = self.game.board
        dragger = self.game.dragger
        ai = self.game.ai
        book = board.book

        if "y" in ai_game.lower():
            game.ai_game = True

        
        while True:
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_move(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            if not game.player_turn and not board.over:
                game.show_last_move(screen)
                game.show_pieces(screen)
                pygame.display.update()
                if book.move_number < 3:
                    last_move_notation = board.move_to_string()
                    ai_move, board.url = book.opening_moves(last_move_notation, board.url)
                    ai.best_move = board.string_to_move(game, ai_move)
                    piece, ai_move = ai.best_move
                else:
                    ai.minimax(board, game.next_player, 2, -10000, 10000)
                    ai_move = ai.best_move

                if ai_move is None:
                    ai_move = ai.random_move(board, game.next_player)
                piece = board.squares[ai_move.initial.row][ai_move.initial.col].piece
                captured = board.squares[ai_move.final.row][ai_move.final.col].has_piece()
                game.sound_effect(captured)

                board.set_false_en_passant()
                board.move(piece, ai_move, testing=False, ai=True)
                ai.best_move = None
                game.show_last_move(screen)
                game.show_pieces(screen)
                game.next_turn()
                pygame.display.update()

                if board.last_move:
                    str = board.move_to_string()
                    board.url = board.book.opening_moves(str, board.url)[1]


            for event in pygame.event.get():
                # click
                if event.type == pygame.MOUSEBUTTONDOWN and game.player_turn:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            game.show_background(screen)
                            game.show_move(screen)
                            game.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_move(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP and game.player_turn:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        possible_move = Move(initial, final)

                        if board.valid_move(dragger.piece, possible_move):
                            # checks if open square (normal capture)
                            captured = board.squares[released_row][released_col].has_piece()
                            game.sound_effect(captured)

                            board.set_false_en_passant()
                            board.move(dragger.piece, possible_move)
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()



                    dragger.undrag_piece()

                    if board.checkmate(game.next_player):
                        color_win = "white" if game.next_player == "black" else "black"
                        print(color_win + " has won by checkmate!")
                        break
                    elif board.stalemate(game.next_player):
                        print("Drawn by stalemate!")
                        break


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()

                    elif event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                    elif event.key == pygame.K_c:
                        print(game.next_player)
                        print(board.checkmate(game.next_player))

                    elif event.key == pygame.K_s:
                        p1, m1 = ai.string_to_move(game, board, "O-O-O")
                        board.move(p1, m1)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_pieces(screen)
                        game.next_turn()
                    elif event.key == pygame.K_e:
                        nota = ai.move_to_string(board)
                        ai.opening_moves(board, None, nota)


                    elif event.key == pygame.K_u:
                        last_move = board.last_move
                        p = board.squares[last_move.final.row][last_move.final.col].piece
                        board.undo_move(p,last_move)
                        game.next_turn()


                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



            pygame.display.update()




main = Main()
main.main_loop()