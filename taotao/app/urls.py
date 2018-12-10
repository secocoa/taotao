from flask_restful import Api

from app.api.stategy import CategoryModel
from app.api.userm import UserModel

api = Api()
def init_urls(app):
    api.init_app(app)

api.add_resource(UserModel,'/user/')

# 攻略
api.add_resource(CategoryModel,'/category/')
