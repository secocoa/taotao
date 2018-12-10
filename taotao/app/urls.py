from flask_restful import Api

<<<<<<< HEAD
from app.api.addressm import AddressModel
from app.api.goodsm import GoodsModel
=======
<<<<<<< HEAD
from app.api.stategy import CategoryModel
=======
from app.api.home import Home, Category_good, StrategyContent
>>>>>>> e5c997b902188af164153e0162122f668517199f
>>>>>>> d965a9adfbbf91acf0c45123ce92be905bbcbfe4
from app.api.userm import UserModel

api = Api()
def init_urls(app):
    api.init_app(app)

api.add_resource(UserModel,'/user/')
<<<<<<< HEAD
api.add_resource(AddressModel,'/address/')
api.add_resource(GoodsModel,'/good/')
=======

<<<<<<< HEAD
# 攻略
api.add_resource(CategoryModel,'/category/')
=======
# 首页
api.add_resource(Home,'/')
# 首页分类详情
api.add_resource(Category_good,'/category/')
# 攻略详情页面
api.add_resource(StrategyContent,'/article/')
>>>>>>> e5c997b902188af164153e0162122f668517199f
>>>>>>> d965a9adfbbf91acf0c45123ce92be905bbcbfe4
