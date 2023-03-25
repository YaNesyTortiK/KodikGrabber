from app.templates import texts, keyboards
from app.utils.kodik import (
    SearchBlockedError,
    NotFoundError,
    shikimori_search,
    get_serial_info,
    get_serial_shiki_info,
)

from aiogram import Router, types
from aiogram.filters import Text, Command


async def search(message: types.Message): 
    
    query = message.text.split(' ', 1)[1:]

    if not query:
        
        return await message.answer("Введите название аниме для поиска")
    
    await message.answer("Поиск...")
    
    try:
            
        search = shikimori_search(query.pop())
            
    except SearchBlockedError:
        
        text = f"Произошла ошибка поиска. Возможно результаты поиска содержат материалы 18+ и сайт заблокировал подключение. /help чтобы узнать как обойти ограничение."
    
    else:
        
        text = texts.generate_cool_search_list(search) 
        
    await message.answer(text, disable_web_page_preview=True)


async def pre_translation(message: types.Message):
    
    serial_id = message.text[9:]
    print(1)
    try:
        
        serial_info = await get_serial_info(serial_id)
        
    except NotFoundError:
        
        return await message.answer(text="Похоже этот сериал отсутствует в базе Kodik'а")
    print(1)
    try:
        
        data = await get_serial_shiki_info(serial_id)
        
    except SearchBlockedError:
        
        return await message.answer("Ошибка поиска данных в шикимори")
    print(1)
        
    repl = f"{data['name']}\nВыберите озвучку из доступных:"
    await message.answer_photo(
        data['pic'],
        caption=repl, 
        reply_markup=keyboards.generate_translations_inline_keyboard(serial_info['translations'], serial_info['series_count'], serial_id),
    )


async def get_quality(call: types.CallbackQuery):

    await call.answer()
    txt = call.data.split("_")
    
    if txt[3] == "-1": # -1 Если фильм. В таком случае пропускается выбор серии
        
        return await call.message.answer(
            f"Выбран перевод \"{txt[2]}\"\nВыберите качество", 
            reply_markup=keyboards.generate_quality_inline_keyboard_for_film(int(txt[3]), txt[1], txt[4]),
        )
        
    await call.message.answer(
        text=f"Выбран перевод \"{txt[2]}\"\nВыберите качество", 
        reply_markup=keyboards.generate_quality_inline_keyboard(int(txt[3]), txt[1], txt[4]),
    )


async def get_serie(call: types.CallbackQuery):
    
    await call.answer()
    txt = call.data.split("_")
    await call.message.answer(
        "Выберите номер серии для загрузки.", 
        reply_markup=keyboards.generate_series_keyboard(int(txt[2]), txt[3], txt[4], txt[1]),
    )


async def get_links(call: types.CallbackQuery, kodik):
    
    await call.answer()
    txt = call.data.split("_")
    
    if txt[0] == "DS":
        
        await call.message.answer(text="Поиск ссылки...")
        await call.message.answer(text=f"Загрузка доступна:\n<a href='https:{await kodik.get_source(txt[3], int(txt[1]), txt[2])}{txt[4]}.mp4?load=1'>Скачать</a>\n"\
                "<b>Внимание!</b> Cкорость загрузки будет ограничена сервером. (в зависимости от качества займёт от 7 до 20 минут на 24 минутную серию)",
                parse_mode="HTML")
        
    elif txt[0] == "DA":
        
        await call.message.answer(text="Ссылки на скачивание будут добавляться по мере их нахождения. (Займет некоторое время)")
        for i in range(1, int(txt[1])+1):
            
            await call.message.answer(text=f"Серия {i} --> <a href='https:{await kodik.get_source(txt[3], int(txt[1]), txt[2])}{txt[4]}.mp4?load=1'>Скачать</a>", parse_mode="HTML")
        
        await call.message.answer(text="Поиск ссылок завершён.\n<b>Внимание!</b>\nСкорость загрузки ограничена сервером. (в зависимости от качества займёт от 7 до 20 минут на 24 минутную серию)", parse_mode="HTML")


async def echo(message: types.Message):
    
	await message.answer(text="Для поиска введите /search и имя тайтла через пробел. (Пример: /search Наруто)")
 
 
def register(router: Router):

    router.message.register(search, Command("search"))
    router.message.register(pre_translation, Text(startswith="/download"))

    router.callback_query.register(get_quality, Text(startswith="T"))
    router.callback_query.register(get_serie, Text(startswith="Q"))
    router.callback_query.register(get_links, Text(startswith="D"))
    
    router.message.register(echo)
