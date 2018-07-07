# -*- coding: utf-8 -*-
import scrapy


class SinaMILSpider(scrapy.Spider):
    name = 'sina_mil'
    start_urls = ['https://mil.news.sina.com.cn/']

    def parse(self, response):
        urls =  response.css('.mess_link_one [target="_blank"] ::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url, callback = self.parse_article)

    def parse_article(self, response):
        article = '\n'.join(response.css('.article p ::text').extract())
        time = response.css('.date ::text').extract_first()
        time = " ".join(time.split())
        time = time + ':00'
        media = response.css('.source ::text').extract_first()
        img = None
        if response.css('.article img::attr(src)').extract_first():
            img = response.css('.article img::attr(src)').extract_first()
        if article and time and media:
            yield{
                    'title': ''.join(response.css('h1::text').extract()),
                    'article': article,
                    'time':  time,
                    'type': '军事',
                    'source': media,
                    'author': media,
                    'url': response.url,
                    'img': img,
                    }
        else:
            return None
