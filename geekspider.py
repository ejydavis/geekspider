import scrapy
import random
from message import email


class GeekSpider(scrapy.Spider):
    name = "geek spider"
    start_urls = ['https://www.geeksforgeeks.org/fundamentals-of-algorithms']
    results = []
    paired_results = []

    def parse(self, response):
        for content in response.css("div.site-content"):
            links = content.css("a ::text").getall()
            hrefs = content.css("a ::attr(href)").getall()
            self.results = dict(links=links, hrefs=hrefs)
            self.analyze_results()

    def analyze_results(self):
        links = self.results.get("links")
        hrefs = self.results.get("hrefs")
        paired_list = []
        links_len = len(links)
        for i in range(0, links_len-1):
            paired_list.append({
                'text': links[i],
                'href': hrefs[i],
            })
        self.paired_results = paired_list
        self.send_results()

    def send_results(self):
        rand_index = random.randint(1, len(self.paired_results)-1)
        text = self.paired_results[rand_index]["text"]
        href = self.paired_results[rand_index]["href"]
        email(name=str(text), href=str(href))

