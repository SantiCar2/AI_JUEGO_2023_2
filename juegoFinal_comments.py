# Import libraries
import numpy as np
import random
import pygame
import sys
import math
import tkinter as tk


class DifficultySelection:
    def __init__(self, root):
        # Initialize the main GUI window
        self.root = root
        self.root.title("Conecta 4") # Title of the window
        self.root.geometry("500x400") # Dimensions of the window

        # Create a framework for difficulty selection
        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(pady=20) # Add a spacer margins

        # Label to show difficulty selection instructions
        tk.Label(
            self.difficulty_frame,
            text="Selecciona la dificultad: ",
            font=("Helvetica", 20),
        ).pack(pady=20) # Add a spacer margins

        # Variable to store selected difficulty
        self.selected_difficulty = tk.StringVar()
        self.selected_difficulty.set("Fácil") # Set the default difficulty

        # Difficulty options available
        difficulty_options = ["Fácil", "Intermedio", "Difícil"]

        # Create a radio button for each difficulty option
        for difficulty in difficulty_options:
            tk.Radiobutton(
                self.difficulty_frame,
                text=difficulty,
                variable=self.selected_difficulty,
                value=difficulty,
                font=("Arial", 16),
                fg="black",
            ).pack(anchor=tk.W)

        # Button to start the game
        tk.Button(
            self.root,
            text="Empezar partida",
            command=self.start_game,
            font=("Arial", 16),
        ).pack(pady=(20, 15))


    def start_game(self):
        selected_difficulty = self.selected_difficulty.get()
        self.root.destroy()  # Close the difficulty selection window
        start_pygame_game(selected_difficulty)  # Start the game of Pygame


def start_pygame_game(selected_difficulty):
    # Define difficulties in terms of opponent’s search levels
    difficulty = [1, 3, 5]

    # Define colors used in the game
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    # Define board dimensions
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    # Define identifiers for players
    PLAYER = 0
    AI = 1

    # Define identifiers for pieces on the board
    EMPTY = 0
    PLAYER_PIECE = 1
    AI_PIECE = 2

    # Define the length required to win (connect) in the game
    WINDOW_LENGTH = 4

    # Size of each square on the board
    SQUARESIZE = 100

    # Calculate the total size of the game window
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    size = (width, height)

    # Circle radius in each board cell
    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size)


    # Function to create an empty game board
    def create_board():
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board


    # Function to drop a game piece onto the board
    def drop_piece(board, row, col, piece):
        board[row][col] = piece


    # Function to check if a column is a valid location to place a game piece
    def is_valid_location(board, col):
        return board[ROW_COUNT - 1][col] == 0


    # Function to get the next open row in a column
    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r


    # Function to print the game board (flipped vertically for better visualization)
    def print_board(board):
        print(np.flip(board, 0))


    # Function to check if a player has won with a certain game piece
    def winning_move(board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if (
                    board[r][c] == piece
                    and board[r][c + 1] == piece
                    and board[r][c + 2] == piece
                    and board[r][c + 3] == piece
                ):
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if (
                    board[r][c] == piece
                    and board[r + 1][c] == piece
                    and board[r + 2][c] == piece
                    and board[r + 3][c] == piece
                ):
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if (
                    board[r][c] == piece
                    and board[r + 1][c + 1] == piece
                    and board[r + 2][c + 2] == piece
                    and board[r + 3][c + 3] == piece
                ):
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if (
                    board[r][c] == piece
                    and board[r - 1][c + 1] == piece
                    and board[r - 2][c + 2] == piece
                    and board[r - 3][c + 3] == piece
                ):
                    return True


    # Function to evaluate a window of consecutive pieces on the board
    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 4:
            score += 100 # Highest score for winning position
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5 # Moderate score for potential winning move
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2 # Lower score for setting up future winning moves

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4 # Penalize opponent's potential winning move

        return score


    # Function to score a position on the board for a given player's piece
    def score_position(board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        print(f"HOLA: {center_array}")
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c : c + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r : r + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score posiive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        # Score negatively sloped diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        return score


    # Function to check if the current state is a terminal node (end of the game)
    def is_terminal_node(board):
        return (
            winning_move(board, PLAYER_PIECE)
            or winning_move(board, AI_PIECE)
            or len(get_valid_locations(board)) == 0
        )


    # Minimax algorithm implementation for game AI decision-making
    def minimax(board, depth, alpha, beta, maximizingPlayer):
        valid_locations = get_valid_locations(board)
        is_terminal = is_terminal_node(board)

        # Base cases for recursion
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, AI_PIECE):
                    return (None, 100000000000000)
                elif winning_move(board, PLAYER_PIECE):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, score_position(board, AI_PIECE))
        
        # Maximizer's turn
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        # Minimizer's turn
        else:  
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value


    # Function to get valid locations for placing a game piece
    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations


    # Function to pick the best move for the AI using minimax with alpha-beta pruning
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


    # Function to draw the game board with player and AI pieces
    def draw_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (
                        c * SQUARESIZE,
                        r * SQUARESIZE + SQUARESIZE,
                        SQUARESIZE,
                        SQUARESIZE,
                    ),
                )
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == PLAYER_PIECE:
                    pygame.draw.circle(
                        screen,
                        RED,
                        (
                            int(c * SQUARESIZE + SQUARESIZE / 2),
                            height - int(r * SQUARESIZE + SQUARESIZE / 2),
                        ),
                        RADIUS,
                    )
                elif board[r][c] == AI_PIECE:
                    pygame.draw.circle(
                        screen,
                        YELLOW,
                        (
                            int(c * SQUARESIZE + SQUARESIZE / 2),
                            height - int(r * SQUARESIZE + SQUARESIZE / 2),
                        ),
                        RADIUS,
                    )
        pygame.display.update()

    # Determine the difficulty level index and print the corresponding value
    diff_index = ["Fácil", "Intermedio", "Difícil"].index(selected_difficulty)
    print(difficulty[diff_index])

    # Create an empty game board
    board = create_board()
    print_board(board)
    game_over = False

    # Initialize pygame
    pygame.init()

    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    # Randomly choose which player starts the game
    turn = random.randint(PLAYER, AI)

    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                # Ask for Player 1 Input
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 wins! :)", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        # AI's turn
        if turn == AI and not game_over:
            col, minimax_score = minimax(
                board, difficulty[diff_index], -math.inf, math.inf, True
            )

            if is_valid_location(board, col):
                # pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 wins! :)", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000) # Pause for a few seconds after game over


if __name__ == "__main__":
    root = tk.Tk() # Create a Tkinter root window
    app = DifficultySelection(root) # Create an instance of the DifficultySelection class
    root.mainloop() # Start the main event loop to handle user interface interactions