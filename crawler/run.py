from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import sqlite3
from .jinritoutiao.spiders import sina_hb, sina_mil, sina_travel, sina_sports, sina_finance


@defer.inlineCallbacks
def crawl():
    runner = CrawlerRunner({
        'ITEM_PIPELINES': {'crawler.jinritoutiao.pipelines.JinritoutiaoPipeline': 300}
    })
    yield runner.crawl(sina_hb.SinaHBSpider)
    yield runner.crawl(sina_mil.SinaMILSpider)
    yield runner.crawl(sina_travel.SinaTravelSpider)
    yield runner.crawl(sina_sports.SinaSportsSpider)
    yield runner.crawl(sina_finance.SinaFinanceSpider)

    reactor.stop()
    
def run_crawl():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    crawl()
    reactor.run()

url = 'crawler/toutiao.sqlite'

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