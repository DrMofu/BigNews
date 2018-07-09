# -*- coding: utf-8 -*-
import scrapy


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    URL = 'http://localhost:8050/render.html?url=https://toutiao.com'
    start_urls = ['http://localhost:8050/render.html?url=https://toutiao.com/&wait=0.5&images=0&viewport=3840x2160']

    def parse(self, response):
        urls = response.css('div [ga_event="article_title_click"] [target="_blank"] ::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(self.URL + url + '&wait=0.5&images=0',
                                 callback = self.parse_article)

    def parse_article(self, response):
        span = response.css('.article-sub span::text').extract();
        time = None
        media = None
        if len(span) >= 2:
            if span[0] == '原创':
                time = span[2]
                media = span[1]
            else:
                time = span[1]
                media = span[0]
        else:
            return None
        yield{
                'title': ''.join(response.css('h1::text').extract()),
                'article': '\n'.join(response.css('.article-content ::text').extract()),
                'time': time,
                'type': ''.join(response.css('.bui-left [ga_event*="click_channel"] ::text').extract()),
                'source': media,
                'author': media,
                'url': response.url.split('url=')[1].split('&wait')[0],
                }
