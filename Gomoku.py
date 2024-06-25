import copy
import tkinter as tk
from tkinter import messagebox

class Gomoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku")
        
        self.main_menu()

    def main_menu(self):
        self.clear_frame()
        
        label = tk.Label(self.root, text="Welcome to Gomoku", font=("Arial", 24))
        label.pack(pady=20)
        
        new_game_btn = tk.Button(self.root, text="New Game", command=self.new_game_menu, font=("Arial", 18))
        new_game_btn.pack(pady=10)
        
        exit_btn = tk.Button(self.root, text="Exit", command=self.root.quit, font=("Arial", 18))
        exit_btn.pack(pady=10)

    def new_game_menu(self):
        self.clear_frame()

        label = tk.Label(self.root, text="Choose Mode", font=("Arial", 24))
        label.pack(pady=20)

        single_player_btn = tk.Button(self.root, text="Single Player", command=self.start_single_player, font=("Arial", 18))
        single_player_btn.pack(pady=10)

        two_player_btn = tk.Button(self.root, text="Two Players", command=self.start_two_players, font=("Arial", 18))
        two_player_btn.pack(pady=10)

        back_btn = tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, font=("Arial", 18))
        back_btn.pack(pady=10)

    def start_single_player(self):
        self.start_game(single_player=True)

    def start_two_players(self):
        self.start_game(single_player=False)

    def start_game(self, single_player):
        self.clear_frame()
        self.single_player = single_player
        self.current_player = "X"
        
        self.board = [["" for _ in range(15)] for _ in range(15)]
        self.buttons = [[None for _ in range(15)] for _ in range(15)]

        board_frame = tk.Frame(self.root)
        board_frame.pack()

        for i in range(15):
            for j in range(15):
                btn = tk.Button(board_frame, text="", width=3, height=1, font=("Arial", 18),
                                command=lambda i=i, j=j: self.make_move(i, j))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        back_btn = tk.Button(self.root, text="Back to Main Menu", command=self.confirm_exit, font=("Arial", 18))
        back_btn.pack(pady=10)

    def make_move(self, i, j):
        if self.board[i][j] == "":
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player)
            if self.check_winner(i, j):
                self.end_game(f"Player {self.current_player} wins!")
            elif all(self.board[i][j] != "" for i in range(15) for j in range(15)):
                self.end_game("It's a tie!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.single_player and self.current_player == "O":
                    self.computer_move()

    def computer_move(self):
        def evaluate_line(x, y, dx, dy, player):
            count = 0
            for step in range(1, 5):
                nx, ny = x + step * dx, y + step * dy
                if 0 <= nx < 15 and 0 <= ny < 15:
                    if self.board[nx][ny] == player:
                        count += 1
                    else:
                        break
                else:
                    break
            return count

        def get_score(x, y, player):
            directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
            score = 0
            for dx, dy in directions:
                count = evaluate_line(x, y, dx, dy, player) + evaluate_line(x, y, -dx, -dy, player)
                if count >= 4:
                    score += 10000  # 即時獲勝或阻止對方獲勝
                elif count == 3:
                    score += 1000   # 準備形成四連
                elif count == 2:
                    score += 100    # 準備形成三連
            return score

        def find_best_move():
            best_score = -1
            best_move = None
            for i in range(15):
                for j in range(15):
                    if self.board[i][j] == "":
                        attack_score = get_score(i, j, "O")
                        defense_score = get_score(i, j, "X")
                        move_score = max(attack_score, defense_score)
                        if move_score > best_score:
                            best_score = move_score
                            best_move = (i, j)
            return best_move

        move = find_best_move()
        if move:
            self.make_move(*move)
        else:
            # Fallback to random move if no best move found (should not happen)
            import random
            empty_cells = [(i, j) for i in range(15) for j in range(15) if self.board[i][j] == ""]
            move = random.choice(empty_cells)
            self.make_move(*move)

    def check_winner(self, x, y):
        def check_line(start_x, start_y, dx, dy):
            count = 0
            for step in range(-4, 5):
                nx, ny = start_x + step * dx, start_y + step * dy
                if 0 <= nx < 15 and 0 <= ny < 15 and self.board[nx][ny] == self.current_player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
            return False

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        return any(check_line(x, y, dx, dy) for dx, dy in directions)

    def end_game(self, message):
        if messagebox.askyesno("Game Over", message + " Do you want to play again?"):
            self.new_game_menu()
        else:
            self.main_menu()

    def confirm_exit(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit to main menu? The current game will be lost."):
            self.main_menu()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = Gomoku(root)
    root.mainloop()
