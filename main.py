import requests
import time
from bs4 import BeautifulSoup

def dota_winners_test():
    url = 'https://dotabuff.com/esports/matches?page=%d' % 54
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.121 Safari/537.36 Vivaldi/2.8.1664.44'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    headline_tags = soup.findAll(
        'span', {'class': 'team-text team-text-full'})
    for headline_tag in headline_tags:
        if len(headline_tags) == 0:
            return 'headline_tag'
        if str(headline_tag.parent.parent['class']).find('radiant') > 0 and str(headline_tag.parent.parent.parent['class']).find('winner') > 0:
            return 'fdkjs'


def dota_winners():
    radiant_winners = 0
    overall_count = 0
    pageid = 48
    while (True):
        print(pageid)
        url = 'https://dotabuff.com/esports/matches?page=%d' % pageid
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.121 Safari/537.36 Vivaldi/2.8.1664.44'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        headline_tags = soup.findAll(
            'span', {'class': 'team-text team-text-full'})
        for headline_tag in headline_tags:
            if len(headline_tags) == 0:
                print('headline_tag')
            if str(headline_tag.parent.parent['class']).find('radiant') > 0 and str(headline_tag.parent.parent.parent['class']).find('winner') > 0:
                radiant_winners += 1
        overall_count += 20
        pageid += 1
        percent=radiant_winners / overall_count
    return percent


def habr_python_articles():
    pageid=1

    for pageid in range(1, 10):
        url='https://habr.com/en/all/page%d/' % pageid
        response=requests.get(url)
        soup=BeautifulSoup(response.text, 'html.parser')
        for headline_tag in soup.findAll('a', {'class': 'post__title_link'}):
            result=str(headline_tag.contents).find('Python')
            # TODO if else continue one line statement
            # print(str(headline_tag.contents) + '\n\t' + headline_tag['href']) if result > 0 else continue
            if result > 0:
                print(str(headline_tag.contents) +
                      '\n\t' + headline_tag['href'])
            else:
                continue


def most_popular_monitor():
    monitors_dict={
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
    pageid=0
    for pageid in range(0, 600, 40):
        url='https://forum.overclockers.ua/viewforum.php?f=11&start=%d' % pageid
        response=requests.get(url)
        soup=BeautifulSoup(response.text, 'html.parser')
        for headline_tag in soup.findAll('a', {'class': 'topictitle'}):
            flag=False
            for monitor in monitors_dict:
                result=str(headline_tag.contents).upper().find(monitor)
                if result > 0:
                    monitors_dict[monitor] += 1
                    flag=True
                    break
            if flag:
                monitors_dict['OTHER'] += 1
    # TODO return value by key
    return monitors_dict


def five_start_Arthas():
    url='https://myshows.me/AI_Avenger/wasted'
    response=requests.get(url)
    soup=BeautifulSoup(response.text, 'html.parser')
    five_stars_shows=[]
    for a in soup.findAll('a'):
        if a.parent.parent.name == 'tr':
            for _ in a.parent.parent.findAll('span', {'class': 'stars _5'}):
                five_stars_shows.append(a.contents)
    return five_stars_shows


if __name__ == "__main__":
    # TODO auto endpoint generation
    # print(most_popular_monitor())
    # habr_python_articles()
    print(dota_winners_test())
    # print(five_start_Arthas())
