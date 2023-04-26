import scrapy
from scrapy.crawler import CrawlerProcess


class RetrieverSpider(scrapy.Spider):
    name = "TvPrice"

    def start_requests(self):
        urls = [
            'https://www.johnlewis.com/lg-oled55cs6la-2022-oled-hdr-4k-ultra-hd-smart-tv-55-inch-with-freeview-hd-freesat-hd-dolby-atmos-black/p109457439?s_ppc=1dx43700074457397082_brand_technology_BAU&tmad=c&tmcampid=2&gclid=Cj0KCQjwn9CgBhDjARIsAD15h0DRAbPPScq8_oelL148dXwzp3FJ2lT1egAwsI5cCZSKJCuOJPXA0q0aAg55EALw_wcB&gclsrc=aw.ds',
        ]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)
            
            
    def parse(self, response):
        for price in response.css("div.Price_base__1OoOa"):
            print('Scrapy begins crawling')
            yield{
                'prod_price': price.css("span::text").get(),
            }
    
process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})
process.crawl(RetrieverSpider)
process.start()
    # def parse(self, response):
    #     filename = f'ProductPage.html'
    #     Path(filename).write_bytes(response.body)
    #     self.log(f'Saved file {filename}')
    #     print(response.body, "Responding...")
