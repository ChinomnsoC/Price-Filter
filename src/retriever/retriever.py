import scrapy

class PriceSpider(scrapy.Spider):
    name = 'TvPrices'
    start_urls = [
        'https://www.currys.co.uk/products/lg-oled55cs6la-55-smart-4k-ultra-hd-hdr-oled-tv-with-google-assistant-and-amazon-alexa-10242981',
    ]
    def parse(self, response):
        for prices in response.css('div.price'):
            yield {
                'price-information': price.xpath('span/span'),
                'infos': price.css('span.value::content').get(),
            }
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
