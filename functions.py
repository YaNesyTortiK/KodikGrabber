from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from bs4 import BeautifulSoup as Soup


class SearchBlockedError(Exception):
    def __init__(self, message: str = None):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
    
class NotFoundError(Exception):
    def __init__(self, message: str = None):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

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

def generate_translations_inline_keyboard(translations: list, series_count: int, serial_id: str) -> InlineKeyboardMarkup:
    """Callback: T_t['id']_t['name']_{series_count}_{serial_id}"""
    keyboard = InlineKeyboardMarkup()
    for t in translations:
        btn = InlineKeyboardButton(text=t['name'], callback_data=f"T_{t['id']}_{t['name']}_{series_count}_{serial_id}")
        keyboard.add(btn)
    return keyboard

def generate_quality_inline_keyboard(series_count: int, translation_id: str, serial_id: str) -> InlineKeyboardMarkup:
    """Callback: Q_720/480/360_{series_count}_{translation_id}_{serial_id}"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("720p", callback_data=f"Q_720_{series_count}_{translation_id}_{serial_id}"))
    keyboard.add(InlineKeyboardButton("480p", callback_data=f"Q_480_{series_count}_{translation_id}_{serial_id}"))  
    keyboard.add(InlineKeyboardButton("360p", callback_data=f"Q_360_{series_count}_{translation_id}_{serial_id}"))
    return keyboard

def generate_quality_inline_keyboard_for_film(series_count: int, translation_id: str, serial_id: str) -> InlineKeyboardMarkup:
    """Callback: DS_{0}_{translation_id}_{serial_id}_720"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("720p", callback_data=f"DS_{0}_{translation_id}_{serial_id}_720"))
    keyboard.add(InlineKeyboardButton("480p", callback_data=f"DS_{0}_{translation_id}_{serial_id}_480"))  
    keyboard.add(InlineKeyboardButton("360p", callback_data=f"DS_{0}_{translation_id}_{serial_id}_360"))
    return keyboard

def generate_series_keyboard(series_count: int, translation_id: str, serial_id: str, quality: str):
    """callback_data: DA(S)_{series_count}/{seria_num}_{translation_id}_{serial_id}_{quality}"""
    keyboard = InlineKeyboardMarkup()
    for i in range(1, series_count+1):
        keyboard.add(InlineKeyboardButton(i, callback_data=f"DS_{i}_{translation_id}_{serial_id}_{quality}"))
    if series_count <= 12:
        keyboard.add(InlineKeyboardButton("Скачать все", callback_data=f"DA_{series_count}_{translation_id}_{serial_id}_{quality}"))
    return keyboard

def is_serial(iframe_url: str) -> bool:
    return True if iframe_url[iframe_url.find(".info/")+6] == "s" else False

def is_video(iframe_url: str) -> bool:
    return True if iframe_url[iframe_url.find(".info/")+6] == "v" else False

def generate_translations_dict(series_count: int, translations_div: Soup) -> dict:
    """Returns: {'series_count': series_count, 'translations': translations}"""
    if not isinstance(translations_div, list):
        translations = []
        for translation in translations_div:
            a = {}
            a['id'] = translation['value']
            a['type'] = translation['data-translation-type']
            a['name'] = translation.text
            translations.append(a)
    else:
        translations = [{"id": "-1", "type": "Неизвестно", "name": "Неизвестно"}]

    return {'series_count': series_count, 'translations': translations}