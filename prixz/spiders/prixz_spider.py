import scrapy


class PrixzSpider(scrapy.Spider):
    name = 'prixz'
    allowed_domains = ['prixz.com']
    start_urls = ['https://prixz.com/']

    def parse(self, response):
        pass
