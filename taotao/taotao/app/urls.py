from flask_restful import Api

from app.api.cartm import CartResource, Cartres
from app.api.userm import UserModel

api = Api()
def init_urls(app):
    api.init_app(app)

api.add_resource(UserModel,'/user/')
api.add_resource(CartResource,'/cart/')
api.add_resource(Cartres,'/wtfc/')
