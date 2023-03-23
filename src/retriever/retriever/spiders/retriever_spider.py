from pathlib import Path
import sys, os
sys.path.append(os.path.abspath(os.path.join('../../../../', 'scrape_output')))

import scrapy


class RetrieverSpider(scrapy.Spider):
    name = "TvPrice"

    def start_requests(self):
        urls = [
            'https://www.johnlewis.com/lg-oled55cs6la-2022-oled-hdr-4k-ultra-hd-smart-tv-55-inch-with-freeview-hd-freesat-hd-dolby-atmos-black/p109457439?s_ppc=1dx43700074457397082_brand_technology_BAU&tmad=c&tmcampid=2&gclid=Cj0KCQjwn9CgBhDjARIsAD15h0DRAbPPScq8_oelL148dXwzp3FJ2lT1egAwsI5cCZSKJCuOJPXA0q0aAg55EALw_wcB&gclsrc=aw.ds',
        ]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)
            
    
    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tag::text').getall(),
    #         }

    def parse(self, response):
        # page = response.url.split("/")[-2]
        filename = f'ProductPage.html'
        Path(filename).write_bytes(response.body)
        self.log(f'Saved file {filename}')
        print(response.body, "Responding...")
