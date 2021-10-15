from player import Player
from player import User

# Код для кнопки раздевалка

bonus_for_2lvl = -2
bonus_for_3lvl = -4


player1 = Player('Власов Максим', 1, 1000, 5000)
player2 = Player('Бенджамин Млинарж', 1, 3, 5000)
player3 = Player('Александр Титов', 1, 3, 5000)
player4 = Player('Артём Трифонов', 1, 3, 5000)
player5 = Player('Кристиан Либор', 1, 3, 5000)
player6 = Player('Силино Джордано', 1, 3, 5000)
player7 = Player('Энрико Ландино', 1, 3, 5000)
player8 = Player('Саммуель Тэйлор', 1, 3, 5000)
player9 = Player('Стивен Эдвардс', 1, 3, 5000)
player10 = Player('Майкл Сандерс', 1, 3, 5000)
player11 = Player('Джеймс Маккой', 1, 3, 5000)

players = [player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11]

# Код для кнопки профиль
user = User("user", 3000, 0, len(players), 500)
