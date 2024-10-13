import requests
from bs4 import BeautifulSoup

SSR_URL = "https://www.nasa.gov/rss/dyn/breaking_news.rss"

NO_DATA = 'No data'


def fetch_ssr(url):
    try:
        ssr_response = requests.get(url)
        return ssr_response.text
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        print(f"Oops! Something got wrong: {e}")
        return None

def parse_ssr(ssr_content):
    soup = BeautifulSoup(ssr_content, "xml")
    items = soup.find_all("item")
    if not items:
        print("No feed items!")
        return None
    feed = []

    def parse_item(data, keyword):
        return data.find(keyword).text if data.find(keyword) else NO_DATA

    for item in items:
        title = parse_item(item, "title")
        link = parse_item(item, "link")
        creator = parse_item(item, "dc:creator")
        publish_date = parse_item(item, "pubDate")
        description = parse_item(item, "description")
        content = parse_item(item, "content:encoded")

        feed.append({
            "title": title,
            "link": link,
            "creator": creator,
            "description": description,
            "publish_date": publish_date,
            "content": content
        })
    return feed

def validate_feed(feed):
    for i, feed_item in enumerate(feed):
        if not all([feed_item.get("title"),
                    feed_item.get("link"),
                    feed_item.get("creator"),
                    feed_item.get("publish_date"),
                    feed_item.get("description"),
                    feed_item.get("content")]):
            print(f"Error: #{i + 1}: {feed_item}")
            return False
    return True

def display_feed(feed):
    def display_content(content):
        soup = BeautifulSoup(content, "html.parser")
        return soup.get_text(strip=True)
    for i, feed_item in enumerate(feed):
        print(f"Item {i + 1}\n"
              f"Title: {feed_item['title']}\n"
              f"Link: {feed_item['link']}\n"
              f"Creator: {feed_item['creator']}\n"
              f"Publish Date: {feed_item['publish_date']}\n"
              f"Description: {feed_item['description']}\n"
              f"Content: {display_content(feed_item['content'])}/n")
        print('*' * 20)


xml_content = fetch_ssr(SSR_URL)

parse_ssr(xml_content)

def init():
    content = fetch_ssr(SSR_URL)
    if content:
        feed = parse_ssr(content)
        if feed and validate_feed(feed):
            display_feed(feed)
        else:
            print("Error: Invalid data")
    else:
        print("Error: Cant load content")

init()

