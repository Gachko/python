import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError, Field
from typing import List, Optional

SSR_URL = "https://www.nasa.gov/rss/dyn/breaking_news.rss"

NO_DATA = 'No data'

class MissingDataError(Exception):
    pass

class RSSItem(BaseModel):
    title: str
    link: str
    creator: Optional[str]
    description: Optional[str]
    publish_date: Optional[str]
    content: Optional[str]

class RSSChannel(BaseModel):
    title: str
    link: str
    description: str
    language: Optional[str]
    items: List[RSSItem]

def fetch_ssr(url):
    try:
        ssr_response = requests.get(url)
        ssr_response.raise_for_status()
        return ssr_response.text
    except requests.exceptions.RequestException as e:
        print(f"Oops! Something got wrong: {e}")


def parse_item(data, keyword):
    element = data.find(keyword)
    if element is None:
        raise MissingDataError(f"Missing required data: {keyword}")
    return element.text


def parse_ssr(ssr_content):
    soup = BeautifulSoup(ssr_content, "xml")
    channel = soup.find("channel")

    if channel is None:
        print("No channel found!")
        return []

    try:
        rss_channel = RSSChannel(
            title=parse_item(channel, "title"),
            link=parse_item(channel, "link"),
            description=parse_item(channel, "description"),
            language=parse_item(channel, "language") if channel.find("language") else None,
            items=[],
        )

        items = channel.find_all("item")
        for item in items:
            try:
                rss_item = RSSItem(
                    title=parse_item(item, "title"),
                    link=parse_item(item, "link"),
                    creator=parse_item(item, "dc:creator"),
                    description=parse_item(item, "description"),
                    publish_date=parse_item(item, "pubDate"),
                    content=parse_item(item, "content:encoded"),
                )
                rss_channel.items.append(rss_item)
            except MissingDataError as e:
                print(f"Error while parsing item: {e}")

        return rss_channel

    except MissingDataError as e:
        print(f"Error while parsing channel: {e}")
        return []

def display_content(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text(strip=True)

def display_feed(channel):
    print(f"Channel Title: {channel.title}")
    print(f"Channel Link: {channel.link}")
    print(f"Channel Description: {channel.description}\n")

    for i, feed_item in enumerate(channel.items):
        print(f"Item {i + 1}\n"
              f"Title: {feed_item.title}\n"
              f"Link: {feed_item.link}\n"
              f"Creator: {feed_item.creator}\n"
              f"Publish Date: {feed_item.publish_date}\n"
              f"Description: {feed_item.description}\n"
              f"Content: {display_content(feed_item.content)}\n")
        print('*' * 20)

xml_content = fetch_ssr(SSR_URL)

parse_ssr(xml_content)

def init():
    try:
        content = fetch_ssr(SSR_URL)
        if content:
            channel = parse_ssr(content)
            if channel:
                display_feed(channel)
            else:
                print("Error: Invalid data")
        else:
            print("Error: Can't load content")
    except MissingDataError as e:
        print(f"Error while parsing feed: {e}")

if __name__ == "__main__":
    init()

