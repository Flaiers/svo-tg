from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
                        InlineKeyboardMarkup, InlineKeyboardButton

from config import FAQ_list_inline


# текст кнопок
button_main = KeyboardButton('🏠 Главное меню')
button_back = KeyboardButton('◀️ Назад')
button_que = KeyboardButton('✏️ Задать вопрос')
button_faq = KeyboardButton('📝 Часто задаваемые вопросы')
button_again = KeyboardButton('🔄 Задать вопрос снова')
button_more0 = InlineKeyboardButton('📋 Ещё...', callback_data='more0')
button_more4 = InlineKeyboardButton('📋 Ещё...', callback_data='more4')

button_to = KeyboardButton('В Шереметьево')
button_from_lobnya = KeyboardButton('Лобня')
button_from_polyana = KeyboardButton('Красная Поляна')
button_from_skhodnenskaya = KeyboardButton('Метро Сходненская')
button_from_zelenograd = KeyboardButton('Зеленоград')
button_from_khlebnikovo = KeyboardButton('Хлебниково')

button_from = KeyboardButton('Из Шереметьево')
button_to_lobnya = KeyboardButton('Лобня')
button_to_polyana = KeyboardButton('Красная Поляна')
button_to_skhodnenskaya = KeyboardButton('Метро Сходненская')
button_to_zelenograd = KeyboardButton('Зеленоград')
button_to_khlebnikovo = KeyboardButton('Хлебниково')

FAQ_button_list = []

for i, (q, a) in enumerate(FAQ_list_inline):
    FAQ_button_list.append(InlineKeyboardButton(q, callback_data="FAQ{}".format(i)))

# включение в работу кнопок
reply_main = ReplyKeyboardMarkup(resize_keyboard=True).add(button_main)

reply_again_main = ReplyKeyboardMarkup(resize_keyboard=True).add(button_again).add(button_main)

reply_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_que).add(button_faq)

reply_back = ReplyKeyboardMarkup(resize_keyboard=True).add(button_back)

reply_transport_main = ReplyKeyboardMarkup(resize_keyboard=True).add(button_to, button_from).add(button_main)

reply_from_location = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(button_from_skhodnenskaya)\
    .add(button_from_lobnya, button_from_polyana)\
    .add(button_from_zelenograd, button_from_khlebnikovo)\
    .add(button_back)

reply_to_location = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(button_to_skhodnenskaya)\
    .add(button_to_lobnya, button_to_polyana)\
    .add(button_to_zelenograd, button_to_khlebnikovo)\
    .add(button_back)

inline_more0 = InlineKeyboardMarkup().add(button_more0)

inline_more4 = InlineKeyboardMarkup().add(button_more4)

inline_faq = InlineKeyboardMarkup()

for i in FAQ_button_list:
    inline_faq.add(i)
