from flask_restful import Api

from app.api.home import Home, Category_good, StrategyContent
from app.api.userm import UserModel

api = Api()
def init_urls(app):
    api.init_app(app)

api.add_resource(UserModel,'/user/')

# 首页
api.add_resource(Home,'/')
# 首页分类详情
api.add_resource(Category_good,'/category/')
# 攻略详情页面
api.add_resource(StrategyContent,'/article/')
