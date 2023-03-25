def generate_watch_url(media_id: str, media_platform: str = "shikimori") -> str:
    if media_platform == "shikimori":
        return f"https://kodikdb.com/find-player?shikimoriID={media_id}&only_season=false"
    else:
        raise KeyError(f"Can't find search platform '{media_platform}'")

def generate_cool_search_list(search_result: list) -> str:
    """Returns string of serials ordered by date with urls to visit site, watch, /download[id]"""
    sorted_list = sorted(search_result, key=lambda d: d['date'] if d['date'] != "Не указано" else "0", reverse=True) 
    repl = "Результат поиска: (Сортировка по дате выхода) (Поиск: <a href='shikimori.one'>Шикимори</a>)\n"
    for ind, dat in enumerate(sorted_list):
        repl += f"{ind+1}) <b>{dat['name']}</b>\n--Дата выхода: {dat['date']}\n--Тип: {dat['m_type']}\n"\
            f"--><a href='{dat['page_url']}'>Шикимори</a> | <a href='{generate_watch_url(dat['id'])}'>Смотреть онлайн</a> | Скачать: /download{dat['id']}\n\n"
    return repl


START = 'Для поиска введите /search и имя тайтла через пробел'
HELP = '''
Для поиска введите /search и имя тайтла через пробел. (Пример: /search Наруто)

Если вам написали что в поиске присутствуют материалы 18+, попробуйте указать более конкретное название или добавить номер сезона.
 
Если это не помогло, попробуйте получить id вручную. Для этого перейдите на сайт <a href='shikimori.one/animes'>Шикимори</a> и найдите там нужный сериал.
Зайдите на его страницу, и в адресной строке браузера, (https://shikimori.one/animes/30-neon-genesis-evangelion) вам нужно взять часть после "animes/" и перед "-". (В данном случае это 30)
Далее ведите команду /dowload подставив полученное id после слова <b><u>БЕЗ ПРОБЕЛА!</u></b> (В данном случае команда будет выглядеть так: /download30)
'''
AUTHORS = '''
Авторы: YaNesyTortiK, @le_bifle
Github проекта: https://github.com/YaNesyTortiK/KodikGrabber
Telegram: @nesy_tortik
'''
