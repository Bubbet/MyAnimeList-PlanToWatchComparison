from requests import get
from json import loads
import concurrent.futures
from time import time
from bs4 import BeautifulSoup


def parse_url(user, any_bool=False):
    url = f'https://myanimelist.net/animelist/{user}'
    page = get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('table', class_='list-table')

    if results is None:
        print(f'{user} is a invalid or empty user, try again.')
        return []
    jso = loads(results.attrs['data-items'])
    ret = [thing['anime_title'] for thing in jso if thing['status'] == 6 or any_bool]
    return ret


with concurrent.futures.ThreadPoolExecutor() as executor:
    a = bool(input('Check for all?: (enter True to compare full lists, anything else will just do the plan to watch)'))
    x = executor.submit(parse_url, input('Enter the first username:'), any_bool=a)
    y = executor.submit(parse_url, input('Enter the second username:'), any_bool=a)
    print('Scraping Anime Lists...')
    start = time()
    titles1 = x.result()
    titles2 = y.result()
    print(f'Took {round(time()-start, 2)} Seconds')
    print(f'Animes both users have in {a and "common" or "planned to watch"}:')
    [print(title) for title in titles1 if title in titles2]
