#encodig: utf-8

from flask import Flask

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
	return u'这是首页'

if __name__ == '__main__':
	app.run()