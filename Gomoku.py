import copy
import tkinter as tk
from tkinter import messagebox

class Gomoku:
    def __init__(self, root):
        # 初始化遊戲
        self.root = root
        self.root.title("五子棋")
        
        # 顯示主選單
        self.main_menu()

    def main_menu(self):
        # 清空目前的視窗內容並顯示主選單
        self.clear_frame()
        
        label = tk.Label(self.root, text="歡迎來到五子棋", font=("Arial", 24))
        label.pack(pady=20)
        
        new_game_btn = tk.Button(self.root, text="新遊戲", command=self.new_game_menu, font=("Arial", 18))
        new_game_btn.pack(pady=10)
        
        exit_btn = tk.Button(self.root, text="離開", command=self.root.quit, font=("Arial", 18))
        exit_btn.pack(pady=10)

    def new_game_menu(self):
        # 顯示新遊戲選單
        self.clear_frame()

        label = tk.Label(self.root, text="選擇模式", font=("Arial", 24))
        label.pack(pady=20)

        single_player_btn = tk.Button(self.root, text="單人遊戲", command=self.start_single_player, font=("Arial", 18))
        single_player_btn.pack(pady=10)

        two_player_btn = tk.Button(self.root, text="雙人遊戲", command=self.start_two_players, font=("Arial", 18))
        two_player_btn.pack(pady=10)

        back_btn = tk.Button(self.root, text="返回主選單", command=self.main_menu, font=("Arial", 18))
        back_btn.pack(pady=10)

    def start_single_player(self):
        # 開始單人遊戲
        self.start_game(single_player=True)

    def start_two_players(self):
        # 開始雙人遊戲
        self.start_game(single_player=False)

    def start_game(self, single_player):
        # 開始遊戲並初始化棋盤
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

        back_btn = tk.Button(self.root, text="返回主選單", command=self.confirm_exit, font=("Arial", 18))
        back_btn.pack(pady=10)

    def make_move(self, i, j):
        # 進行玩家的移動
        if self.board[i][j] == "":
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player)
            if self.check_winner(i, j):
                self.end_game(f"玩家 {self.current_player} 勝利!")
            elif all(self.board[i][j] != "" for i in range(15) for j in range(15)):
                self.end_game("平局!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.single_player and self.current_player == "O":
                    self.computer_move()

    def computer_move(self):
        # 計算電腦的最佳移動
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
            # 若未找到最佳移動則隨機移動（理論上不應發生）
            import random
            empty_cells = [(i, j) for i in range(15) for j in range(15) if self.board[i][j] == ""]
            move = random.choice(empty_cells)
            self.make_move(*move)

    def check_winner(self, x, y):
        # 檢查是否有玩家勝利
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
        # 結束遊戲並詢問是否重新開始
        if messagebox.askyesno("遊戲結束", message + " 是否要再玩一次?"):
            self.new_game_menu()
        else:
            self.main_menu()

    def confirm_exit(self):
        # 確認是否退出到主選單
        if messagebox.askyesno("確認退出", "確定要返回主選單嗎? 當前遊戲將會丟失。"):
            self.main_menu()

    def clear_frame(self):
        # 清空目前的視窗內容
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = Gomoku(root)
    root.mainloop()
