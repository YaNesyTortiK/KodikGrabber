from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import asyncio
from search_engines import get_serial_info
from functions import is_serial, is_video

async def get_manifest_link(shikimori_id: str, seria_num: int, translation_id: str):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    # op.add_argument("user-data-dir=C:\\profile")
    op.add_argument("--mute-audio")
    # op.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=op)
    driver.implicitly_wait(15)
    driver.get(f"https://kodikdb.com/find-player?shikimoriID={shikimori_id}&only_season=false")

    # enter iframe
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    iframe_src = iframe.get_attribute("src")
    driver.switch_to.frame(iframe)

    if is_serial(iframe_src):
        print("Serial")
        # choose seria
        seria_box = driver.find_element(By.CLASS_NAME, 'serial-series-box')
        seria_box.click()
        seria_select = seria_box.find_element(By.TAG_NAME, 'select').find_elements(By.TAG_NAME, 'option')
        seria_select[seria_num-1].click()

        # choose translation
        translation_box = driver.find_element(By.CLASS_NAME, 'serial-translations-box')
        translation_box.click()
        translation_select = translation_box.find_element(By.TAG_NAME, 
            'select').find_elements(By.TAG_NAME, 'option')
        for t in translation_select:
            if t.get_attribute('value') == translation_id:
                t.click()
                break
    elif is_video(iframe_src):
        print("Video")
        if translation_id != "-1":
            # choose translation
            translation_box = driver.find_element(By.CLASS_NAME, 'movie-translations-box')
            translation_box.click()
            translation_select = translation_box.find_element(By.TAG_NAME, 
                'select').find_elements(By.TAG_NAME, 'option')
            for t in translation_select:
                if t.get_attribute('value') == translation_id:
                    t.click()
                    break
    else:
        print("NOT A VIDEO AND NOT A SERIAL!!!")
        raise AttributeError("NOT A VIDEO AND NOT A SERIAL!!!")
    
    # start video
    driver.find_element(By.TAG_NAME, 'a').click()
    
    await asyncio.sleep(12) # Wait for server to start playing

    url = None
    for request in driver.requests:
        if request.response:
            ur = request.url
            if ur.find(".cloud.kodik") != -1 and ur.find("manifest") != -1:
                url = ur
    print(url)
    driver.close()
    return url

async def get_download_link(shikimori_id: str, seria_num: int, translation_id: str):
    """
    return link without quality
    """
    data = await get_manifest_link(shikimori_id, seria_num, translation_id)
    if data != None:
        data = data[:data.rfind("/")]
        return data
    else:
        return 'Error'