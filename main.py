import requests
import time

from bs4 import BeautifulSoup
from datetime import date



def soup_site(address, pageid=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.78 Safari/537.36 Vivaldi/2.8.1664.35'
    }
    if pageid:
        url = '%s%s' % (address, pageid)
    else:
        url = address

    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')


def dota_news(find_value):
    pageid = 1
    current_date = published_date = date.today()
    news_dict = {

    }

    months_dict = {
        'янв': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'мая': 5,
        'июн': 6,
        'июл': 7,
        'авг': 8,
        'сен': 9,
        'окт': 10,
        'нояб': 11,
        'дек': 12
    }

    while(True):
        soup = soup_site('https://dota2.net/allnews?page=', pageid=pageid)
        time_tags = soup.select("div[class=news-item__statistics]")

        for time_tag in time_tags:
            published = time_tag.contents[0]
            for month in months_dict:
                if published.find(month) >= 0:
                    published_date = date(
                        current_date.year, months_dict[month], int(published.split()[0]))
        if (current_date - published_date).days > 30:
            break

        headline_tags = soup.findAll(
            'a', {'class': 'news-item__title'})
        for headline_tag in headline_tags:
            title = str(headline_tag.contents[0])
            if title.lower().find(find_value.lower()) >= 0:
                news_dict[headline_tag.contents[0]] = headline_tag['href']

        pageid += 1
    return news_dict


def dota_radiant_winrate():
    radiant_winners = 0
    overall_games_count = 0
    pageid = 1

    while (True):
        soup = soup_site('https://www.dotabuff.com/esports/matches?page=',
                         pageid=pageid)
        headline_tags = soup.findAll(
            'span', {'class': 'team-text team-text-full'})

        if not headline_tags:
            break

        for headline_tag in headline_tags:
            if str(headline_tag.parent.parent['class']).find('radiant') > 0 \
                    and str(headline_tag.parent.parent.parent['class']).find('winner') > 0:
                radiant_winners += 1
        overall_games_count += 20

        pageid += 1

    if overall_games_count != 0:
        return radiant_winners / overall_games_count
    else:
        return 0


def habr_python_articles(find_value):
    pageid = 1
    headline_link_dict = {
    }
    for pageid in range(1, 10):
        soup = soup_site('https://habr.com/en/all/page', pageid=pageid)
        for headline_tag in soup.findAll('a', {'class': 'post__title_link'}):
            result = str(headline_tag.contents).lower().find(find_value.lower())
            if result > 0:
                headline_link_dict[str(headline_tag.contents)
                                   ] = headline_tag['href']
            else:
                continue
    return headline_link_dict


def most_popular_monitor():
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
    pageid = 0
    # stupid stop
    for pageid in range(0, 600, 40):
        url = 'https://forum.overclockers.ua/viewforum.php?f=11&start=%d' % pageid
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        headline_tags = soup.findAll('a', {'class': 'topictitle'})
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
        pageid += 1
    # TODO return value by key
    return monitors_dict


def five_start_Arthas():
    soup = soup_site('https://myshows.me/AI_Avenger/wasted')
    five_stars_shows = []
    for a in soup.findAll('a'):
        if a.parent.parent.name == 'tr':
            for _ in a.parent.parent.findAll('span', {'class': 'stars _5'}):
                five_stars_shows.append(a.contents)
    return five_stars_shows


if __name__ == "__main__":
    # dict = most_popular_monitor()
    # dict = habr_python_articles('vue.js')
    # for x in dict:
    #     print(x + "\t" + str(dict[x]))
    # dict = dota_news('lil')
    # for x in dict:
    #     print(x + str(dict[x]))
    # print(dota_radiant_winrate())
    print(five_start_Arthas())
