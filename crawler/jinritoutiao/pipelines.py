# -*- coding: utf-8 -*-

import sqlite3

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JinritoutiaoPipeline(object):
    def open_spider(self, spider):
        self.conn = sqlite3.connect('toutiao.sqlite')
        self.c = self.conn.cursor()
        self.c.execute(r'create table if not exists toutiao(title text unique, article text, time text, type text, source text,author text, img text, likes integer default 0, url text, waitforcheck integer default 1, value integer default 0)')

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        if item != None:
            titles = self.c.execute(r'select title from toutiao').fetchall()
            if tuple(item['title'],) not in titles:
                self.c.execute(r'insert into toutiao (title, article, time, type, source, author, url, img) values(?, ?, ?, ?, ?, ?, ?, ?)', (item['title'],item['article'], item['time'], item['type'], item['source'], item['author'], item['url'], item['img']))
        return item
