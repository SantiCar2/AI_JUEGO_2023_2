import tkinter as tk
from tkinter import messagebox
def dificult

class DifficultySelection:
    def __init__(self, root):
        self.root = root
        self.root.title("Seleccionar Dificultad")
        self.root.geometry("300x200")
        
        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(pady=20)

        tk.Label(self.difficulty_frame, text="Selecciona la Dificultad:", font=("Helvetica", 14)).pack()

        self.selected_difficulty = tk.StringVar()
        self.selected_difficulty.set("Fácil")

        difficulty_options = ["Fácil", "Intermedio", "Difícil"]

        for difficulty in difficulty_options:
            tk.Radiobutton(self.difficulty_frame, text=difficulty, variable=self.selected_difficulty,
                           value=difficulty).pack(anchor=tk.W)

        tk.Button(self.root, text="Empezar Juego", command=self.start_game).pack(pady=10)

    def start_game(self):
        selected_difficulty = self.selected_difficulty.get()
        print("Empezando juego con dificultad:", selected_difficulty)

if __name__ == "__main__":
    root = tk.Tk()
    app = DifficultySelection(root)
    root.mainloop()