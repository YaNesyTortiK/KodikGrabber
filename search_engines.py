import requests
from bs4 import BeautifulSoup as Soup
import lxml
import aiohttp
from functions import SearchBlockedError, NotFoundError
from functions import is_serial, is_video, generate_translations_dict
import json
import asyncio
import requests


def shikimori_search(name: str) -> list:
    """
    Returns a list of dictionaries like {"name": "str", "id": "str", "date": "str", "m_type": "str", "page_url": "str"}
    Example: [
        {'name': 'Overlord', 'id': '29803', 'date': '2015', 'm_type': 'TV Сериал'},
        {'name': 'Overlord: Ple Ple Pleiades - Nazarick Saidai no Kiki', 'id': '33372', 'date': '2016', 'm_type': 'OVA'},
        {'name': 'Overlord Movie 1: Fushisha no Ou', 'id': '34161', 'date': '2017', 'm_type': 'Фильм'},
        {'name': 'Overlord Movie 2: Shikkoku no Eiyuu', 'id': '34428', 'date': '2017', 'm_type': 'Фильм'},
        {'name': 'Overlord II', 'id': '35073', 'date': '2018', 'm_type': 'TV Сериал'},
    ]
    """
    shikimnori_search_url = "https://shikimori.one/animes/order-by/aired_on"
    headers = {
        "authority": "shikimori.one",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "ru-RU,ru;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "_ga=GA1.2.2044361286.1672919141; _gid=GA1.2.524894347.1672919141; _ym_uid=1672919141674942935; _ym_d=1672919141; _ym_isad=2; i5=1672919155x1672919164x1672919183; _kawai_session=pBxL1MzaJkigcJdciMAHeZFHEQ6AqoobkJzACdTGxAlETKDY919H4bL9GSWrz9l1tYlfHd^%^2FfMdWKU7GbzCbir32KT3vN0EYvcOVC^%^2B5xzYDS9blhxM9o4ivxVG4GCE^%^2BNSeuKJArTsueb^%^2Bprv5qKo5LE9H4Phb^%^2FjEJRbfgVehgx7BE^%^2BIk7DQVxC9G88Hkis2uCSVMMeZxR7DKaSJaRo2DYju8OfxEj5UlmMc2CQFnS2VQVokTL770tpheSn6YbGtd^%^2BFAiM7nSdxUx6D1z7YV2gghKUDREdWWfBhdfnM0fWH3fjvVpWgTpbKV3P2pgCa7b^%^2FuDgdg0aaRN9dWUtkTXZhgenRKdupvTl9f6BUFJAPgZEL--v^%^2BU9HEAjm7ONHiap--do4Wm75dJ2CoAVena^%^2B^%^2Ft7g^%^3D^%^3D",
        "if-none-match": "W/\"7b8b10e73b71517e84679fa6791e77a1\"",
        "referer": "https://yandex.ru/",
        "sec-ch-ua": "\"Opera GX\";v=\"93\", \"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"107\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx GX)",
    }
    response = requests.get(shikimnori_search_url, params={"search": name}, headers=headers).text
    soup = Soup(response, "lxml")
    cont = soup.find("div", {"class": "cc-entries"})
    movies = [
        # {"name": "A", "id": 1, "date": "2015", "m_type": "TV сериал"}
    ]
    try:
        for art in list(cont.find_all_next("article")):
            movie = {"name": None, "id": None, "date": None, "m_type": None}
            try:
                movie["name"] = art.find("a", {"class": "title left_aligned"}).text
                movie["id"] = art["id"]
                movie["date"] = art.find("span", {"class": "right"}).text
                if movie["date"] == '':
                    movie["date"] = "Не указано"
                movie["m_type"] = art.find_all("span")[-1].text
                movie["page_url"] = art.find("a", href=True)['href']
            except:
                movie["name"] = art.find("span", {"class": "title left_aligned"}).text
                movie["id"] = art["id"]
                movie["date"] = art.find("span", {"class": "right"}).text
                if movie["date"] == '':
                    movie["date"] = "Не указано"
                movie["m_type"] = art.find_all("span")[-1].text
                movie["page_url"] = art.find("a", href=True)['href']
            movies.append(movie)
    except AttributeError:
        raise SearchBlockedError
    return movies


async def get_url_data(url: str):
    """Returns scrapped data from url"""
    async with aiohttp.ClientSession() as session:
        print(1, 'GETTING', url)
        data = await session.get(url)
        print(2, 'SUCCESS')
    return await data.text()

def post_url_data(url: str, params):
    """posts data to url"""
    print(1, 'POSTING: ', url, 'PARAMS: ', params)
    data = requests.post(url=url, params=params)
    print(2, 'SUCCESS')
    return data


async def get_link_to_serial_info(shikimoriID: str):
    token="447d179e875efe44217f20d1ee2146be"
    serv = f"https://kodikapi.com/get-player?title=Player&hasPlayer=false&url=https%3A%2F%2Fkodikdb.com%2Ffind-player%3FshikimoriID%3D{shikimoriID}&token={token}&shikimoriID={shikimoriID}"
    data = await get_url_data(serv)
    return data

async def get_serial_info(shikimoriID: str) -> dict:
    """Returns dict {'series_count': int, 'translations': [{'id': 'str', 'type': 'str', 'name': 'str'}, ...]}
    If series_count == -1, then it's a video (doesn't have series)
    """
    url = await get_link_to_serial_info(shikimoriID)
    url = json.loads(url)
    is_found = url['found']
    if not is_found:
        raise NotFoundError
    else:
        url = url['link']
        url = "https:"+url
        data = await get_url_data(url)
        soup = Soup(data, 'lxml')
        if is_serial(url):
            print('SERIAL')
            series_count = len(soup.find("div", {"class": "serial-series-box"}).find("select").find_all("option"))
            translations_div = soup.find("div", {"class": "serial-translations-box"}).find("select").find_all("option")
            print(translations_div)
            return generate_translations_dict(series_count, translations_div)
        elif is_video(url):
            print('VIDEO')
            series_count = -1
            try:
                translations_div = soup.find("div", {"class": "movie-translations-box"}).find("select").find_all("option")
            except AttributeError:
                translations_div = [{"name": "Неизвестно", "id": "-1"}]
            return generate_translations_dict(series_count, translations_div)
        else:
            print("NOT A VIDEO NOR A SERIAL!!!")
            raise NotFoundError("NOT A VIDEO NOR A SERIAL!!!")
        

async def get_serial_shiki_info(shikimoriID: str):
    """Returns main picture src and score of serial"""
    url = f"https://shikimori.one/animes/{shikimoriID}"
    data = await get_url_data(url)
    soup = Soup(data, 'lxml')
    if soup.find("p", {"class": "error-404"}) != None:
        url = soup.find("a")['href']
        data = await get_url_data(url)
        soup = Soup(data, 'lxml')

    try:
        name = soup.find('header', {'class': 'head'}).find('h1').text
        try:
            picture = soup.find('div', {"class": 'c-poster'}).find("div")['data-href']
        except:
            picture = soup.find('div', {"class": 'c-poster'}).find("img")['src']
        score = soup.find('div', {'class': 'text-score'}).find('div').text
    except:
        raise SearchBlockedError("Ошибка поиска по шики")
    return {"name": name, "pic": picture, "score": score}
