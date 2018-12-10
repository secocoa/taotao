from flask_restful import Api

from app.api.addressm import AddressModel
from app.api.goodsm import GoodsModel
from app.api.userm import UserModel

api = Api()
def init_urls(app):
    api.init_app(app)

api.add_resource(UserModel,'/user/')
api.add_resource(AddressModel,'/address/')
api.add_resource(GoodsModel,'/good/')