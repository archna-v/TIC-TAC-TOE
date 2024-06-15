import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from board import Board
from game import Game
from player import Player
import mysql.connector
from ttkthemes import ThemedTk
import requests
from io import BytesIO

class TicTacToeUI:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("Tic Tac Toe")

        # Set initial window size
        self.root.geometry("400x550")

        # Set background color
        self.root.configure(bg="#2C3E50")

        # Load background image
        image_url = "https://wallpapertag.com/wallpaper/full/2/9/9/313123-clouds-background-2880x1800-lockscreen.jpg"
        response = requests.get(image_url)
        image_data = response.content
        self.bg_image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))

        # Create a Canvas widget to place the background image
        self.canvas = tk.Canvas(self.root, width=400, height=550)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Database connection details (replace with your own)
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "20-Nov-04"
        self.db_name = "tictactoe_db"

        self.players = [self.create_player(1), self.create_player(2)]
        self.board = Board(3, '-')
        self.game = Game(self.players, self.board)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_title()
        self.create_board()
        self.winner_label = self.create_winner_label()
        self.play_again_frame = self.create_play_again_frame()
        
        # Start animations
        self.animate_title()

    def create_title(self):
        self.title = tk.Label(self.root, text="Tic Tac Toe", font=("Helvetica", 28, "bold"), bg="#2C3E50", fg="#ECF0F1")
        self.title_window = self.canvas.create_window(200, 40, window=self.title, anchor="center")

    def store_game_results(self, winner):
        try:
            connection = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            cursor = connection.cursor()

            player1 = self.players[0]
            player2 = self.players[1]
            winner_name = winner if winner != "Draw" else "Draw"

            insert_query = """
                INSERT INTO game_results (player1_name, player1_symbol, player2_name, player2_symbol, winner)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (player1.name, player1.symbol, player2.name, player2.symbol, winner_name))
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Database Info", "Game results stored successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def create_winner_label(self):
        self.winner_label = tk.Label(self.root, text="", font=("Helvetica", 16, "bold"), bg="#2C3E50", fg="#E74C3C")
        self.winner_label_window = self.canvas.create_window(200, 100, window=self.winner_label, anchor="center")
        return self.winner_label

    def create_player(self, player_number):
        name = input(f"Please enter the name of Player {player_number}: ")
        symbol = input(f"Please enter the symbol of Player {player_number}: ")
        return Player(name, symbol)

    def create_board(self):
        self.board_frame = tk.Frame(self.root, bg="#2C3E50")
        self.board_frame_window = self.canvas.create_window(200, 275, window=self.board_frame, anchor="center")
        for x in range(3):
            for y in range(3):
                button = tk.Button(self.board_frame, text='', font='Helvetica 20 bold', height=2, width=5,
                                   bg='#ECF0F1', fg='#E74C3C', activebackground='#BDC3C7', activeforeground='#E74C3C',
                                   command=lambda x=x, y=y: self.on_click(x, y))
                button.grid(row=x, column=y, padx=5, pady=5)
                self.buttons[x][y] = button

    def create_play_again_frame(self):
        self.play_again_frame = tk.Frame(self.root, bg="#2C3E50")
        tk.Label(self.play_again_frame, text="Play Again?", font="Helvetica 14 bold", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        yes_button = tk.Button(self.play_again_frame, text="Yes", font="Helvetica 14", bg='#2ECC71', fg='#ECF0F1', command=self.reset_board)
        yes_button.pack(side=tk.LEFT, padx=10)
        no_button = tk.Button(self.play_again_frame, text="No", font="Helvetica 14", bg='#E74C3C', fg='#ECF0F1', command=self.root.destroy)
        no_button.pack(side=tk.RIGHT, padx=10)
        self.play_again_frame_window = self.canvas.create_window(200, 500, window=self.play_again_frame, anchor="center")
        self.canvas.itemconfig(self.play_again_frame_window, state='hidden')
        return self.play_again_frame

    def on_click(self, x, y):
        result = self.game.make_move(x, y)
        self.update_board()
        if result:
            self.winner_label.config(text=result)
            self.store_game_results(result)
            self.canvas.itemconfig(self.play_again_frame_window, state='normal')

    def update_board(self):
        for x in range(3):
            for y in range(3):
                symbol = self.board.board[x][y]
                if symbol != '-':
                    self.buttons[x][y].config(text=symbol, state='disabled', disabledforeground='#E74C3C')
                else:
                    self.buttons[x][y].config(text=symbol, state='normal')

    def reset_board(self):
        self.board = Board(3, '-')
        self.game = Game(self.players, self.board)
        self.update_board()
        self.winner_label.config(text="")
        self.canvas.itemconfig(self.play_again_frame_window, state='hidden')

    def animate_title(self):
        def flash():
            current_color = self.title.cget("fg")
            next_color = "#ECF0F1" if current_color == "#E74C3C" else "#E74C3C"
            self.title.config(fg=next_color)
            self.root.after(500, flash)
        flash()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    TicTacToeUI().run()
