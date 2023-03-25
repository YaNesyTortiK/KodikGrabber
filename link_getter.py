from search_engines import get_url_data, post_url_data
import json
from bs4 import BeautifulSoup as Soup
from base64 import b64decode

async def get_download_link(shikimori_id: str, seria_num: int, translation_id: str):
    token="447d179e875efe44217f20d1ee2146be"
    serv = f"https://kodikapi.com/get-player?title=Player&hasPlayer=false&url=https%3A%2F%2Fkodikdb.com%2Ffind-player%3FshikimoriID%3D{shikimori_id}&token={token}&shikimoriID={shikimori_id}"
    data = await get_url_data(serv)
    url = json.loads(data)['link']
    data = await get_url_data('https:'+url)
    soup = Soup(data, 'lxml')
    container = soup.find('div', {'class': 'serial-translations-box'})
    media_hash = None
    media_id = None
    for translation in container.find_all('option'):
        if translation.get_attribute_list('data-id')[0] == translation_id:
            media_hash = translation.get_attribute_list('data-media-hash')[0]
            media_id = translation.get_attribute_list('data-media-id')[0]
            break

    url = f'https://kodik.info/serial/{media_id}/{media_hash}/720p?d=kodik.cc&d_sign=9945930febce35101e96ce0fe360f9729430271c19941e63c5208c2f342e10ed&pd=kodik.info&pd_sign=09ffe86e9e452eec302620225d9848eb722efd800e15bf707195241d9b7e4b2b&ref=&ref_sign=208d2a75f78d8afe7a1c73c2d97fd3ce07534666ab4405369f4f8705a9741144&advert_debug=true&min_age=16&first_url=false&season=1&episode={seria_num}'
    data = await get_url_data(url)
    soup = Soup(data, 'lxml')
    hash_container = soup.find_all('script')[4].text
    video_type = hash_container[hash_container.find('.type = \'')+9:]
    video_type = video_type[:video_type.find('\'')]
    video_hash = hash_container[hash_container.find('.hash = \'')+9:]
    video_hash = video_hash[:video_hash.find('\'')]
    video_id = hash_container[hash_container.find('.id = \'')+7:]
    video_id = video_id[:video_id.find('\'')]

    download_url = str(await get_download_link_with_data(video_type, video_hash, video_id))
    download_url = download_url[2:-26] # :hls:manifest.m3u8

    return download_url

async def get_download_link_with_data(video_type: str, video_hash: str, video_id: str):
    params={
        "hash": video_hash, # "6476310cc6d90aa9304d5d8af3a91279"
        "id": video_id, # 19850
        "quality":"720p",
        "type":video_type, # video
        "protocol": '',
        "host":"kodik.cc",
        "d":"kodik.cc",
        "d_sign":"9945930febce35101e96ce0fe360f9729430271c19941e63c5208c2f342e10ed",
        "pd":"kodik.cc",
        "pd_sign":"9945930febce35101e96ce0fe360f9729430271c19941e63c5208c2f342e10ed",
        "ref": '',
        "ref_sign":"208d2a75f78d8afe7a1c73c2d97fd3ce07534666ab4405369f4f8705a9741144",
        "advert_debug": True,
        "first_url": False,
    }

    data = post_url_data('http://kodik.cc/gvi', params=params).json()

    url = data['links']['720'][0]['src']
    return b64decode(url[::-1].encode() + b'==')