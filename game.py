class Game:
    def __init__(self, players, board):
        self.players = players
        self.board = board
        self.current_player = 0

    def get_current_player(self):
        return self.players[self.current_player]

    def make_move(self, x, y):
        player = self.get_current_player()
        if self.board.make_move(x, y, player.symbol):
            if self.board.check_winner(player.symbol):
                return f"{player.name} wins!"
            elif self.board.is_full():
                return "The game is a draw!"
            self.current_player = 1 - self.current_player
            return None
        else:
            return "This move is not valid, try again."
