# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class SinaTravelSpider(scrapy.Spider):
    name = 'sina_travel'
    start_urls = ['http://travel.sina.com.cn/']

    def parse(self, response):
        urls = response.css('.travel-new a ::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url, callback = self.parse_article)

    def parse_article(self, response):
        article = '<br/>'.join(response.css('.article>p ::text').extract())
        
        time = response.css('.time-source ::text').extract_first().strip()
        time = " ".join(time.split())
        time = time + ':00'
        time = datetime.strptime(time, '%Y年%m月%d日%H:%M:%S')
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        media = response.css('.time-source span ::text').extract_first()
        img = None
        if response.css('.article img::attr(src)').extract_first():
            img = response.css('.article img::attr(src)').extract_first()
        if article and time and media:
            yield{
                    'title': ''.join(response.css('h1 ::text').extract()),
                    'article': article,
                    'time':  time,
                    'type': '旅游',
                    'source': media,
                    'author': media,
                    'url': response.url,
                    'img': img,
                    }
        else:
            return None
