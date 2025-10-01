import requests
from bs4 import BeautifulSoup
from html import unescape
from html.parser import HTMLParser


class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.strict = False
		self.convert_charrefs = True
		self.fed = []

	def handle_data(self, d):
		self.fed.append(d)

	def get_data(self):
		return ''.join(self.fed)


def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()


def fetch_news(keyword, urls):
	news = []
	for url in urls:
		try:
			response = requests.get(url, timeout=5)
			response.raise_for_status()
			soup = BeautifulSoup(response.content, 'xml')
			items = soup.find_all('item')
			for item in items:
				title = item.find('title')
				link = item.find('link')
				description = item.find('description')
				if title and (keyword is None or keyword.lower() in title.text.lower()):
					desc_text = description.text if description else ""
					desc_text = strip_tags(desc_text)
					desc_text = unescape(desc_text)
					news.append({
						'title': title.text,
						'link': link.text if link else "",
						'description': desc_text
					})
		except Exception as e:
			print(f"⚠️ Ошибка при запросе {url}: {e}")
			continue
	return news