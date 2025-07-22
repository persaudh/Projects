import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeReverseVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe: Reverse Mode")
        self.buttons = []
        self.board = [""] * 9
        self.reverse_index = random.randint(0, 8)
        self.current_player = "X"
        self.create_board()

    def create_board(self):
        self.status_label = tk.Label(self.root, text="Your Turn (X)", font=("Helvetica", 16))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        for i in range(9):
            btn = tk.Button(self.root, text="", font=("Helvetica", 24), width=5, height=2,
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=1 + i // 3, column=i % 3)
            self.buttons.append(btn)

    def make_move(self, index):
        if self.board[index] == "" and self.current_player == "X":
            if index == self.reverse_index:
                self.animate_reverse(index, "X")
            else:
                self.set_move(index, "X")
                self.after_move("X")

    def ai_move(self):
        move = self.find_best_move()
        if move is not None:
            if move == self.reverse_index:
                self.animate_reverse(move, "O", ai=True)
            else:
                self.set_move(move, "O")
                self.after_move("O")

    def set_move(self, index, player):
        self.board[index] = player
        self.buttons[index]["text"] = player
        self.buttons[index]["bg"] = "SystemButtonFace"

    def after_move(self, player):
        if self.check_winner(player):
            self.end_game("You win!" if player == "X" else "AI wins!")
        elif self.is_draw():
            self.end_game("It's a draw!")
        else:
            self.current_player = "O" if player == "X" else "X"
            self.status_label.config(text=f"{'AI' if self.current_player == 'O' else 'Your'} Turn ({self.current_player})")
            if self.current_player == "O":
                self.root.after(500, self.ai_move)

    def animate_reverse(self, index, player, ai=False):
        # Flash the button
        original_bg = self.buttons[index]["bg"]
        self.buttons[index]["bg"] = "red"
        self.root.update()
        self.root.after(300)

        reversed_player = "O" if player == "X" else "X"
        self.set_move(index, reversed_player)
        self.reverse_index = -1  # Deactivate the reverse trap
        self.status_label.config(text=f"Reverse! Switched to {reversed_player}'s piece")

        self.root.after(500, lambda: self.after_move(reversed_player))

    def find_best_move(self):
        # Try to win
        for i in range(9):
            if self.board[i] == "":
                symbol = "O" if i != self.reverse_index else "X"
                self.board[i] = symbol
                if self.check_winner(symbol):
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        # Block human
        for i in range(9):
            if self.board[i] == "":
                symbol = "X" if i != self.reverse_index else "O"
                self.board[i] = symbol
                if self.check_winner(symbol):
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        # Random move
        empty = [i for i, v in enumerate(self.board) if v == ""]
        return random.choice(empty) if empty else None

    def check_winner(self, player):
        combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(self.board[i] == player for i in combo) for combo in combos)

    def is_draw(self):
        return all(cell != "" for cell in self.board)

    def end_game(self, message):
        response = messagebox.askyesno("Game Over", f"{message}\nPlay again?")
        if response:
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", bg="SystemButtonFace")
        self.reverse_index = random.randint(0, 8)
        self.current_player = "X"
        self.status_label.config(text="Your Turn (X)")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeReverseVisual(root)
    root.mainloop()
