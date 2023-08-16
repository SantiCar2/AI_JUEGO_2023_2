import tkinter as tk
import numpy as np
import random
import pygame
import sys
import math

class DifficultySelection:
    def __init__(self, root):
        self.root = root
        self.root.title("Seleccionar Dificultad")
        self.root.geometry("500x400")
        
        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(pady=20)

        tk.Label(self.difficulty_frame, text="Selecciona la Dificultad:", font=("Helvetica", 20)).pack(pady=20)

        self.selected_difficulty = tk.StringVar()
        self.selected_difficulty.set("Fácil")

        difficulty_options = ["Fácil", "Intermedio", "Difícil"]

        for difficulty in difficulty_options:
            tk.Radiobutton(self.difficulty_frame, text=difficulty, variable=self.selected_difficulty,
               value=difficulty, font=("Arial", 16), fg="black").pack(anchor=tk.W)

        tk.Button(self.root, text="Empezar Juego", command=self.start_game, font=("Arial", 16)).pack(pady=(20, 15))

    def start_game(self):
        selected_difficulty = self.selected_difficulty.get()
        self.root.destroy()  # Cerrar la ventana de selección de dificultad
        start_pygame_game(selected_difficulty)  # Iniciar el juego de Pygame

def start_pygame_game(difficulty):
    pygame.init()

    Table = (255, 51, 255)
    Casillas = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)



    ROW_NUMB = 6
    COLUM_NUMB = 7
    game_over = False

    MAX = 0
    MIN = 1

    EMPTY = 0
    MAX_PIECE = 1
    MIN_PIECE = 2

    WINDOW_LENGTH = 4


    def create_board():
        board = np.zeros((ROW_NUMB, ROW_NUMB))
        return board


    def drop_piece(board, row, col, piece):
        board[row][col] = piece


    def is_valid_location(board, col):
        return board[ROW_NUMB - 1][col] == 0


    def get_next_open_row(board, col):
        for r in range(ROW_NUMB):
            if board[r][col] == 0:
                return r


    def print_board(board):
        print(np.flip(board, 0))


    def winning_move(board, piece):
        # VERIFICAR COLUM
        for c in range(ROW_NUMB - 3):
            for r in range(ROW_NUMB):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True

        # VERIFICAL FILAS
        for c in range(ROW_NUMB):
            for r in range(ROW_NUMB - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    return True

        # VERIFICAR DIAGONALES
        for c in range(ROW_NUMB - 3):
            for r in range(ROW_NUMB - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                    c + 3] == piece:
                    return True


    def evaluate_window(window, piece):
        score = 0
        opp_piece = MAX_PIECE
        if piece == MAX_PIECE:
            opp_piece = MIN_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score


    def score_position(board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, ROW_NUMB // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(ROW_NUMB):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(ROW_NUMB - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        ## Score Vertical
        for c in range(ROW_NUMB):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_NUMB - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_NUMB - 3):
            for c in range(ROW_NUMB - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        for r in range(ROW_NUMB - 3):
            for c in range(ROW_NUMB - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        return score



    def get_valid_locations(board):
        valid_locations = []
        for col in range(ROW_NUMB):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def draw_board(board):
        for c in range(ROW_NUMB):
            for r in range(ROW_NUMB):
                pygame.draw.rect(screen, Table, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, Casillas, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(ROW_NUMB):
            for r in range(ROW_NUMB):
                if board[r][c] == MAX_PIECE:
                    pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif board[r][c] == MIN_PIECE:
                    pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()


    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()

    SQUARESIZE = 100

    width = ROW_NUMB * SQUARESIZE
    height = (ROW_NUMB + 1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(MAX, MIN)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, Casillas, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == MAX:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, Casillas, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for MAX 1 Input
                if turn == MAX:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, MAX_PIECE)

                        if winning_move(board, MAX_PIECE):
                            label = myfont.render("MAX 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        
        if game_over:
            pygame.time.wMINt(3000)

    game_screen(difficulty)

    pygame.quit()
    sys.exit()

def game_screen(difficulty):
    # Coloca aquí el código relacionado con la pantalla del juego, utilizando la dificultad seleccionada
    # Este sería el bucle principal donde se juega el juego
    p=100

def main():
    root = tk.Tk()
    app = DifficultySelection(root)
    root.mainloop()

if __name__ == "__main__":
    main()