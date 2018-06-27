# -*- coding: UTF-8 -*- 

from flask import Flask
import config as config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
	return u'哈哈哈'

if __name__ == '__main__':
	app.run()