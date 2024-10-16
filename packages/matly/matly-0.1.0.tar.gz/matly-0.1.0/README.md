# Matly

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