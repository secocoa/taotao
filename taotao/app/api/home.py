import random

from flask import request
from flask_restful import Resource, fields, marshal

# 首页
# 商品
from app.models import Goods, Strategy

# 商品
goods_value = {
    'id':fields.Integer(attribute='g_id'),
    'name':fields.String(attribute='g_name'),
    'price':fields.String(attribute='g_price'),
    'img':fields.String(attribute='g_img'),
    'collectnum':fields.String(attribute='g_collectnum'),
    'commentnum':fields.String(attribute='g_commentnum'),
}
# 轮播图
swiper_goods_c = {
    'id':fields.Integer(attribute='g_id'),
    'img':fields.String(attribute='g_img'),
}

class Home(Resource):
    def get(self):
        page = int(request.args.get('page') or 1)
        size = int(request.args.get('size')or 3)
        # 分页取商品
        goods = Goods.query.paginate(page,size,).items
        # 所有商品
        goodall = Goods.query.all()
        # 随机取商品四个
        swipergoods = random.sample(goodall,4)

        goods_c = {
            'status':fields.Integer,
            'goods':fields.List(fields.Nested(goods_value)),
            'swipergoods':fields.List(fields.Nested(swiper_goods_c)),
        }
        return marshal({'status':200,'goods':goods,'swipergoods':swipergoods},goods_c)

# 首页分类详情
class Category_good(Resource):
    def get(self):
        category_id = request.args.get('id')
        # 分类里面的商品
        goods = Goods.query.filter(Goods.category == category_id).all()
        # 轮播图
        swipergoods = random.sample(goods,4)
        # swipergoods = goods[0:4]

        return_c = {
            'status':fields.Integer,
            'goods':fields.List(fields.Nested(goods_value)),
            'swipergoods':fields.List(fields.Nested(swiper_goods_c)),
        }

        return marshal({'status':200,'goods':goods,'swipergoods':swipergoods},return_c)


# 攻略详情
strategy_content = {
    'name':fields.String(attribute='sname'),
    'content':fields.String(attribute='s_content'),
    'commentnum':fields.String(attribute='s_commentnum'),
    'collectnum':fields.String(attribute='s_collectnum'),
}
# 评论内容
comment_content = {
    'id':fields.String(attribute='commentid'),
    'content':fields.String(attribute='c_content'),
    'username':fields.String(attribute='co_user'),
}
# 精选好货
special_goods = {
    'id':fields.String(attribute='g_id'),
    'name':fields.String(attribute='g_name'),
    'content':fields.String(attribute='g_content'),
    'img':fields.String(attribute='g_img'),
}

# 攻略详情页面
class StrategyContent(Resource):
    def get(self):
        strategy_id = request.args.get('id')
        if strategy_id:
            strategy = Strategy.query.get(strategy_id)

            return_values = {
                'status':fields.Integer,
                'name':fields.String(attribute='s_name'),
                'content':fields.String(attribute='s_context'),
                'commentnum':fields.String(attribute='s_commentnum'),
                'collectnum':fields.String(attribute='s_collectnum'),
            }



            print(strategy_id)
            print(strategy)

            return {'status':0,}
        print(strategy_id)


        return {'status':1,'msg':'获取失败,没有传id'}
