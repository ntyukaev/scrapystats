from scannerstats.utils import name_file
from scrapy import Spider, Request
from scrapy_splash import SplashRequest
import json


class CarsSpider(Spider):
    name = 'cars'

    def start_requests(self):
        urls = [
            'https://auto.ru/'
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        selectors = response.selector.xpath('//a[contains(@class, "IndexMarks__item")]/@href')
        manufacturers = list(map(lambda x: x.get().replace('all', 'used'), selectors))
        for manufacturer in manufacturers:
            yield SplashRequest(
                manufacturer,
                callback=self.parse_manufacturer
            )

    def parse_manufacturer(self, response):
        data = json.loads(response.selector.xpath('//script[contains(@id, "init")]/text()').get())
        file_name = name_file(response.request._original_url)
        with open('data/{file_name}'.format(file_name=file_name), 'w', encoding='utf-8') as f:
            json.dump(data['listing']['data']['offers'], f, ensure_ascii=False)
        total_page_count = data['listing']['data']['pagination']['total_page_count']
        original_url = response.request._original_url
        pages = (
            original_url + '?page=' + str(page) for page in range(2, total_page_count + 1))
        for page in pages:
            yield SplashRequest(
                page,
                callback=self.parse_page
            )

    def parse_page(self, response):
        data = json.loads(response.selector.xpath('//script[contains(@id, "init")]/text()').get())
        file_name = name_file(response.request._original_url)
        with open('data/{file_name}'.format(file_name=file_name), 'w', encoding='utf-8') as f:
            json.dump(data['listing']['data']['offers'], f, ensure_ascii=False)



