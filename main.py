import time
import asyncio


from datetime import date

import wstools
import works
import dota

from bs4 import BeautifulSoup


# TODO Async scrapping (STOP RANGE)
# TODO City name parcing (work.ua , ...)


async def habr_coroutine(headline_link_dict, pageid, find_value):
    soup = await wstools.async_site_soup('https://habr.com/en/all/page', pageid=pageid)
    for headline_tag in soup.findAll('a', {'class': 'post__title_link'}):
        result = str(headline_tag.contents).lower().find(
            find_value.lower())
        if result > 0:
            headline_link_dict[str(headline_tag.contents[0])
                               ] = headline_tag['href']
        else:
            continue


# TODO range
async def habr_python_articles(find_value):
    headline_link_dict = {
    }
    tasks = [
        asyncio.create_task(habr_coroutine(headline_link_dict, i, find_value)) for i in range(1, 20)
    ]
    await asyncio.wait(tasks)
    return headline_link_dict


async def monitor_coroutine(monitors_dict, pageid):
    soup = await wstools.async_site_soup(
        'https://forum.overclockers.ua/viewforum.php?f=11&start=', pageid=pageid)
    headline_tags = soup.findAll('a', {'class': 'topictitle'})

    if soup.find('li', {'class': 'next'}) is None:
        return

    for headline_tag in headline_tags:
        flag = False
        for monitor in monitors_dict:
            result = str(headline_tag.contents).upper().find(monitor)
            if result > 0:
                monitors_dict[monitor] += 1
                flag = True
                break
        if flag:
            monitors_dict['OTHER'] += 1


async def most_popular_monitor():
    monitors_dict = {
        'MSI': 0, 
        'DELL': 0,
        'SAMSUNG': 0,
        'AOC': 0,
        'VIEWSONIC': 0,
        'LG': 0,
        'ASUS': 0,
        'ACER': 0,
        'BENQ': 0,
        'PHILIPS': 0,
        'OTHER': 0
    }

    tasks = [
        asyncio.create_task(monitor_coroutine(monitors_dict, i)) for i in range(1, 600, 40)
    ]
    await asyncio.wait(tasks)
    return monitors_dict


#no sense to async
def five_stars_Arthas():
    soup = wstools.sync_site_soup('https://myshows.me/AI_Avenger/wasted')
    five_stars_shows = []
    for a in soup.findAll('a'):
        if a.parent.parent.name == 'tr':
            for _ in a.parent.parent.findAll('span', {'class': 'stars _5'}):
                five_stars_shows.append(a.contents[0])
    return five_stars_shows


def main():
    city = 'Киев'
    keyword = 'Python'

    dict = works.dou_jobs(keyword, city)

    ioloop = asyncio.get_event_loop()
    # articles = ioloop.run_until_complete(habr_python_articles('python'))
    # value = ioloop.run_until_complete(dota.dota_radiant_winrate())
    # monitors = ioloop.run_until_complete(most_popular_monitor())
    # async_dota_news_dict = ioloop.run_until_complete(dota.dota_news('lil'))
    # rabota_ua_dict = ioloop.run_until_complete(works.rabota_ua('java', city='киев'))
    # djinni_dict = ioloop.run_until_complete(works.djinni('Python', 'Одесса'))
    # work_ua_dict = ioloop.run_until_complete(works.work_ua('python', city='odesa'))

    #ioloop.close()
    for x in dict:
        print(x + "\t" + str(dict[x]))

    # print(five_start_Arthas())


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
