from flask import Flask

from app import settings
from app.ext import init_ext
from app.urls import init_urls




def create_app(envir):
    app = Flask(__name__)

    app.config.from_object(settings.config.get(envir))
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))


    init_ext(app)
    init_urls(app)

    return app