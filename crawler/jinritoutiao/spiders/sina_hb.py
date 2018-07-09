# -*- coding: utf-8 -*-
import scrapy


class SinaHBSpider(scrapy.Spider):
    name = 'sina_hb'
    start_urls = ['http://hb.sina.com.cn/']

    def parse(self, response):
        urls =  response.css('h2 [target="_blank"] ::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url, callback = self.parse_article)

    def parse_article(self, response):
        article = '\n'.join(response.css('.article-body p::text').extract())
        time = response.css('.source-time ::text').extract_first()
        media = response.css('.source-time #art_source::text').extract_first()
        img = None
        if response.css('.img_wrapper img::attr(src)').extract_first():
            img = response.css('.img_wrapper img::attr(src)').extract_first()
        if article and time and media:
            yield{
                    'title': ''.join(response.css('h1::text').extract()),
                    'article': article,
                    'time':  time,
                    'type': '大湖北',
                    'source': media,
                    'author': media,
                    'url': response.url,
                    'img': img,
                    }
        else:
            return None
