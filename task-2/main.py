"""
This project will fetch latest 20 sport news from the varzesh3.com and will print in stdout
I just simply used built-in urllib instead of the requests or aiohttp library for reducing dependencies and
because it's just a one-time fetch for now.

For parsing xml I've used built-in xml.etree, other option is using BeautifulSoup which is a little bit faster.
Python version: 3.12
"""

import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass
class SportNews:
    publish_date: str
    link: str
    title: str


class SportNewsScraper:
    def __init__(self, url="https://www.varzesh3.com/rss/all"):
        self.url = url
        self.headers = {'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      f'(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

    def _fetch_rss(self) -> str | None:
        """
        This method will fetch rss data
        :return:
        """
        request = urllib.request.Request(self.url, headers=self.headers)

        try:
            with urllib.request.urlopen(request) as response:
                if response.status == 200:
                    return response.read().decode("utf-8")
                else:
                    print(f"Failed to fetch RSS: HTTP status {response.status}")
                    return None
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"URLError: {e.reason}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

    @staticmethod
    def _parse_news(data: str) -> list[SportNews]:
        """
        In this method we will parse the xml using xml.etree.ElementTree and return a list of SportNews
        :param data:
        :return:
        """
        parsed_data: list[SportNews] = []
        root = ET.fromstring(data)

        channel = root.find("channel")

        counter: int = 0
        for item in channel.findall("item"):
            if counter == 20:
                break
            parsed_data.append(
                SportNews(
                    publish_date=item.find("pubDate").text.strip(),
                    link=item.find("link").text.strip(),
                    title=item.find("title").text.strip(),
                )
            )
            counter += 1

        return parsed_data

    def crawl(self):
        """
        This method will start fetching the news data from varzesh3.com (in this case) and parse the news
        :return:
        """
        data = self._fetch_rss()
        if data:
            clean_data: list[SportNews] = self._parse_news(data)
            for i, news in enumerate(clean_data):
                print(f"{i + 1}: {news.publish_date} - {news.title} - {news.link}")

        else:
            print("Couldn't fetch news!")


scraper = SportNewsScraper()
scraper.crawl()
