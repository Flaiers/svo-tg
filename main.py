from bot import TOKEN, unknown, FAQ_list_inline, list_answers
from states import SVO
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import message, ReplyKeyboardRemove
import logging, asyncio, string, random, time, kb, re

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

# handler на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('👋 Привет, {0.first_name}!'
        '\nЯ — HR-бот аэропорта Шереметьево. Помогаю адаптироваться новым сотрудникам. Чтобы начать пользоваться сервисом, перейди в Главное меню, нажав на кнопку'.format(message.from_user),
        reply_markup=kb.reply_main)

# handler всех сообщений
@dp.message_handler()
async def main(message: types.Message, state:FSMContext):
    if message.text == "🏠 Главное меню":
        await message.answer('Ты в Главном меню, выбери что ты хочешь',
            reply_markup=kb.reply_menu)

    elif message.text == '✏️ Задать вопрос':
        await message.answer('Введи мне свой вопрос, хочешь вернуться назад, нажми на кнопку',
            reply_markup=kb.reply_back)

        await SVO.question.set()

    elif message.text == '📝 Часто задаваемые вопросы':
        send = await bot.send_message(message.chat.id, 'Чтобы получить ответ, выбери тему интересующей информации:',
            reply_markup=kb.inline_faq)

        back = await bot.send_message(message.chat.id, 'Хочешь вернуться назад, нажми на кнопку',
            reply_markup=kb.reply_back)

        async with state.proxy() as data:
            delete = back.message_id
            mes = send.message_id
            data["delete_id"] = delete
            data["message_id"] = mes

    elif message.text == '🔄 Задать вопрос снова':
        send = await bot.send_message(message.chat.id, 'Чтобы получить ответ, выбери тему интересующей информации:',
            reply_markup=kb.inline_faq)

        back = await bot.send_message(message.chat.id, 'Хочешь вернуться назад, нажми на кнопку',
            reply_markup=kb.reply_back)

        async with state.proxy() as data:
            delete = back.message_id
            mes = send.message_id
            data["delete_id"] = delete
            data["message_id"] = mes

    elif message.text == '◀️ Назад':
        await message.answer('Ты в Главном меню, выбери что ты хочешь',
            reply_markup=kb.reply_menu)
        try:
            async with state.proxy() as data:
                mes = data["message_id"]

            await bot.delete_message(chat_id=message.chat.id,
                message_id=mes)
        except KeyError:
            print("Error: message_id not found")

    else:
        await message.answer(random.choice(unknown),
            reply_markup=kb.reply_menu)

# handler попадания в задачу вопроса
@dp.message_handler(state=SVO.question, content_types=types.ContentTypes.TEXT)
async def question(message: types.Message, state:FSMContext):
    question = message.text
    async with state.proxy() as data:
        data["question1"] = question
        answer = data["question1"]
    if answer == '◀️ Назад':
        await message.answer('Ты в Главном меню, выбери что ты хочешь',
            reply_markup=kb.reply_menu)
        await state.reset_state()

    else:
        '''похожее на вопрос 0'''
        park = re.findall('парк', answer, flags=re.I)
        places = re.findall('мест', answer, flags=re.I)
        '''похожее на вопрос 1'''
        phone = re.findall('телефон', answer, flags=re.I)
        urgent = re.findall('сроч', answer, flags=re.I)
        rescue = re.findall('спасат', answer, flags=re.I)
        service = re.findall('служб', answer, flags=re.I)
        '''похожее на вопрос 2'''
        passage = re.findall('проход', answer, flags=re.I)
        train = re.findall('обуче', answer, flags=re.I)
        security = re.findall('охран', answer, flags=re.I)
        labor = re.findall('труда', answer, flags=re.I)
        '''похожее на вопрос 3'''
        route = re.findall('маршрут', answer, flags=re.I)
        corporate = re.findall('корпорат', answer, flags=re.I)
        transport = re.findall('транспорт', answer, flags=re.I)
        '''похожее на вопрос 4'''
        events = re.findall('событ', answer, flags=re.I)
        tester = re.findall('испыт', answer, flags=re.I)
        term = re.findall('срок', answer, flags=re.I)
        '''похожее на вопрос 5'''
        sale = re.findall('скидк', answer, flags=re.I)
        employee = re.findall('сотрудник', answer, flags=re.I)
        worker = re.findall('работник', answer, flags=re.I)
        '''похожее на вопрос 6'''
        mentor = re.findall('настав', answer, flags=re.I)
        '''похожее на вопрос 7'''
        card = re.findall('карт', answer, flags=re.I)
        medicine = re.findall('медицин', answer, flags=re.I)
        insurance = re.findall('страхов', answer, flags=re.I)
        '''похожее на вопрос 8'''
        admission  = re.findall('пропуск', answer, flags=re.I)

        if park or places:
            await message.answer(list_answers[0],
                reply_markup=kb.inline_more0)
            await state.reset_state()

        elif phone or urgent or rescue or service:
            await message.answer(list_answers[1] + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
                reply_markup=kb.reply_again_main)

            await state.reset_state()
            await SVO.again.set()

        elif sale or employee or worker:
            await message.answer(list_answers[2] + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
                reply_markup=kb.reply_again_main, parse_mode='html')

            await state.reset_state()
            await SVO.again.set()

        elif mentor:
            await message.answer(list_answers[3] + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
                reply_markup=kb.reply_again_main)

            await state.reset_state()
            await SVO.again.set()

        elif route or corporate or transport:
            await message.answer(list_answers[4],
                reply_markup=kb.inline_more4)
            await state.reset_state()

        elif passage or train or security or labor:
            await message.answer(list_answers[5] + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
                reply_markup=kb.reply_again_main)

            await state.reset_state()
            await SVO.again.set()

        elif events or tester or term:
            await message.answer(list_answers[6] + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
                reply_markup=kb.reply_again_main)

            await state.reset_state()
            await SVO.again.set()

        elif admission:
            await message.answer(list_answers[7] + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
                reply_markup=kb.reply_again_main)

            await state.reset_state()
            await SVO.again.set()

        elif card or medicine or insurance:
            await message.answer(list_answers[8] + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
                reply_markup=kb.reply_again_main)

            await state.reset_state()
            await SVO.again.set()

        else:
            await message.answer(f'{random.choice(unknown)}\n'
                'Выбери одну из кнопок',
                reply_markup=kb.reply_again_main)

            await state.reset_state()
            await SVO.again.set()

# handler возвращения снова к задаче вопроса
@dp.message_handler(state=SVO.again, content_types=types.ContentTypes.TEXT)
async def again(message: types.Message, state:FSMContext):
    again = message.text
    async with state.proxy() as data:
        data["again1"] = again
        text = data["again1"]

    if text == '🔄 Задать вопрос снова':
        await message.answer('Введи мне свой вопрос снова, хочешь вернуться назад, нажми на кнопку',
            reply_markup=kb.reply_back)

        await state.reset_state()
        await SVO.question.set()

    elif text == '🏠 Главное меню':
        await message.answer('Ты в Главном меню, выбери что ты хочешь',
            reply_markup=kb.reply_menu)
        await state.reset_state()

    else:
        await message.answer(f'{random.choice(unknown)}\n'
            'Выбери одну из кнопок',
            reply_markup=kb.reply_again_main)

        await state.reset_state()
        await SVO.again.set()

# callback inline кнопок
@dp.callback_query_handler(lambda message: message.data.startswith("FAQ"))
async def faq(callback_query: types.CallbackQuery, state:FSMContext):
    await bot.answer_callback_query(callback_query.id)
    number = int(callback_query.data[3:])
    answer = FAQ_list_inline[number][1]

    async with state.proxy() as data:
        mes = data["message_id"]
        delete = data["delete_id"]

    await bot.delete_message(chat_id=callback_query.message.chat.id,
        message_id=mes)

    await bot.delete_message(chat_id=callback_query.message.chat.id,
        message_id=delete)

    '''для корректного отображения клавиатуры'''
    await asyncio.sleep(0.1)

    await bot.send_message(callback_query.from_user.id, f'Ответ на тему интересующей информации: "{FAQ_list_inline[number][0]}"',
        reply_markup=kb.reply_again_main)

    if number == 0:
        await bot.send_message(callback_query.from_user.id, answer,
            reply_markup=kb.inline_more0)

    elif number == 1:
        await bot.send_message(callback_query.from_user.id, answer + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main)

    elif number == 2:
        await bot.send_message(callback_query.from_user.id, answer + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

    elif number == 3:
        await bot.send_message(callback_query.from_user.id, answer + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main)

    elif number == 4:
        await bot.send_message(callback_query.from_user.id, answer,
            reply_markup=kb.inline_more4)

    elif number == 5:
        await bot.send_message(callback_query.from_user.id, answer + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main)

    elif number == 6:
        await bot.send_message(callback_query.from_user.id, answer + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main)

    elif number == 7:
        await bot.send_message(callback_query.from_user.id, answer + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main)

    elif number == 8:
        await bot.send_message(callback_query.from_user.id, answer + '\n\nМожешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main)

# callback inline кнопоки Еще для вороса 0
@dp.callback_query_handler(lambda message: message.data.startswith("more0"))
async def more0(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    with open("/home/git/svo-tg/static/sticker1.webp", "rb") as file1:
        sticker1 = file1.read()

    with open("/home/git/svo-tg/static/sticker2.webp", "rb") as file2:
        sticker2 = file2.read()

    with open("/home/git/svo-tg/static/sticker3.webp", "rb") as file3:
        sticker3 = file3.read()

    with open("/home/git/svo-tg/static/sticker4.webp", "rb") as file4:
        sticker4 = file4.read()

    await bot.send_sticker(callback_query.from_user.id, sticker1)
    await bot.send_message(callback_query.from_user.id, 'Места внутри паркинга:\n5000 рублей в месяц\n\nМеста на крыше паркинга:\n4000 рублей в месяц',
        reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(3)

    await bot.send_sticker(callback_query.from_user.id, sticker2)
    await bot.send_message(callback_query.from_user.id, 'Стоимость абонемента на парковку для сотрудников составляет:\n3000 рублей в месяц\n\nДля членов профсоюза: 2500 рублей в месяц')
    await asyncio.sleep(3.5)

    await bot.send_sticker(callback_query.from_user.id, sticker3)
    await bot.send_message(callback_query.from_user.id, 'Стоимость абонемента для сотрудников составляет:\n2500 рублей в месяц')
    await asyncio.sleep(3.5)

    await bot.send_sticker(callback_query.from_user.id, sticker4)
    await bot.send_message(callback_query.from_user.id, 'Парковка Р4:\nСтоимость абонемента для сотрудников составляет:\n5000 рублей в месяц\n\nПарковка Р6:\nСтоимость абонемента для сотрудников составляет:\n4000 рублей в месяц\n\n'
        'Можешь еще раз задать вопрос или вернуться в Главное меню',
        reply_markup=kb.reply_again_main)

# callback inline кнопоки Еще для вороса 4
@dp.callback_query_handler(lambda message: message.data.startswith("more4"))
async def more4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выбери, в Шереметьево или из Шереметьево тебе нужно. Хочешь вернуться в Главное меню, нажми на кнопку',
        reply_markup=kb.reply_transport_main)
    await SVO.transport.set()

# handler отправки корпоративного транспорта
@dp.message_handler(state=SVO.transport, content_types=types.ContentTypes.TEXT)
async def transport(message: types.Message, state:FSMContext):
    transport = message.text
    async with state.proxy() as data:
        data["transport1"] = transport
        text = data["transport1"]

    if text == 'В Шереметьево':
        await message.answer('Выбери своё местоположение, или откуда тебе нужно добраться до Шереметьево',
            reply_markup=kb.reply_from_location)

        await state.reset_state()
        await SVO.from_location.set()

    elif text == 'Из Шереметьево':
        await message.answer('Выбери куда тебе нужно',
            reply_markup=kb.reply_to_location)

        await state.reset_state()
        await SVO.to_location.set()
    
    elif text == '🏠 Главное меню':
        await message.answer('Ты в Главном меню, выбери что ты хочешь',
            reply_markup=kb.reply_menu)
        await state.reset_state()

    else:
        await message.answer(f'{random.choice(unknown)}\n'
            'Выбери одну из кнопок',
            reply_markup=kb.reply_transport_main)

        await state.reset_state()
        await SVO.transport.set()

# handler отправки откуда нужно добраться
@dp.message_handler(state=SVO.from_location, content_types=types.ContentTypes.TEXT)
async def from_location(message: types.Message, state:FSMContext):
    from_location = message.text
    async with state.proxy() as data:
        data["from_location1"] = from_location
        text = data["from_location1"]

    if text == '◀️ Назад':
        await message.answer('Выбери, в Шереметьево или из Шереметьево тебе нужно. Хочешь вернуться в Главное меню, нажми на кнопку',
            reply_markup=kb.reply_transport_main)

        await state.reset_state()
        await SVO.transport.set()

    elif text == 'Лобня':
        await message.answer('<ins>Маршрут №3</ins>:\nСтанция Лобня - Кафе «Севастополь» — 07:15\n\n'
            '<ins>Маршрут №5</ins>:\nСтанция Лобня - Терминал D — 06:30 (по выходным 6:45), 18:50\n\n'
            '<ins>Маршрут №6</ins>:\nСтанция Лобня - Терминал E — 08:25 (по будням)\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    elif text == 'Красная Поляна':
        await message.answer('<ins>Маршрут №1</ins>:\nКрасная Поляна - Кафе «Севастополь» — 07:05\n\n'
            '<ins>Маршрут №2</ins>:\nКрасная Поляна - Терминал E — 07:40 (по выходным 8:00)\n\n'
            '<ins>Маршрут №4</ins>:\nКрасная Поляна - Терминал E — 06:30 (по выходным 6:45), 18:50\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    elif text == 'Метро Сходненская':
        await message.answer('<ins>Маршрут №10</ins>:\nметро Сходненская - Терминал E — 07:50\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    elif text == 'Зеленоград':
        await message.answer('<ins>Маршрут №7</ins>:\nЗеленоград - Терминал E — 06:25, 18:10\n\n'
            '<ins>Маршрут №8</ins>:\nЗеленоград - Терминал E — 07:25\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    elif text == 'Хлебниково':
        await message.answer('<ins>Маршрут №11</ins>:\nХлебниково - Терминал E — 07:00, 08:30, 19:00\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    else:
        await message.answer(f'{random.choice(unknown)}\n'
            'Выбери одну из кнопок',
            reply_markup=kb.reply_from_location)

        await state.reset_state()
        await SVO.from_location.set()

# handler отправки куда нужно добраться
@dp.message_handler(state=SVO.to_location, content_types=types.ContentTypes.TEXT)
async def to_location(message: types.Message, state:FSMContext):
    to_location = message.text
    async with state.proxy() as data:
        data["to_location1"] = to_location
        text = data["to_location1"]

    if text == '◀️ Назад':
        await message.answer('Выбери, в Шереметьево или из Шереметьево тебе нужно. Хочешь вернуться в Главное меню, нажми на кнопку',
            reply_markup=kb.reply_transport_main)

        await state.reset_state()
        await SVO.transport.set()

    elif text == 'Лобня':
        await message.answer('<ins>Маршрут №5</ins>:\nТерминал E - станция Лобня — 08:20, 17:05 по будням (по пятницам 14:35), 20:15\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    elif text == 'Красная Поляна':
        await message.answer('<ins>Маршрут №1</ins>:\nАдминистрация - Красная Поляна — 18:15 по будням (по пятницам 15:45)\n\n'
            '<ins>Маршрут №2</ins>:\n7 корпус - Красная Поляна — 18:05 по будням (по пятницам 15:50)\n\n'
            '<ins>Маршрут №3</ins>:\n7 корпус - Красная Поляна (ул. Текстильная) — 17:05 по будням (по пятницам 14:35)\n\n'
            '<ins>Маршрут №4</ins>:\nТерминал E - Красная Поляна — 08:20, 17:50 (по пятницам 15:35), 20:15\n\n'
            '<ins>Маршрут №6</ins>:\nТерминал E - ст. Лобня - Красная Поляна — 18:15 (по пятницам 15:45)\n\n'
            '<ins>Маршрут №8</ins>:\nТерминал E - Депо - Красная Поляна — 09:10\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    elif text == 'Метро Сходненская':
        await message.answer('<ins>Маршрут №10</ins>:\nШереметьево 1 - м.Сходненская — 18:15 по будням (по пятницам 15:45)\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    elif text == 'Зеленоград':
        await message.answer('<ins>Маршрут №7</ins>:\nТерминал E - Зеленоград — 08:30, 17:05 по будням (по пятницам 14:35)\n\n'
            '<ins>Маршрут №7</ins>:\nШереметьево 1 - Зеленоград — 20:15\n\n'
            '<ins>Маршрут №8</ins>:\nКорпус №7 - Зеленоград — 18:15 (по пятницам 15:45)\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    elif text == 'Хлебниково':
        await message.answer('<ins>Маршрут №11</ins>:\nТерминал E - Хлебниково — 08:10, 09:10, 17:05 по будням (по пятницам 14:35), 18:15 по будням (по пятницам 15:45), 20:15\n\n'
            'Можешь еще раз задать вопрос или вернуться в Главное меню',
            reply_markup=kb.reply_again_main, parse_mode='html')

        await state.reset_state()

    else:
        await message.answer(f'{random.choice(unknown)}\n'
            'Выбери одну из кнопок',
            reply_markup=kb.reply_to_location)

        await state.reset_state()
        await SVO.to_location.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
