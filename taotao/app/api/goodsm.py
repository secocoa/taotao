import random

from flask import session, request
from flask_restful import Resource, marshal, fields

from app.models import Goods

good_info = {
    'gname':fields.String(attribute='g_name'),
    'ginformation':fields.String(attribute='g_information'),
    'gprice':fields.String(attribute='g_price'),
    'gimg':fields.String(attribute='g_img'),
    'gcollectnum':fields.Integer(attribute='g_collectnum'),
    'gcommentnum':fields.Integer(attribute='g_commentnum'),
}
comments_info = {
    'body':fields.String(attribute='e_content'),
    'id':fields.Integer(attribute='e_id'),
    'usename':fields.String(attribute='ev_user'),
    'time':fields.String(attribute='time')
}
specialgoods_info = {
    'saleprice':fields.String(attribute='g_saleprice'),
    'name':fields.String(attribute='g_name'),
    'price':fields.String(attribute='g_price'),
    'id':fields.Integer(attribute='g_id'),
    'img':fields.String(attribute='g_img')

}
class GoodsModel(Resource):
    def get(self):
        id = request.args.get('id')
        if id:
            # 找到商品
            good = Goods.query.get(id)
            # 找到评论
            comments = good.g_evaluate.all()
            #找到用户
            # 找到所有精选
            specialgoods = Goods.query.filter(Goods.is_chioce==1).all()
            # 随机10个精选
            specialgoods = random.sample(specialgoods,10)
            all_info = {
                'msg':fields.String,
                'status':fields.Integer,
                'good':fields.Nested(good_info),
                'comments':fields.List(fields.Nested(comments_info)),
                'specialgoods':fields.List(fields.Nested(specialgoods_info))
            }
            return marshal({'msg':'OK',
                            'status':1,
                            'good':good,
                            'comments':comments,
                            'specialgoods':specialgoods},all_info)
        else:
            return {'msg':'没有获取ID','status':0}
