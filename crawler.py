import requests
import json
import re
from models import News

def crawler_36kr():
	return_list = []
	PER_PAGE = 20
	newsurl = 'https://36kr.com/api/newsflash?per_page=%s' % PER_PAGE
	res = requests.get(newsurl) # 获取html文件信息
	res.encoding = 'utf-8'  # 很重要！
	ans = json.loads(res.text)

	result = []

	for item in ans['data']['items']:
		title= item['title']
		# 检查新闻是否已经存在
		news = News.query.filter(News.title == title).first()
		if news:
			print('数据已经存在 %s' % title)
			continue
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
				news = News(title=title,article=desc,date=time,\
				type='科技',source='36Kr',author='36Kr',likes=0,\
				url=url,waitforcheck=1,value=0)	
				return_list.append(news)
	return return_list