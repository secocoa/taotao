from flask_restful import Api

from app.api.addressm import AddressModel
from app.api.goodsm import GoodsModel

from app.api.stategy import CategoryModel

from app.api.home import Home, Category_good, StrategyContent

from app.api.userm import UserModel

api = Api()
def init_urls(app):
    api.init_app(app)
# 登录注册
api.add_resource(UserModel,'/user/')

# 地址
api.add_resource(AddressModel,'/address/')
# 商品详情
api.add_resource(GoodsModel,'/good/')



# 攻略
api.add_resource(CategoryModel,'/category/')

# 首页
api.add_resource(Home,'/')
# 首页分类详情
api.add_resource(Category_good,'/category/')
# 攻略详情页面
api.add_resource(StrategyContent,'/article/')

