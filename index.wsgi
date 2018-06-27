import sae

from index import app

application = sae.create_wsgi_app(app)