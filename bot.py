import logging # эта библиотека идет вместе с python
from aiogram import Bot, Dispatcher, executor, types, filters # импортируем aiogram
from search_engines import shikimori_search, get_serial_info, get_serial_shiki_info
from functions import generate_cool_search_list, SearchBlockedError, \
    generate_translations_inline_keyboard, generate_quality_inline_keyboard, generate_quality_inline_keyboard_for_film, \
    generate_series_keyboard, NotFoundError
from link_getter import get_download_link
import threading

# API_TOKEN = os.getenv('TOKEN') # Токен  
API_TOKEN = "<TOKEN>"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
	await message.reply("Для поиска введите /search и имя тайтла через пробел")

@dp.message_handler(commands=['help'])
async def on_help(message: types.Message):
	await message.reply("Для поиска введите /search и имя тайтла через пробел.\n\n"\
        "Если вам написали что в поиске присутствуют материалы 18+, попробуйте указать более конкретное название или добавить номер сезона.\n\n"\
        "Если это не помогло, попробуйте получить id вручную. Для этого перейдите на сайт <a href='shikimori.one/animes'>Шикимори</a> и найдите там нужный сериал.\n"\
        "Зайдите на его страницу, и в адресной строке браузера, (https://shikimori.one/animes/30-neon-genesis-evangelion) вам нужно взять часть после \"animes/\" и перед \"-\". (В данном случае это 30)\n"\
        "Далее ведите команду /dowload подставив полученное id после слова <b><u>БЕЗ ПРОБЕЛА!</u></b> (В данном случае команда будет выглядеть так: /download30)"
    
    , parse_mode="HTML", disable_web_page_preview=True)

@dp.message_handler(commands=['search']) 
async def send_welcome(message: types.Message): # Реализует поиск
    txt = message.text[message.text.find(" ")+1:]
    print(f"[SEARCH] [{message.from_id}] {message.text}")
    repl = "Error"
    if txt == "" or txt == "/search":
        repl = "Вы должны указать название сериала для поиска"
    else:
        await message.answer("Поиск...")
        try:
            search = shikimori_search(txt)
        except SearchBlockedError:
            repl = f"Произошла ошибка поиска. Возможно результаты поиска содержат материалы 18+ и сайт заблокировал подключение. /help чтобы узнать как обойти ограничение."
        else:
            repl = generate_cool_search_list(search) # Возвращает красиво оформленный список
    await message.answer(repl, parse_mode="HTML", disable_web_page_preview=True)

@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=[r"/download\\*"]))  # Эта функция принимает id (/downloadxxx), отправка вопроса о переводе
async def download_translation_asker(message: types.Message):
    print(f"[DOWNLOAD REQUEST] [{message.from_id}] {message.text}")
    serial_id = message.text[9:]
    try:
        serial_info = await get_serial_info(serial_id)
    except NotFoundError:
        await message.answer(text="Похоже этот сериал отсутствует в базе Kodik'а")
        print("-- Kodik Not Found")
    else:
        try:
            data = await get_serial_shiki_info(serial_id)
        except SearchBlockedError:
            await message.answer("Ошибка поиска данных в шикимори")
        else:
            repl = f"{data['name']}\nВыберите озвучку из доступных:"
            # await message.answer(text=repl, reply_markup=generate_translations_inline_keyboard(serial_info['translations'], serial_info['series_count'], serial_id))
            await message.answer_photo(caption=repl, reply_markup=generate_translations_inline_keyboard(serial_info['translations'], serial_info['series_count'], serial_id), photo=data['pic'])

@dp.callback_query_handler(lambda c: c.data[0] == "T")  # Обработка выбора перевода, отправка вопроса о качестве
async def process_callback_translation_question(callback_query: types.CallbackQuery):
    print(f"[DOWNLOAD REQUEST] [{callback_query.message.from_user.id}] {callback_query.data}")
    await bot.answer_callback_query(callback_query.id)
    txt = callback_query.data.split("_")
    if txt[3] == "-1": # -1 Если фильм. В таком случае пропускается выбор серии
        await callback_query.message.answer(text=f"Выбран перевод \"{txt[2]}\"\nВыберите качество", reply_markup=generate_quality_inline_keyboard_for_film(int(txt[3]), txt[1], txt[4]))
    else:
        await callback_query.message.answer(text=f"Выбран перевод \"{txt[2]}\"\nВыберите качество", reply_markup=generate_quality_inline_keyboard(int(txt[3]), txt[1], txt[4]))

@dp.callback_query_handler(lambda c: c.data[0] == "Q")  # Обработка выбора качества, отправка вопроса о серии
async def process_callback_translation_question(callback_query: types.CallbackQuery):
    print(f"[DOWNLOAD REQUEST] [{callback_query.message.from_user.id}] {callback_query.data}")
    await bot.answer_callback_query(callback_query.id)
    txt = callback_query.data.split("_")
    await callback_query.message.answer(text="Выберите номер серии для загрузки.", reply_markup=generate_series_keyboard(int(txt[2]), txt[3], txt[4], txt[1]))

@dp.callback_query_handler(lambda c: c.data[0] == "D")  # Обработка выбора серии
async def process_callback_translation_question(callback_query: types.CallbackQuery):
    print(f"[DOWNLOAD REQUEST] [{callback_query.message.from_user.id}] {callback_query.data}")
    await bot.answer_callback_query(callback_query.id)
    txt = callback_query.data.split("_")
    if txt[0] == "DS":
        await callback_query.message.answer(text="Поиск ссылки... (Это может занять около минуты)")
        await callback_query.message.answer(text=f"Загрузка доступна:\n<a href='{await get_download_link(txt[3], int(txt[1]), txt[2])}/{txt[4]}.mp4'>Скачать</a>\n"\
                "<b>Внимание!</b>\nСсылка будет доступна в течении <u>2-3 часов</u>. Также скорость загрузки будет ограничена сервером. (в зависимости от качества займёт от 7 до 20 минут на 24 минутную серию)",
                parse_mode="HTML")
        print(f"[DOWNLOAD REQUEST] [{callback_query.message.from_id}] SUCCESSFULLY  download link sended")
    elif txt[0] == "DA":
        await callback_query.message.answer(text="Ссылки на скачивание будут добавляться по мере их нахождения. Обратите внимание, что ссылка доступна в течении 2-3 часов.")
        for i in range(1, int(txt[1])+1):
            await callback_query.message.answer(text=f"Серия {i} --> <a href='{await get_download_link(txt[3], int(txt[1]), txt[2])}/{txt[4]}.mp4'>Скачать</a>", parse_mode="HTML")
        await callback_query.message.answer(text="Поиск ссылок завершён.\n<b>Внимание!</b>\nСкорость загрузки ограничена сервером. (в зависимости от качества займёт от 7 до 20 минут на 24 минутную серию)", parse_mode="HTML")
        print(f"[DOWNLOAD REQUEST] [{callback_query.message.from_id}] SUCCESSFULLY  download links sended")


@dp.message_handler()
async def echo(message: types.Message):
	await message.answer(message.text)

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)