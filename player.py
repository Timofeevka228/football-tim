class Player:
    def __init__(self, name, level, energy, price):
        self.name = name
        self.level = level
        self.energy = energy
        self.price = price

    def get_data(self):
        return [self.name, str(self.level), str(self.energy)]

class User:
    def __init__(self, name, money, trophy, number_players, increase):
        self.name = name
        self.money = money
        self.trophy = trophy
        self.number_players = number_players
        self.increase = increase

    def get_data(self):
        return [self.name, self.money, self.trophy, self.number_players]