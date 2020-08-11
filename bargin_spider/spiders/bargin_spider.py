# -*- coding: utf-8 -*-
import scrapy


class bargin_spider(scrapy.Spider):
    name = "bargin_spider"
    start_urls = [
        # 'http://quotes.toscrape.com/',
        'https://www.ozbargain.com.au/'
    ]

    def parse(self, response):
        for quote in response.css("h2.title"):
            yield {
                'text': quote.css('h2::attr(data-title)').extract_first(),
                'link': quote.css('a::attr(href)').extract_first()
                # 'author': quote.css("small.author::text").extract_first(),
                # 'tags': quote.css("div.tags > a.tag::text").extract()
            }

        page_num = response.css("a.pager-next::attr(title)").extract_first()
        if '5' in page_num:
            return

        next_page_url = response.css("a.pager-next::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

