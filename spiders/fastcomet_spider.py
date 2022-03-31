from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

"""
Scrapy spider for fastcomet.com to get all urls from the site and return the url
"""

class FastcometSpider(CrawlSpider):
    name = 'fastcomet'
    allowed_domains = ['fastcomet.com']
    start_urls = ['https://fastcomet.com/']

    rules = (
        Rule(LinkExtractor(allow=('fastcomet')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'url': response.url,
        }
