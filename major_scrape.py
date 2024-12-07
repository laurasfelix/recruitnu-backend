#scraping all majors from northwestern website
# https://catalogs.northwestern.edu/undergraduate/programs-az/

import requests
from bs4 import BeautifulSoup

url = "https://catalogs.northwestern.edu/undergraduate/programs-az/"

def scrape():
    try:
        page = requests.get(url)

        if page.status_code == 200:

            result = []

            soup = BeautifulSoup(page.text, 'html.parser')

            programs = soup.find('div', class_="az_sitemap")

            major_lists = programs.find_all('ul')

            for i in major_lists:
                major_items = i.find_all('li')
                text = [item.get_text(strip=True) for item in major_items]
                result += text

            return result[27:]


        else:
            print("DID NOT WORK", page.status_code)
            return []

    except Exception as e:
        raise Exception("an error ocurred") from e 

# print(scrape())