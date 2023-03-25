from bs4 import BeautifulSoup as Soup


class SearchBlockedError(Exception):
    def __init__(self, message: str = None):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
    
class NotFoundError(Exception):
    def __init__(self, message: str = None):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

def is_serial(iframe_url: str) -> bool:
    return True if iframe_url[iframe_url.find(".info/")+6] == "s" else False

def is_video(iframe_url: str) -> bool:
    return True if iframe_url[iframe_url.find(".info/")+6] == "v" else False

def generate_translations_dict(series_count: int, translations_div: Soup) -> dict:
    """Returns: {'series_count': series_count, 'translations': translations}"""
    if not isinstance(translations_div, Soup):
        
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