# Matly

[![Discord](https://discord.com/api/guilds/1268404228683202570/embed.png)](https://discord.gg/Kuk2qXFjc5)
[![GitHub](https://img.shields.io/github/license/LunaStev/wson)](https://mit-license.org/)
[![YouTube](https://img.shields.io/badge/YouTube-LunaStev-red.svg?logo=youtube)](https://www.youtube.com/@luna-bee)
![PyPI](https://img.shields.io/pypi/v/matly.svg) 
![PyPI](https://img.shields.io/pypi/pyversions/matly.svg)

Matly is a user-friendly web scraping library designed to simplify the process of extracting data from web pages. With a clean and intuitive API, Matly makes it easy for both beginners and experienced developers to perform web scraping tasks.

## Features

- **Simple API**: Easily perform HTTP requests and parse HTML.
- **Data Extraction**: Retrieve data using CSS selectors.
- **Error Handling**: Built-in error handling for HTTP requests.
- **BeautifulSoup Integration**: Utilizes BeautifulSoup for HTML parsing.

## Installation

Install Matly using `pip`.
```bash
pip install matly
```

## Usage
Here’s a quick example of how to use Matly:
```py
from matly import get, parse, find

# Fetch the HTML content from a URL
html = get("https://example.com")

# Parse the HTML content
soup = parse(html)

# Find all <h1> elements
data = find(soup, "h1")

# Print the extracted data
print(data)
```
## License
This project is licensed under the MIT License.