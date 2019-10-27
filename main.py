import requests
import urllib.request
import time
from bs4 import BeautifulSoup


def main():
    # TODO auto endpoint generation

    # print(five_start_Arthas()))
    # print(most_popular_monitor())
    # habr_python_articles()


def habr_python_articles():
    pageid = 1

    for pageid in range(1, 10):
        url = 'https://habr.com/en/all/page%d/' % pageid
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for headline_tag in soup.findAll('a', {'class': 'post__title_link'}):
            result = str(headline_tag.contents).find('Python')
            # TODO if else continue one line statement
            # print(str(headline_tag.contents) + '\n\t' + headline_tag['href']) if result > 0 else continue
            if result > 0:
                print(str(headline_tag.contents) +
                      '\n\t' + headline_tag['href'])
            else:
                continue


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
    for pageid in range(0, 600, 40):
        url = 'https://forum.overclockers.ua/viewforum.php?f=11&start=%d' % pageid
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for headline_tag in soup.findAll('a', {'class': 'topictitle'}):
            flag = False
            for monitor in monitors_dict:
                result = str(headline_tag.contents).upper().find(monitor)
                if result > 0:
                    monitors_dict[monitor] += 1
                    flag = True
                    break
            if flag:
                monitors_dict['OTHER'] += 1
    # TODO return value by key
    return monitors_dict


def five_start_Arthas(address):
    url = 'https://myshows.me/AI_Avenger/wasted'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    five_stars_shows = []
    for a in soup.findAll('a'):
        if a.parent.parent.name == 'tr':
            for _ in a.parent.parent.findAll('span', {'class': 'stars _5'}):
                five_stars_shows.append(a.contents)
    return five_stars_shows


if __name__ == "__main__":
    main()
