import wstools
import asyncio
import time


async def __work_ua_coroutine__(works_dict, url, pageid):
    soup = await wstools.async_site_soup(url, pageid=pageid)
    headline_tags = soup.findAll('h2', {'class': 'add-bottom-sm'})
    if not headline_tags:
        return
    for headline_tag in headline_tags:
        works_dict[headline_tag.find(
            'a')['title']] = 'https://www.work.ua' + headline_tag.find('a')['href']


async def work_ua(keyword, city):
    works_dict = {

    }
    url = 'https://www.work.ua/jobs-' + city + '-' + keyword + '/?page='
    tasks = [
        asyncio.create_task(__work_ua_coroutine__(works_dict, url, pageid)) for pageid in range(1, 20)
    ]
    await asyncio.wait(tasks)
    return works_dict


async def __djinni_coroutine__(works_dict, url, closer, pageid):
    soup = await wstools.async_site_soup(url, pageid=pageid, closer=closer)
    headline_tags = soup.findAll(
        'a', {'class': 'profile'})
    if headline_tags:
        for headline_tag in headline_tags:
            works_dict[headline_tag.contents[0]
                       ] = 'https://djinni.co/' + headline_tag['href']
    else:
        return


async def djinni(keyword, city):
    works_dict = {

    }
    url = 'https://djinni.co/jobs/?primary_keyword=' + keyword + '&page='
    closer = '&location=' + city
    tasks = [
        asyncio.create_task(__djinni_coroutine__(works_dict, url, closer, pageid)) for pageid in range(1, 20)
    ]
    await asyncio.wait(tasks)
    return works_dict


async def __rabota_ua_coroutine__(works_dict, site_url, pageid):
    soup = await wstools.async_site_soup(site_url, pageid)
    headline_tags = soup.findAll(
        'a', {'class': 'f-visited-enable ga_listing'})
    if headline_tags:
        for headline_tag in headline_tags:
            works_dict[headline_tag['title']
                       ] = 'https://rabota.ua' + headline_tag['href']
    else:
        return


# TODO range
async def rabota_ua(keyword, city=None):
    works_dict = {
    }
    if city is not None:
        site_url = 'https://rabota.ua/zapros/' + keyword + '/' + city + '/pg'
    else:
        site_url = 'https://rabota.ua/zapros/' + keyword + '/pg'
    tasks = [
        asyncio.create_task(__rabota_ua_coroutine__(works_dict, site_url, pageid)) for pageid in range(1, 20)
    ]
    await asyncio.wait(tasks)
    return works_dict

#cant be async'ed
def dou_jobs(keyword, city):
    works_dict = {

    }
    driver = wstools.set_up_chrome_driver()
    url = 'https://jobs.dou.ua/vacancies/?city=' + city + '&category=' + keyword
    driver.get(url)
    try:
        time.sleep(0.1)
        continue_link = driver.find_element_by_link_text('Больше вакансий')
        while continue_link.is_displayed():
            continue_link.click()
            time.sleep(0.1)
    except wstools.selenium.common.exceptions.NoSuchElementException:
        print('eos')

    html = driver.execute_script("return document.body.outerHTML;")
    soup = wstools.BeautifulSoup(html, 'html.parser')
    headline_tags = soup.findAll('a', {'class': 'vt'})
    for headline_tag in headline_tags:
        works_dict[headline_tag.contents[0]] = headline_tag['href']
    return works_dict
