from pathlib import Path

import scrapy


class RetrieverSpider(scrapy.Spider):
    name = "TvPrices"

    def start_requests(self):
        allowed_domains = ['currys.co.uk']  
        urls = [
            'https://www.currys.co.uk/products/lg-oled55cs6la-55-smart-4k-ultra-hd-hdr-oled-tv-with-google-assistant-and-amazon-alexa-10242981',
        ]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'TvPrices-{page}.html'
        Path(filename).write_bytes(response.body)
        self.log(f'Saved file {filename}')
