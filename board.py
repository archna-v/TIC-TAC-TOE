class Board:
    def __init__(self, size, default_char):
        self.size = size
        self.default_char = default_char
        self.board = [[default_char for _ in range(size)] for _ in range(size)]

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def make_move(self, x, y, symbol):
        if self.board[x][y] == self.default_char:
            self.board[x][y] = symbol
            return True
        return False

    def check_winner(self, symbol):
        # Check rows
        for row in self.board:
            if all(s == symbol for s in row):
                return True

        # Check columns
        for col in range(self.size):
            if all(self.board[row][col] == symbol for row in range(self.size)):
                return True

        # Check diagonals
        if all(self.board[i][i] == symbol for i in range(self.size)):
            return True

        if all(self.board[i][self.size - i - 1] == symbol for i in range(self.size)):
            return True

        return False

    def is_full(self):
        return all(self.board[x][y] != self.default_char for x in range(self.size) for y in range(self.size))
