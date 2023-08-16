import tkinter as tk
import numpy as np
import random
import pygame
import sys
import math

class DifficultySelection():
    
    def __init__(self, root):
        self.root = root
        self.root.title("Conecta 4")
        self.root.geometry("500x400")
        
        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(pady=20)

        tk.Label(self.difficulty_frame, text="Selecciona la dificultad: ", font=("Helvetica", 20)).pack(pady=20)

        self.selected_difficulty = tk.StringVar()
        self.selected_difficulty.set("Fácil")

        difficulty_options = ["Fácil", "Intermedio", "Difícil"]

        for difficulty in difficulty_options:
            tk.Radiobutton(self.difficulty_frame, text=difficulty, variable=self.selected_difficulty,
               value=difficulty, font=("Arial", 16), fg="black").pack(anchor=tk.W)

        tk.Button(self.root, text="Empezar partida", command=self.start_game, font=("Arial", 16)).pack(pady=(20, 15))

    def start_game(self):
        selected_difficulty = self.selected_difficulty.get()
        self.root.destroy()  # Cerrar la ventana de selección de dificultad
        start_pygame_game(selected_difficulty)  # Iniciar el juego de Pygame

def start_pygame_game(difficulty):
    pygame.init()

    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)

    RED = (255, 0, 0)
    GREEN = (255, 255, 0)

    ROW_NUMB = 5
    COLUMN_NUMB = 6

    game_over = False
    
    MAX = 0
    MIN = 1
    
    EMPTY = 0
    MAX_PIECE = 1
    MIN_PIECE = 2

    WINDOW_LENGTH = 4


    def new_board():
        board = np.zeros((ROW_NUMB, COLUMN_NUMB))
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
        # VERIFY COLUMN FOR WIN
        for c in range(COLUMN_NUMB - 3):
            for r in range(ROW_NUMB):
                if (board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece):
                    return True

        # VERIFY ROW FOR WIN
        for c in range(COLUMN_NUMB):
            for r in range(ROW_NUMB - 3):
                if (board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece):
                    return True

        # VERIFY DIAGONALS FOR WIN
        for c in range(COLUMN_NUMB - 3):
            for r in range(ROW_NUMB - 3):
                if (board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece):
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
        center_array = [int(i) for i in list(board[:, COLUMN_NUMB // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(ROW_NUMB):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_NUMB - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMN_NUMB):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_NUMB - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_NUMB - 3):
            for c in range(COLUMN_NUMB - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        for r in range(ROW_NUMB - 3):
            for c in range(COLUMN_NUMB - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        return score

    def is_terminal_node(board):
        return (
            winning_move(board, MAX_PIECE)
            or winning_move(board, MIN_PIECE)
            or len(get_valid_locations(board)) == 0
        )

    def minimax(board, depth, alpha, beta, maximizingPlayer):
        valid_locations = get_valid_locations(board)
        is_terminal = is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, MIN_PIECE):
                    return (None, 100000000000000)
                elif winning_move(board, MAX_PIECE):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, score_position(board, MIN_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, MIN_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, MAX_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
    
    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_NUMB):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations
    

    def pick_best_move(board, piece):
        valid_locations = get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, piece)
            score = score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col
        return best_col

    def draw_board(board):
        for c in range(COLUMN_NUMB):
            for r in range(ROW_NUMB):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(COLUMN_NUMB):
            for r in range(ROW_NUMB):
                if board[r][c] == MAX_PIECE:
                    pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif board[r][c] == MIN_PIECE:
                    pygame.draw.circle(screen, GREEN, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()


    board = new_board()
    print_board(board)
    game_over = False

    pygame.init()

    SQUARESIZE = 100

    width = COLUMN_NUMB * SQUARESIZE
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
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == MAX:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for MAX 1 Input
                if turn == MAX:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, MAX_PIECE)

                        if winning_move(board, MAX_PIECE):
                            label = myfont.render("MAX 1 wins! :)", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        if game_over:
            pygame.time.wMINt(3000)


    # game_screen(difficulty)
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