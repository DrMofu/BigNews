# from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerProcess
import sqlite3

def run_crawl():
    process = CrawlerProcess(get_project_settings())
    process.crawl('sina_hb')
    process.start()

def get_toutiao():
    conn = sqlite3.connect('toutiao.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    returnlist = c.execute('select * from toutiao').fetchall()
    conn.close()
    return returnlist
