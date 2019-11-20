import requests
from bs4 import BeautifulSoup


def get_links(keywords, url):
    # Get page with list of birds
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # Get URLs to specific bird wiki pages
    li_elems = soup.find_all('li')
    links = []

    for l in li_elems:
        a_elems = l.find_all('a')

        if a_elems:
            href = a_elems[0]['href']
            a_text = str(a_elems[0].text).lower()

            if '#' not in href and any([kw in a_text for kw in keywords]):
                full_url = f'https://en.wikipedia.org/{href}'
                links.append(full_url)

    return links


def get_urls_by_family(family_keywords, url):
    # Get URLs of bird wiki pages by each family
    family_links = dict()

    for fam in family_keywords:
        family_links[fam] = get_links(family_keywords[fam], url)

    return family_links


def get_texts(family_urls):
    family_content = dict()

    # Iterate by family
    for fam in family_urls:
        # Get content by species URL
        for url in family_urls[fam]:
            content = get_content_from_page(url)


def get_content_from_page(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    for e in soup.find_all('p'):
        print(e)
        print(e.text)
    return


def get_data():
    # Bird families
    families = ['Passerellidae', 'Anatidae']

    # Keywords to look for in each family
    keywords = [['sparrow', 'bunting', 'junco', 'towhee'],
                ['duck', 'goose', 'swan', 'teal', 'eider', 'scoter',
                 'goldeneye', 'merganser']]

    family_keywords = dict(zip(families, keywords))

    # Page with a list of species URLs
    url = "https://en.wikipedia.org/wiki/List_of_birds_of_the_United_States"

    # Get links by bird families
    family_urls = get_urls_by_family(family_keywords, url)

    # Get text in wiki pages of birds in each family
    get_texts(family_urls)



if __name__ == '__main__':
    get_data()
    exit(0)
