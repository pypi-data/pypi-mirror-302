import requests
from bs4 import BeautifulSoup

class Matly:
    def get(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse(self, html):
        return BeautifulSoup(html,'html.parser')

    def find(self, soup, selector):
        return soup.select(selector)


def tests():
    matly = Matly()
    html = matly.get("https://example.com")
    soup = matly.parse(html)
    data = matly.find(soup, "h1")
    print(data)

if __name__ == "__main__":
    tests()