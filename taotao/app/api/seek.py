from flask import request
from flask_restful import Resource, fields, marshal

from app.models import Goods


# 商品
goods_value = {
    'id':fields.Integer(attribute='g_id'),
    'name':fields.String(attribute='g_name'),
    'price':fields.String(attribute='g_price'),
    'img':fields.String(attribute='g_img'),
    'collectnum':fields.String(attribute='g_collectnum'),
    'commentnum':fields.String(attribute='g_commentnum'),
}
class Seek(Resource):
    def get(self):
        content = request.args.get('content')

        if not content:
            return {
                'sratus':1,
                'msg':'没有要搜索的内容'
            }
        con = '%' + str(content) + '%'

        goods = Goods.query.filter(Goods.g_name.ilike(con)).all()
        print(goods)
        if not goods:
            return {
                'status':1,
                'msg':'亲,请换个姿势搜索哦~'
            }
        goods_seek = {
            'status':fields.Integer,
            'goods':fields.List(fields.Nested(goods_value))
        }
        return marshal({'status':0,'goods':goods},goods_seek)