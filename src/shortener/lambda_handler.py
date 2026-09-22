from mangum import Mangum

from shortener.main import app

handler = Mangum(app, lifespan="on")
