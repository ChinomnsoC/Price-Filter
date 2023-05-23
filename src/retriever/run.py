from scrapy.crawler import CrawlerProcess
from retriever.spiders.retriever_spider  import  RetrieverSpider # this is our friend in subfolder **spiders**
from scrapy.utils.project import get_project_settings

# Run that thing!

process = CrawlerProcess(get_project_settings())
process.crawl(RetrieverSpider)
process.start()