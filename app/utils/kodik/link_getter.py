import re
import aiohttp

from base64 import b64decode
from bs4 import BeautifulSoup


class KodikParser(object):
    
    API_URL = 'https://kodikapi.com/get-player'
    PLAYER_TEMPLATE = 'https://kodik.info/serial/%s/%s/720p'
    
    def __init__(self, token: str):

        self.token = token
        self.session = aiohttp.ClientSession()
        
        
    async def _get_player(self, shikimori_id: str) -> str:
        
        async with self.session.get(
            self.API_URL,
            params={
                'title': 'Player',
                'hasPlayer': 'false',
                'url': 'https://kodikdb.com/find-player?shikimoriID=%s' % shikimori_id,
                'token': self.token,
                'shikimoriID': shikimori_id,
            },
        ) as response:
            
            return (await response.json()).get('link')
        
        
    async def _scrape_player(self, player_url: str, translation: int) -> tuple:
        
        async with self.session.get('https:' + player_url) as response:
            
            html = await response.text()
            
        soup = BeautifulSoup(html, 'lxml')
        option = soup.find(
            'div', {'class': 'serial-translations-box'},
        ).find('option', {'data-id': str(translation)})
        
        return (
            option.get('data-media-id'),
            option.get('data-media-hash'),
        )
        
        
    async def _prepare_source(self, media_id: str, media_hash: str, serie: int) -> dict:
        
        async with self.session.get(
            self.PLAYER_TEMPLATE % (media_id, media_hash),
            params={
                'd': 'kodik.cc',
                'd_sign': '9945930febce35101e96ce0fe360f9729430271c19941e63c5208c2f342e10ed',
                'pd': 'kodik.info',
                'pd_sign': '09ffe86e9e452eec302620225d9848eb722efd800e15bf707195241d9b7e4b2b',
                'ref': '',
                'ref_sign': '208d2a75f78d8afe7a1c73c2d97fd3ce07534666ab4405369f4f8705a9741144',
                'advert_debug': 'true',
                'first_url': 'false',
                'episode': serie,
            },
        ) as response:
            
            html = await response.text()
            
        soup = BeautifulSoup(html, 'lxml')
        target_script = soup.find_all('script')[4].text
        
        variable_names = ('type', 'hash', 'id')
        return {
            variable: re.search(
                fr'.{variable} = \'(.+?)\'', 
                target_script
            ).group(1)
            for variable in variable_names
        }
        
        
    async def _get_direct_link(self, id: str, hash: str, type: str) -> str:
        
        async with self.session.post(
            'https://kodik.cc/gvi',
            params={
                "id": id, 
                "hash": hash,
                "quality": "720p",
                "type": type,
                "protocol": "",
                "host": "kodik.cc",
                "d": "kodik.cc",
                "d_sign": "9945930febce35101e96ce0fe360f9729430271c19941e63c5208c2f342e10ed",
                "pd": "kodik.cc",
                "pd_sign": "9945930febce35101e96ce0fe360f9729430271c19941e63c5208c2f342e10ed",
                "ref": "",
                "ref_sign": "208d2a75f78d8afe7a1c73c2d97fd3ce07534666ab4405369f4f8705a9741144",
                "advert_debug": 'true',
                "first_url": 'false',
            }
        ) as response:
            
            data = await response.json(content_type=None)
            
            encrypted_link = data['links']['720'][0]['src']
            return b64decode(
                encrypted_link[::-1].encode() + b'=='
            ).decode()
 

    async def get_source(self, shikimori_id: str, serie: int, translation: int) -> str:

        player_url = await self._get_player(shikimori_id)
        media_id, media_hash = await self._scrape_player(
            player_url, translation,
        )
        source_data = await self._prepare_source(
            media_id, media_hash, serie,
        )
        
        return await self._get_direct_link(**source_data)
