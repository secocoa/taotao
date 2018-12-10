from flask import session, request
from flask_restful import Resource

from app.models import Goods


class GoodsModel(Resource):
    def get(self):
        id = request.args.get('id')
        good = Goods.query.get(id)
