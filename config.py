import requests
from bs4 import BeautifulSoup


# empty lists to be filled with parsed data from BS4 query
links = []
subtext = []

for page in range(1,5):
	'''Parses first 5 pages of HackerNews portal to scrape news data'''
    res = requests.get(f'https://news.ycombinator.com/news?p={page}')
    soup = BeautifulSoup(res.text, 'html.parser')
    article_links = soup.select('.storylink')
    article_subtext = soup.select('.subtext')
    links += article_links
    subtext += article_subtext


def sort_stories_by_votes(hnews_list):
	'''Generates list of news in descending oreder using lambda function'''
    return sorted(hnews_list, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
	'''Filters news with votes > 99 to be displayed on the front end page'''
    hnews_list = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hnews_list.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hnews_list)