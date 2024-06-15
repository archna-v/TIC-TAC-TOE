class Player:
    def __init__(self, name=None, symbol=None):
        self.name = name
        self.symbol = symbol

    def set_player_name_and_symbol(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_player_name_and_symbol(self):
        return self.name, self.symbol
