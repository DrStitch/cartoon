# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.spiders import Spider
from cartoon.items import CartoonItem

class CartSpider(Spider):
    name = "cart"
    allowed_domains = [""]
    cookies = {'xres': '3'}
    def __init__(self, url='', *args, **kwargs):
        super(HentaiSpider, self).__init__(*args, **kwargs)
        self.start_urls = (
            url,
        )

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=self.cookies)

    def parse(self, response):
        item = CartoonItem()
        div = response.xpath('//div[@id="sd"]')
        item['image_urls'] = div.xpath('//img/@src').extract()
        item['name'] = ['%03d' % (response.request.meta['depth'] + 1)]
        yield item

        next_url = div.xpath('./a/@href').extract()[0]
        if next_url != response.url:
            yield Request(next_url, cookies=self.cookies)
