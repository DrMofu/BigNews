from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
import sqlite3
from jinritoutiao import spiders


@defer.inlineCallbacks
def crawl():
    runner = CrawlerRunner(get_project_settings())
    yield runner.crawl(spiders.sina_hb.SinaHBSpider)
    yield runner.crawl(spiders.sina_mil.SinaMILSpider)
    yield runner.crawl(spiders.sina_travel.SinaTravelSpider)
    yield runner.crawl(spiders.sina_sports.SinaSportsSpider)
    yield runner.crawl(spiders.sina_finance.SinaFinanceSpider)

    reactor.stop()
    
def run_crawl():
    crawl()
    reactor.run()

url = 'toutiao.sqlite'

def get_toutiao():
    # conn = sqlite3.connect('crawler/toutiao.sqlite')
    conn = sqlite3.connect(url)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    returnlist = c.execute('select * from toutiao').fetchall()
    conn.close()
    return returnlist

def delete_database():
    conn = sqlite3.connect(url)
    c = conn.cursor()
    c.execute('drop table toutiao')
    conn.close()
    print('finished!')

def test():
	return_list = get_toutiao()
	for item in return_list:
		print(item['article'])
	return 'finished!'