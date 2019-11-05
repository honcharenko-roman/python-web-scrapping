import wstools
import asyncio

from datetime import date


async def __dota_winners_coroutine__(radiant_winners, overall_games, pageid):
    soup = await wstools.async_site_soup('https://www.dotabuff.com/esports/matches?page=',
                                 pageid=pageid)
    headline_tags = soup.findAll(
        'span', {'class': 'team-text team-text-full'})

    if not headline_tags:
        return

    for headline_tag in headline_tags:
        if str(headline_tag.parent.parent['class']).find('radiant') > 0 \
                and str(headline_tag.parent.parent.parent['class']).find('winner') > 0:
            radiant_winners.append(1)
    overall_games.append(20)


# TODO STOP RANGE mb flag!
# TODO FIRST LOOP INCORRECT VALUE
async def dota_radiant_winrate():
    radiant_winners = []
    overall_games = []

    tasks = [
        asyncio.create_task(__dota_winners_coroutine__(radiant_winners, overall_games, i)) for i in range(1, 50)
    ]
    await asyncio.wait(tasks)

    return sum(radiant_winners) / sum(overall_games)

async def __dota_news_coroutine__(news_dict, months_dict, find_value, pageid):
    current_date = published_date = date.today()
    soup = await wstools.async_site_soup('https://dota2.net/allnews?page=', pageid=pageid)
    time_tags = soup.select("div[class=news-item__statistics]")

    for time_tag in time_tags:
        published = time_tag.contents[0]
        for month in months_dict:
            if published.find(month) >= 0:
                published_date = date(
                    current_date.year, months_dict[month], int(published.split()[0]))

    if (current_date - published_date).days > 30:
        return 

    headline_tags = soup.findAll(
        'a', {'class': 'news-item__title'})
    for headline_tag in headline_tags:
        title = str(headline_tag.contents[0])
        if title.lower().find(find_value.lower()) >= 0:
            news_dict[headline_tag.contents[0]] = headline_tag['href']

#TODO RANGE!
async def dota_news(find_value):
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
    tasks = [
        asyncio.create_task(__dota_news_coroutine__(news_dict, months_dict, find_value, pageid)) for pageid in range(1, 27)
    ]
    await asyncio.wait(tasks)
    return news_dict
