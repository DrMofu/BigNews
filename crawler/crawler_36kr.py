import requests
import json
import re
import sqlite3

PER_PAGE =20
newsurl = 'https://36kr.com/api/newsflash?per_page=%s' % PER_PAGE
res = requests.get(newsurl) # 获取html文件信息
res.encoding = 'utf-8'  # 很重要！
ans = json.loads(res.text)

conn = sqlite3.connect('../bignews.db')
c = conn.cursor()

for item in ans['data']['items']:    
    title= item['title']
    # 检查新闻是否已经存在
    cursor = c.execute("SELECT Title from News WHERE Title = '{}'".format(title))
    row = cursor.fetchall()
    if row:
        print('数据已经存在 %s' % title)
    else:
        time = item['created_at']
        desc = item['description']
        url = item['news_url']
        if re.search('）$',desc):
            source = desc.split('（')[-1][:-1]
            desc = desc.rstrip('（'+source+'）')
        else:
            source = '36氪'    
            desc = item['description']
        c.execute("INSERT INTO News (Title, Article, Date, Type, Source, Author, Likes, URL, WaitForCheck, Value)\
             VALUES ('{}','{}','{}','科技','{}','{}',0,'{}',1,0)".format(title,desc,time,source,source,url))
conn.commit()    
conn.close()