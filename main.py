import telebot
from telebot import types

import datetime

bot = telebot.TeleBot("6719842419:AAE_4QwMa6jz6bePUFUSbJyyB5XIU-PyHp4")


@bot.message_handler(commands=['start', 'help'])
def send_info(message):
    send_welcome(message)
    bot.send_message(
        message.chat.id,
        "Сделал @faworitewine\nПо всем вопросам @mdaaaatrash\nВерсия 0.0.2")


def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    hydro_button = types.KeyboardButton('Гидрографи')
    schedule_button = types.KeyboardButton('Расписание')
    markup.add(hydro_button, schedule_button)
    bot.reply_to(message, "Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Гидрографи' or message.text == '/hydrography':
        print("[LOG] Command: Гидрография | UserName: " + str(message.from_user.username) + " | FL Name: " + str(
            message.from_user.first_name) + " " + str(message.from_user.last_name))
        bot.reply_to(message,
                     "Сделал @faworitewine\nПо всем вопросам @mdaaaatrash\nВерсия 0.1.1\n*Введите количество точек:*",
                     parse_mode="Markdown")
        bot.register_next_step_handler(message, ask_depth)
    elif message.text == 'Расписание':
        print("[LOG] Command: Расписание | UserName: " + str(message.from_user.username) + " | FL Name: " + str(
            message.from_user.first_name) + " " + str(message.from_user.last_name))
        week_number = get_week_number()
        if week_number is not None:
            send_info(message)
            parity = "четная" if week_number % 2 == 0 else "нечетная"

            if parity == "четная":
                bot.send_photo(
                    message.chat.id,
                    "https://i.postimg.cc/KvFqCJcZ/2024-02-16-22-14-58.png")
            else:
                bot.send_photo(
                    message.chat.id,
                    "https://i.postimg.cc/vmddK5Kf/2024-02-16-22-13-56.png")
    elif message.text == 'test':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton('2', callback_data='point_1')
        item2 = types.InlineKeyboardButton('3', callback_data='point_2')
        markup.add(item, item2)
        bot.send_message(message.chat.id, 'Выбирите колличество точек!', reply_markup=markup)


def ask_depth(message):
    try:
        count = int(message.text)
        bot.reply_to(
            message,
            "Введите глубину и расстояние для точки 1 \nНапишите значения через пробел:"
        )
        bot.register_next_step_handler(message,
                                       lambda m: process_depth(m, 1, count, []))
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите целое число.")


def process_depth(message, point_num, count, depths):
    try:
        data = message.text.split()
        depth = float(data[0])
        distance = float(data[1])

        depths.append((depth, distance))

        if len(depths) < count:
            bot.reply_to(
                message,
                f"Введите глубину и расстояние для точки {point_num + 1} \nНапишите значения через пробел:"
            )
            bot.register_next_step_handler(
                message, lambda m: process_depth(m, point_num + 1, count, depths))
        else:
            calculate_Z(message, depths)
    except (ValueError, IndexError):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton('2', callback_data='point_1')
        item2 = types.InlineKeyboardButton('3', callback_data='point_2')
        markup.add(item, item2)
        bot.reply_to(message, "Пожалуйста, введите данные в формате 'глубина расстояние /start'.", reply_markup=markup)


def calculate_Z(message, data):
    z1 = 0
    m1 = 0

    for depth, distance in data:
        z1 += depth / (distance / 60)
        m1 += 1 / (distance / 60)

    Z = z1 / m1
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('2', callback_data='point_1')
    item2 = types.InlineKeyboardButton('3', callback_data='point_2')
    markup.add(item, item2)
    bot.reply_to(message, f"_Z = {Z}_ \n/hydrography - Повторное использование\n*Или выбирите колличесво точек снизу*",
                 reply_markup=markup, parse_mode="Markdown")


def get_week_number():
    try:
        now = datetime.datetime.now()
        return now.isocalendar()[1]
    except Exception as e:
        print(f"Error getting week number: {e}")
        return None


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    print("[LOG] Command: Гидрография_Point | UserName: " + str(call.message.from_user.username) + " | FL Name: " + str(
        call.message.from_user.first_name) + " " + str(call.message.from_user.last_name))
    if call.message:
        if call.data == 'point_1':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Выбрано 2 точки!')
            ask_de(call.message, 2)
        elif call.data == 'point_2':
            ask_de(call.message, 3)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Выбрано 3 точки!')


def ask_de(message, count):
    bot.reply_to(message, "Введите глубину и расстояние для точки 1 \nНапишите значения через пробел:")
    bot.register_next_step_handler(message, lambda m: process_depth(m, 1, count, []))


bot.polling(none_stop=True)
