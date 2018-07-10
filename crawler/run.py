from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import sqlite3

url = 'crawler/toutiao.sqlite'

def run_crawl():
    process = CrawlerProcess(get_project_settings())
    process.crawl('sina_hb')
    # process.crawl('sina_mil')
    process.start()

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