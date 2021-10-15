import telebot
from telebot import types
import settings
import random
import os

bot = telebot.TeleBot('1829054806:AAHhECi07Wo3tr2a0mqXAY1mEd9q8wjaWNw')

empty = types.ReplyKeyboardMarkup(True)
empty.row('     ')

mascott = 0
mascott_increase = 500
apply_increase = 0

id_list = []

players_menu = types.ReplyKeyboardMarkup(True)
players_menu.row('1', '2', '3', '4', '5')
players_menu.row('6', '7', '8', '9', '10')
players_menu.row('11', 'Выход🚪')

shop_menu = types.ReplyKeyboardMarkup(True)
shop_menu.row('Бутерброд🥪', 'Талисман🦄')
shop_menu.row('Игрок 1-го уровня ⬆️', 'Игрок 2-го уровня ⬆️')
shop_menu.row('Игрок 3-го уровня ⬆️', 'Выход🚪')

main_menu = types.ReplyKeyboardMarkup(True)
main_menu.row('Играть🎮', 'Раздевалка🧖‍♂️')
main_menu.row('ТОП🥇', 'Профиль👤')
main_menu.row('Магазин🛒')

start_menu = types.ReplyKeyboardMarkup(True)
start_menu.row('Придумать имя игровому профилю')

game_menu = types.ReplyKeyboardMarkup(True)
game_menu.row('◀️', '🔼', '▶️')

goalkeeper_menu = types.ReplyKeyboardMarkup(True)
goalkeeper_menu.row('1️⃣', '2️⃣')
goalkeeper_menu.row('3️⃣', '4️⃣')

choose_gm_menu = types.ReplyKeyboardMarkup(True)
choose_gm_menu.row('Чемпионат', 'Штрафные')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    file_name = './users/' + str(message.from_user.id) + '.txt'
    f = open(file_name, 'w')
    template = f'name,3000,0,1,0,0\n' \
               f'Власов Максим,1,3'
    f.write(template)
    f.close()
    print(file_name)
    bot.send_message(message.from_user.id,
                     f'Привет, {message.from_user.first_name}, у тебя есть возможность сыграть в игру про футбол ⚽️'
                     f' прямо тут, твоя задача участвовать в соревнованиях по футболу и зарабатывать как можно '
                     f'больше денег 💸 и трофеев 🏆. \n\nВ игре есть два режима игры: Чемпионат и Штрафные.\n\n'
                     f'В чемпионате тебенеобходимо подсказывать своему игроку куда пнуть мяч  и если его  не перехватят '
                     f'то вы проходите дальше если нет то вы вылетаете. В штрафных 3 этапап,'
                     f' тебе необходимо выбратьв какой угол твой игрок пнёт мяч, если вратарь его пропустит,'
                     f' то ты проходишь на следующийэтап, если мяч  ловят то ты вылетаешь'
                     f'У тебя есть возможность набрать в свою команду до 11 игроков и \n\n'
                     f'Изначально тебе будет выдан игрок 1 уровня и $3000\n'
                     f'Есть 3 уровня игроков : \n 1) 1 уровень - Новичок ($5000) \n '
                     f'2) 2 уровень - Любитель ($6500)\n 3) 3 уровень - Профессионал ($8000)\n\n'
                     f'Но не думай ты не сможешь играть одним футболистом всё время,'
                     f'у каждого игрока есть свой запас энергии он равен 3⚡️, '
                     f'но можно ускориить этот процесс купив бутерброд 🥪 за $1000 💸 который восстановит'
                     f' 1 единицу энергии.'
                     f'Зарабатывай трофеи и вырвись в топ по трофеям👊🏻!', reply_markup=start_menu)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text.lower()
    if text == 'играть🎮':
        user = get_data_settings(message, 1)
        bot.send_message(message.from_user.id, f'Привет, {user[0]}! '
                                               f'Выбери игрока, который будет участвовать! Введите номер игрока которого выбрали!')
        players = get_data_settings(message, 2)
        print()
        text = f'У вас есть {len(players)} игроков:\n'
        for i in range(len(players)):
            player = players[i].split(',')
            text += f'{i + 1} игрок {player[0]}, {player[1]} уровень, количество энергии: {player[2]}⚡️\n'
        bot.send_message(message.from_user.id, text, reply_markup=players_menu)
        bot.register_next_step_handler(message, get_player, players)
    elif text == 'раздевалка🧖‍♂️':
        players = get_data_settings(message, 2)
        text = f'У вас есть {len(players)} игроков:\n'
        for i in range(len(players)):
            player = players[i].split(',')
            text += f'{i + 1} игрок {player[0]}, {player[1]} уровень, энергия {player[2]}⚡️\n'
        bot.send_message(message.from_user.id, text)
    elif text == 'топ🥇':
        # bot.send_message(message.from_user.id, f'Данная функция ёщё не реализована')
        get_list_files(message)
    elif text == 'профиль👤':
        result = get_data_settings(message, 1)
        if not None:
            name, money, trophy, number_players, increase, mascott = result
            msct = 'имеется'
            if int(mascott) == 0:
                msct = 'отсутствует'
            text = f'Ваш профиль:\n\nНикнейм: {name}\nТрофеи {trophy}🏆\n' \
                   f'Мои игроки {number_players}🏋🏻‍♂️ \nБаланс ${money} 💸 \nТалисман {msct}'
            bot.send_message(message.from_user.id, text)
    elif text == 'магазин🛒':
        bot.send_message(message.from_user.id, f'Выбери то что хочешь купить на панели!', reply_markup=shop_menu)
        bot.register_next_step_handler(message, shop)
    elif text == 'придумать имя игровому профилю':
        bot.send_message(message.from_user.id, f'Теперь придумай имя для своего игрового профиля 🎮.')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, f'Такой команды нет 🤡')


def get_all_users_id():
    global id_list
    id_list = []
    for root, dirs, files in os.walk('./users'):
        for file in files:
            id_list.append(file.split('.')[0])


def get_name(message):
    name = message.text
    change_settings(message, 1, name)
    # settings.user.name = name
    bot.send_message(message.from_user.id, f'Имя успешно сохранено', reply_markup=main_menu)


def change_settings(message, action, arg=0, player_number=-1):
    data = []
    file_name = './users/' + str(message.from_user.id) + '.txt'
    with open(file_name, 'r') as f:
        for line in f:
            data.append(line.replace('\n', ''))
    if action == 1:  # изменить имя
        line = data[0].split(',')
        line[0] = str(arg)
        data[0] = ",".join(line)

    elif action == 2:  # добавить деньги на счёт
        line = data[0].split(',')
        new_value = int(line[1]) + int(arg)
        line[1] = str(new_value)
        data[0] = ",".join(line)

    elif action == 3:  # добавить трофей
        line = data[0].split(',')
        new_value = int(line[2]) + int(arg)
        line[2] = str(new_value)
        data[0] = ",".join(line)

    elif action == 4:  # добавить кол-во  игроков
        line = data[0].split(',')
        new_value = int(line[3]) + int(arg)
        line[3] = str(new_value)
        data[0] = ",".join(line)

    elif action == 5:  # изменить increase
        line = data[0].split(',')
        new_value = int(line[4]) + int(arg)
        line[4] = str(new_value)
        data[0] = ",".join(line)

    elif action == 6:  # изменить энергию игрока
        if player_number >= 0:
            line = data[player_number + 1].split(',')
            line[2] = str(int(line[2]) + int(arg))
            data[player_number + 1] = ','.join(line)

    elif action == 7:  # добавить талисман
        line = data[0].split(',')
        line[5] = '1'
        data[0] = ",".join(line)

    f = open(file_name, 'w')
    for line in data:
        f.write(line + '\n')
    f.close()


def get_data_settings(message, action):
    data = []
    file_name = './users/' + str(message.from_user.id) + '.txt'
    with open(file_name, 'r') as f:
        for line in f:
            data.append(line.replace('\n', ''))
    if action == 1:  # данные пользователя
        return data[0].split(',')
    elif action == 2:  # данные игроков
        if len(data) > 1:
            return data[1:]

    return None


def shop(message):
    text = message.text
    if text == 'Бутерброд🥪':
        bot.send_message(message.from_user.id, f'Напишите номер игрока который поучит бутерброд.')
        players = get_data_settings(message, 2)
        text = f'У вас есть {len(players)} игроков:\n'
        for i in range(len(players)):
            player = players[i].split(',')
            text += f'{i + 1} игрок {player[0]}, {player[1]} уровень, количество энергии: {player[2]}⚡️\n'
        bot.send_message(message.from_user.id, text, reply_markup=players_menu)
        bot.register_next_step_handler(message, buy_sandwich, players)
    elif text == 'Талисман🦄':
        bot.send_message(message.from_user.id, f'Талисман был куплен успешно!✅\n Теперь он улучшает игру вашей команды'
                                               f'', reply_markup=main_menu)

        global mascott
        mascott = 1
        change_settings(message, 2, -3000)
        change_settings(message, 7)

    elif (text == 'Игрок 1-го уровня ⬆️' or text == 'Игрок 2-го уровня ⬆️' or text == 'Игрок 3-го уровня ⬆️'):
        if int(get_data_settings(message, 1)[3]) <= 10:
            check = False
            level = ''
            if text == 'Игрок 1-го уровня ⬆️' and int(get_data_settings(message, 1)[1]) >= 5000:
                change_settings(message, 2, -5000)
                check = True
                level = '1'
            elif text == 'Игрок 2-го уровня ⬆️' and int(get_data_settings(message, 1)[1]) >= 6500:
                change_settings(message, 2, -6500)
                check = True
                level = '2'
            elif text == 'Игрок 3-го уровня ⬆️' and int(get_data_settings(message, 1)[1]) >= 8000:
                change_settings(message, 2, -8000)
                check = True
                level = '3'
            else:
                bot.send_message(message.from_user.id,
                                 f'У вас не хватает денег на покупку!❌', reply_markup=main_menu)
            if check:
                count = int(get_data_settings(message, 1)[3])
                new_player = settings.players[count].get_data()
                new_player[1] = level
                new_player = ','.join(new_player)
                file_name = './users/' + str(message.from_user.id) + '.txt'
                f = open(file_name, 'a')
                f.write(new_player + '\n')
                f.close()
                bot.send_message(message.from_user.id,
                                 f'Игрок {level}-го уровня был куплен успешно!✅\n Теперь он находится в раздевалке'
                                 f'', reply_markup=main_menu)
                change_settings(message, 4, 1)
        else:
            bot.send_message(message.from_user.id, f'У вас уже достаточное количество  игроков⚽️'
                             , reply_markup=main_menu)
    elif text == "Выход🚪":
        bot.send_message(message.from_user.id, f'Вы вернулись в главное меню!✅'
                         , reply_markup=main_menu)


def buy_sandwich(message, players):
    text = message.text
    if text.isdigit():
        if settings.user.money >= 1000:
            if int(text) <= len(players):
                change_settings(message, 6, 1, int(text) - 1)
                change_settings(message, 2, -1000)
                bot.send_message(message.from_user.id,
                                 f'Бутерброд был куплен успешно!✅\n Выбранному игроку была добавлена 1 '
                                 f'единица энергии!⚡', reply_markup=shop_menu)
                bot.register_next_step_handler(message, shop)
            else:
                bot.send_message(message.from_user.id, f'У вас нету игрока под таким номером!🙅‍♂️',
                                 reply_markup=shop_menu)
                bot.register_next_step_handler(message, shop)
        else:
            bot.send_message(message.from_user.id, f'У вас не хватает денег на покупку!❌', reply_markup=shop_menu)
            bot.register_next_step_handler(message, shop)
    elif text == 'Выход🚪':
        bot.send_message(message.from_user.id, f'Вы отменили покупку!❌', reply_markup=shop_menu)
        bot.register_next_step_handler(message, shop)
    else:
        bot.send_message(message.from_user.id, f'Ты не правильно ввёл данные!🤬', reply_markup=shop_menu)
        bot.register_next_step_handler(message, shop)


def first_round(message, number):
    answer = message.text
    if int(get_data_settings(message, 1)[5]) == 0:
        win = 0
        buttons = ['◀️', '🔼', '▶️']
        miss_procent70 = buttons[random.randint(0, 2)]
        chance = random.randint(1, 100)
        print(miss_procent70)
        print(chance)
        if message.text == miss_procent70:
            if chance > 25 - int(get_data_settings(message, 2)[number].split(',')[1]) * 3:
                bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉')
                win = 1
            else:
                bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                                 reply_markup=main_menu)
                win = 0
        else:
            bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉')
            win = 1

        if win == 1:
            bot.send_message(message.from_user.id, f'Твой персонаж на втором этапе! Выбери куда пнуть мяч!',
                             reply_markup=game_menu)
            _1lvl2rnd = open('1lvl2rnd.png', 'rb')
            bot.register_next_step_handler(message, second_round, number)
            bot.send_photo(message.from_user.id, _1lvl2rnd)
            _1lvl2rnd.close()
    elif int(get_data_settings(message, 1)[5]) == 1:
        win = 0
        buttons = ['◀️', '🔼', '▶️']
        miss_procent70 = buttons[random.randint(0, 2)]
        chance = random.randint(1, 100)
        print(miss_procent70)
        print(chance)
        if message.text == miss_procent70:
            if chance > 20 - int(get_data_settings(message, 2)[number].split(',')[1]) * 3:
                bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉')
                win = 1
            else:
                bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                                 reply_markup=main_menu)
                win = 0
        else:
            bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉')
            win = 1

        if win == 1:
            bot.send_message(message.from_user.id, f'Твой персонаж на втором этапе! Выбери куда пнуть мяч!',
                             reply_markup=game_menu)
            _1lvl2rnd = open('1lvl2rnd.png', 'rb')
            bot.register_next_step_handler(message, second_round, number)
            bot.send_photo(message.from_user.id, _1lvl2rnd)
            _1lvl2rnd.close()


def second_round(message, number):
    if int(get_data_settings(message, 1)[5]) == 0:
        win = 0
        answer = message.text
        buttons = ['◀️', '🔼', '▶️']
        miss_procent80 = buttons[random.randint(0, 2)]
        print(miss_procent80)
        chance = random.randint(1, 100)
        print(chance)
        if message.text == miss_procent80:
            if chance > 30 - int(get_data_settings(message, 2)[number].split(',')[1]) * 3:
                bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                                 reply_markup=game_menu)
                win = 1
            else:
                bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                                 reply_markup=main_menu)
                win = 0
        else:
            bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                             reply_markup=game_menu)
            win = 1

        if win == 1:
            bot.register_next_step_handler(message, third_round, number)
            _1lvl3rnd = open('1lvl3rnd.png', 'rb')
            bot.send_photo(message.from_user.id, _1lvl3rnd)
            _1lvl3rnd.close()
    if int(get_data_settings(message, 1)[5]) == 1:
        win = 0
        answer = message.text
        buttons = ['◀️', '🔼', '▶️']
        miss_procent80 = buttons[random.randint(0, 2)]
        print(miss_procent80)
        chance = random.randint(1, 100)
        print(chance)
        if message.text == miss_procent80:
            if chance > 25 - int(get_data_settings(message, 2)[number].split(',')[1]) * 3:
                bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                                 reply_markup=game_menu)
                win = 1
            else:
                bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                                 reply_markup=main_menu)
                win = 0
        else:
            bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                             reply_markup=game_menu)
            win = 1

        if win == 1:
            bot.register_next_step_handler(message, third_round, number)
            _1lvl3rnd = open('1lvl3rnd.png', 'rb')
            bot.send_photo(message.from_user.id, _1lvl3rnd)
            _1lvl3rnd.close()


def third_round(message, number):
    if int(get_data_settings(message, 1)[5]) == 0:
        win = 0
        answer = message.text
        first_buttons = ['◀️', '🔼', '▶️']
        print(message.text)
        rand = random.randint(0, 2)
        miss_procent80 = first_buttons.pop(rand)
        miss_procent50 = first_buttons[random.randint(0, 1)]
        chance = random.randint(1, 100)
        print(miss_procent80)
        print(chance)
        if message.text == miss_procent80:
            if chance > 30 - int(get_data_settings(message, 2)[number].split(',')[1]) * 3:
                bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                                 reply_markup=game_menu)
                win = 1
            else:
                bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                                 reply_markup=main_menu)
                win = 0
        elif message.text == miss_procent50:
            if chance > 15:
                bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                                 reply_markup=game_menu)
                win = 1
            else:
                bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                                 reply_markup=main_menu)
                win = 0
        else:
            bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                             reply_markup=game_menu)
            win = 1

        if win == 1:
            bot.register_next_step_handler(message, forth_round, number)
            _1lvl4rnd = open('1lvl4rnd.png', 'rb')
            bot.send_photo(message.from_user.id, _1lvl4rnd)
            _1lvl4rnd.close()
    if int(get_data_settings(message, 1)[5]) == 1:
        win = 0
        answer = message.text
        first_buttons = ['◀️', '🔼', '▶️']
        print(message.text)
        rand = random.randint(0, 2)
        miss_procent80 = first_buttons.pop(rand)
        miss_procent50 = first_buttons[random.randint(0, 1)]
        chance = random.randint(1, 100)
        print(miss_procent80)
        print(chance)
        if message.text == miss_procent80:
            if chance > 23 - int(get_data_settings(message, 2)[number].split(',')[1]) * 2:
                bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                                 reply_markup=game_menu)
                win = 1
            else:
                bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                                 reply_markup=main_menu)
                win = 0
        elif message.text == miss_procent50:
            if chance > 11:
                bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                                 reply_markup=game_menu)
                win = 1
            else:
                bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                                 reply_markup=main_menu)
                win = 0
        else:
            bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                             reply_markup=game_menu)
            win = 1

        if win == 1:
            bot.register_next_step_handler(message, forth_round, number)
            _1lvl4rnd = open('1lvl4rnd.png', 'rb')
            bot.send_photo(message.from_user.id, _1lvl4rnd)
            _1lvl4rnd.close()


def forth_round(message, number):
    win = 0
    answer = message.text
    first_buttons_one = ['◀️', '🔼', '▶️']
    print(message.text)
    rand = random.randint(0, 2)
    block = first_buttons_one.pop(rand)
    miss_procent80 = first_buttons_one.pop(random.randint(0, 1))
    # block = second_buttons[random.randint(0, 1)]
    chance = random.randint(1, 100)
    if message.text == miss_procent80:
        if chance > 0:
            bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉',
                             reply_markup=game_menu)
            win = 1
        else:
            bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                             reply_markup=main_menu)
            win = 0
    elif message.text == block:
        bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                         reply_markup=main_menu)
        win = 0
    else:
        bot.send_message(message.from_user.id, f'Так держать! Вы прошли на следующий этап!🎉', reply_markup=game_menu)
        win = 1

    if win == 1:
        bot.register_next_step_handler(message, fifth_round, number)
        _1lvl5rnd = open('1lvl5rnd.png', 'rb')
        bot.send_photo(message.from_user.id, _1lvl5rnd)
        _1lvl5rnd.close()


def fifth_round(message, number):
    if int(get_data_settings(message, 1)[5]) == 0:
        apply_increase = 0
        probability = 25 - int(get_data_settings(message, 2)[number].split(',')[1]) * 3
    else:
        apply_increase = 1
        probability = 16 - int(get_data_settings(message, 2)[number].split(',')[1]) * 3
    win = 0
    answer = message.text
    first_buttons_one = ['◀️', '🔼', '▶️']
    print(message.text)
    rand = random.randint(0, 2)
    block = first_buttons_one.pop(rand)
    miss_chance90 = first_buttons_one.pop(random.randint(0, 1))
    # block = second_buttons[random.randint(0, 1)]
    chance = random.randint(1, 100)
    if message.text == miss_chance90:
        if chance > probability:
            win = 1
        else:
            bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                             reply_markup=main_menu)
            win = 0
    elif message.text == block:
        bot.send_message(message.from_user.id, f'К сожалению ваш мяч перехватили. Вы проиграли.😓',
                         reply_markup=main_menu)
        win = 0
    else:
        win = 1

    if win == 1:
        if apply_increase == 1:
            print('Добавление increase')
            change_settings(message, 2, 2500)
            change_settings(message, 3, 1)
            # settings.user.money += 1500 + settings.user.increase
            # settings.user.trophy += 0
            bot.send_message(message.from_user.id,
                             f'Победа!🎉 \nВы провели своего игрока к победе🏆\nзабив решающий гол!⚽️',
                             reply_markup=main_menu)
        else:
            print('Добавление обычное')
            change_settings(message, 2, 1500)
            change_settings(message, 3, 1)
            # settings.user.increase = 0
            # settings.user.money += 1500
            # settings.user.trophy += 0
            bot.send_message(message.from_user.id,
                             f'Победа!🎉 \nВы провели своего игрока к победе🏆\nзабив решающий гол!⚽️',
                             reply_markup=main_menu)


def get_mode(message, number):
    text = message.text
    if text == 'Чемпионат':
        bot.send_message(message.from_user.id, f'Ты попал на матч своей команды! ВЫбирай стрелки и в соответствии'
                                               f' с ними твой игрок пнёт мяч в нужное '
                                               f'направлении', reply_markup=game_menu)
        _1lvl1rnd = open('1lvl1rnd.png', 'rb')
        bot.send_message(message.from_user.id, f'Твой персонаж на первом этапе! Выбери куда пнуть мяч!',
                         reply_markup=game_menu)
        bot.send_photo(message.from_user.id, _1lvl1rnd)
        bot.register_next_step_handler(message, first_round, number)
        _1lvl1rnd.close()
    elif text == 'Штрафные':
        bot.send_message(message.from_user.id,
                         f'Ты находишься на линии штрафной! Твоя задача выбрать угол, в котоый ты будешь пинать',
                         reply_markup=goalkeeper_menu)
        goalkeeper_img = open("goalkeeper_game_test.png", 'rb')
        bot.send_message(message.from_user.id, f'Выбери куда пнуть мяч!', reply_markup=goalkeeper_menu)
        bot.send_photo(message.from_user.id, goalkeeper_img)
        goalkeeper_img.close()
        bot.register_next_step_handler(message, second_gm_first_rnd)


def get_player(message, players):
    text = message.text
    if text.isdigit():
        if int(text) <= len(players):
            number = int(text) - 1
            player = players[number].split(',')
            if int(player[2]) > 0:
                bot.send_message(message.from_user.id, f'Выбери режим игры.🎮', reply_markup=choose_gm_menu)
                change_settings(message, 6, -1, number)
                bot.register_next_step_handler(message, get_mode, number)
            else:
                bot.send_message(message.from_user.id, f'У выбранного игрока недостаточно энергии!⚡️',
                                 reply_markup=main_menu)
        else:
            bot.send_message(message.from_user.id, f'У вас нету игрока под таким номером!🙅‍♂️', reply_markup=main_menu)
    elif text == 'Выход🚪':
        bot.send_message(message.from_user.id, f'Вы вернулись в главное меню!✅'
                         , reply_markup=main_menu)
    else:
        bot.send_message(message.from_user.id, f'Ты не правильно ввёл данные!🤬', reply_markup=main_menu)


def second_gm_first_rnd(message):
    answer = message.text
    buttons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
    blocked_first = buttons[random.randint(0, 3)]
    if buttons.index(answer) != blocked_first:
        bot.send_message(message.from_user.id, f'Повезло... Ты проходишь дальше!👏')
        bot.send_message(message.from_user.id, f'Выбери куда пнуть мяч!')
        goalkeeper_img = open("goalkeeper_game_test.png", 'rb')
        bot.send_photo(message.from_user.id, goalkeeper_img)
        goalkeeper_img.close()
        bot.register_next_step_handler(message, second_gm_second_rnd)
    else:
        bot.send_message(message.from_user.id, f'Твой удар отразили матч для тебя окончен!😓', reply_markup=main_menu)
    print(message.text)


def second_gm_second_rnd(message):
    answer = message.text
    buttons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
    blocked_first = buttons[random.randint(0, 3)]
    if buttons.index(answer) != blocked_first:
        bot.send_message(message.from_user.id, f'Повезло... Ты проходишь дальше!👏')
        bot.send_message(message.from_user.id, f'Выбери куда пнуть мяч!')
        goalkeeper_img = open("goalkeeper_game_test.png", 'rb')
        bot.send_photo(message.from_user.id, goalkeeper_img)
        goalkeeper_img.close()
        bot.register_next_step_handler(message, second_gm_third_rnd())
    else:
        bot.send_message(message.from_user.id, f'Твой удар отразили матч для тебя окончен!😓', reply_markup=main_menu)
    print(message.text)


def second_gm_third_rnd(message):
    answer = message.text
    buttons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
    blocked_first = random.randint(0, 3)
    buttons.pop(blocked_first)
    blocked_second = random.randint(0, 2)
    buttons.pop(blocked_second)
    if answer in buttons:
        bot.send_message(message.from_user.id, f'Ого!🙀\n Ты пробил все 3 штафных!⚽️\n победа за тобой!🥳',
                         reply_markup=main_menu)
        settings.user.money += 1500
        settings.user.trophy += 2
    else:
        bot.send_message(message.from_user.id, f'Твой удар отразили матч для тебя окончен!😓', reply_markup=main_menu)
    print(message.text)


def get_list_files(message):
    medals = ['🥇', '🥈', '🥉', '🏅']
    top_users = []
    for root, dirs, files in os.walk("./users"):
        for filename in files:
            path = './users/' + filename
            f = open(path, 'r')
            line = f.readline().split(',')
            print('line', line)
            if len(line) == 1:
                continue
            name, trophy = line[0], int(line[2])
            top_users.append((name, trophy))
            f.close()
    top_users.sort(key=lambda x: x[1], reverse=True)
    line_top = ''
    for i in range(len(top_users)):
        if i == 0:
            line_top += medals[0] + top_users[i][0] + ' ' + str(top_users[i][1])
        elif i == 1:
            line_top += medals[1] + top_users[i][0] + ' ' + str(top_users[i][1])
        elif i == 2:
            line_top += medals[2] + top_users[i][0] + ' ' + str(top_users[i][1])
        else:
            line_top += medals[3] + top_users[i][0] + ' ' + str(top_users[i][1])
        line_top += '🏆\n'
    bot.send_message(message.from_user.id, line_top, reply_markup=main_menu)


bot.polling(none_stop=True)
