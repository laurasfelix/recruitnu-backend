# looks up a company's logo given their name

from bs4 import BeautifulSoup
import requests

def lookup(name):
    list_query = []
    query = "What's " + name + "'s logo?"
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(query)
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    images = soup.findAll('img')

    for image in images:
        list_query.append(image.get('src'))
    return list_query[1]

# print(lookup("Jane Street"))