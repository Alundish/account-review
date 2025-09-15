import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    if not url or not isinstance(url, str):
        return None
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            text = soup.get_text(separator=' ')
            return ' '.join(text.split())
    except requests.RequestException:
        return None

