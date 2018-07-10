# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class SinaSportsSpider(scrapy.Spider):
    name = 'sina_sports'
    start_urls = ['http://sports.sina.com.cn/index1.shtml']

    def parse(self, response):
        urls =  response.css('h3 .ty-card-link-em ::attr(href)').extract()
        for url in urls:
            yield scrapy.Request('http:' + url, callback = self.parse_article)

    def parse_article(self, response):
        article = '<br/>'.join(response.css('.article p ::text').extract()).strip()
        
        time = response.css('.date ::text').extract_first()
        time = " ".join(time.split())
        time = time + ':00'
        time = datetime.strptime(time, '%Y年%m月%d日 %H:%M:%S')
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        media = response.css('.source ::text').extract_first()
        img = None
        if response.css('.article img::attr(src)').extract_first():
            img = response.css('.article img::attr(src)').extract_first()
        if article and time and media:
            yield{
                    'title': ''.join(response.css('h1::text').extract()),
                    'article': article,
                    'time':  time,
                    'type': '体育',
                    'source': media,
                    'author': media,
                    'url': response.url,
                    'img': img,
                    }
        else:
            return None
