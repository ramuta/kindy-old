import os
import heroku


def scale_worker(num):
    cloud = heroku.from_key(os.environ['HEROKU_API_KEY'])
    app = cloud.apps['kindy']
    app.processes['worker'].scale(num)