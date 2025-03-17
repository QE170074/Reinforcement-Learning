import tkinter as tk
import time


class TicTacToe:
    def __init__(self, master, player1, player2):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.master.configure(bg="white")

        self.player_names = {"X": player1, "O": player2}
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_started = False  

        self.colors = {
            "X": "#FF5733", 
            "O": "#33FF57", 
            "bg": "#E6E6FA", 
            "highlight": "#FFD700", 
            "win": "#40E0D0"
        }

        # Tiêu đề
        self.label = tk.Label(master, text="Tic-Tac-Toe", font=("Arial", 24, "bold"), bg="white", fg="black")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Hiển thị lượt chơi
        self.turn_label = tk.Label(master, text="Game Starting Soon...", font=("Arial", 16), bg="white", fg="black")
        self.turn_label.grid(row=1, column=0, columnspan=3, pady=5)

        # Bảng trò chơi
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(master, text="", font=("Arial", 40, "bold"), width=6, height=2, bg=self.colors["bg"],
                                relief="raised", command=lambda i=i, j=j: self.on_click(i, j), state="disabled")
                btn.grid(row=i + 2, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        # Bắt đầu hiệu ứng đếm ngược
        self.master.after(500, self.start_countdown, 3)  

    def start_countdown(self, count):
        if count > 0:
            self.turn_label.config(text=f"Starting in {count}...", fg="#FF4500")
            self.master.after(1000, self.start_countdown, count - 1)  
        else:
            self.turn_label.config(text=f"{self.player_names['X']}'s Turn", fg=self.colors["X"])
            self.enable_buttons()
            self.game_started = True

    def enable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="normal")

    def on_click(self, i, j):
        if self.game_started and self.board[i][j] == "":
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player, state="disabled",
                                      disabledforeground=self.colors[self.current_player], relief="sunken")

            if self.check_winner():
                self.animate_winner()
                self.show_winner_screen()
            elif self.check_tie():
                self.show_tie_screen()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.turn_label.config(text=f"{self.player_names[self.current_player]}'s Turn", fg=self.colors[self.current_player])

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                return True

        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != "":
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True

        return False

    def check_tie(self):
        return all(cell != "" for row in self.board for cell in row)

    def animate_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                for j in range(3):
                    self.flash_winner(i, j)
                return

        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != "":
                for i in range(3):
                    self.flash_winner(i, j)
                return

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            for i in range(3):
                self.flash_winner(i, i)
            return

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            for i in range(3):
                self.flash_winner(i, 2 - i)
            return

    def flash_winner(self, i, j):
        for _ in range(3):
            self.buttons[i][j].config(bg="gold")
            self.master.update()
            time.sleep(0.2)
            self.buttons[i][j].config(bg=self.colors["win"])
            self.master.update()
            time.sleep(0.2)

    def show_winner_screen(self):
        win_popup = tk.Toplevel(self.master)
        win_popup.title("Game Over")
        win_popup.geometry("300x200")
        win_popup.configure(bg="white")

        win_label = tk.Label(win_popup, text=f"🎉 {self.player_names[self.current_player]} Wins! 🎉", 
                             font=("Arial", 16, "bold"), bg="white", fg=self.colors[self.current_player])
        win_label.pack(pady=20)

        restart_button = tk.Button(win_popup, text="Play Again", font=("Arial", 14), 
                                   bg="#008080", fg="white", command=lambda: [win_popup.destroy(), self.reset_game()])
        restart_button.pack(pady=5)

        quit_button = tk.Button(win_popup, text="Quit", font=("Arial", 14), 
                                bg="#8B0000", fg="white", command=self.master.quit)
        quit_button.pack(pady=5)

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.turn_label.config(text=f"{self.player_names['X']}'s Turn", fg=self.colors["X"])
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", bg=self.colors["bg"], relief="raised")

        self.game_started = False
        self.master.after(500, self.start_countdown, 3)

def main():
    root = tk.Tk()
    game = TicTacToe(root, "Player X", "Player O")
    root.mainloop()

if __name__ == "__main__":
    main()
