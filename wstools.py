import requests
import aiohttp
import html5lib
import selenium

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def set_up_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=chrome_options)
    return driver

def sync_site_soup(address, pageid=None, closer=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.78 Safari/537.36 Vivaldi/2.8.1664.35'
    }
    if pageid and closer:
        url = '%s%s%s' % (address, pageid, closer)
    elif pageid:
        url = '%s%s' % (address, pageid)
    else:
        url = address
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')


async def async_site_soup(address, pageid=None, closer=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.78 Safari/537.36 Vivaldi/2.8.1664.35'
    }
    if pageid and closer:
        url = '%s%s%s' % (address, pageid, closer)
    elif pageid:
        url = '%s%s' % (address, pageid)
    else:
        url = address
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            text = await resp.read()

    return BeautifulSoup(text.decode('utf-8'), 'html5lib')