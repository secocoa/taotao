import random

from flask import request
from flask_restful import Resource, fields, marshal

# 首页
# 商品
from app.models import Goods, Strategy, Comment, User

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
        if category_id:
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
        return {'status':1,'msg':'获取失败,没有分类id'}

# 攻略详情
strategy_content = {
    'name':fields.String(attribute='s_name'),
    'content':fields.String(attribute='s_context'),
    'commentnum':fields.String(attribute='s_commentnum'),
    'collectnum':fields.String(attribute='s_collectnum'),
    'readnum':fields.String(attribute='s_readnum'),
}
# 精选好货
special_goods = {
    'id':fields.String(attribute='g_id'),
    'name':fields.String(attribute='g_name'),
    'price':fields.String(attribute='g_price'),
    'img':fields.String(attribute='g_img'),
}
# 主评论内容
comment_content = {
    # 主评论id
    'id':fields.String(attribute='commentid'),
    'content':fields.String(attribute='c_content'),
    'time':fields.String(attribute='c_time'),
}
# 主评论人
user_name = {
    'uid':fields.Integer(),
    'uname':fields.String(attribute='u_name'),
}
# 子评论
recomment_content = {
    'rid':fields.Integer(attribute='nt_id'),
    'body':fields.String(attribute='nt_content'),
    'uid':fields.String(attribute='u_id'),
    'time':fields.String(attribute='nt_time'),
    'bname':fields.String(attribute='nt_bname'),
    'name':fields.String(attribute=''),
}
# 攻略详情页面
class StrategyContent(Resource):
    def get(self):
        # 文章id
        strategy_id = request.args.get('id')
        if strategy_id:

            strategy = Strategy.query.get(strategy_id)
            print(strategy)
            # 所有商品
            goodall = Goods.query.all()
            # 随机取商品2个
            swipergoods = random.sample(goodall, 2)

            # 评论数据 根据文章id
            comments = Comment.query.filter(Comment.strategy == strategy_id).all()
            # print(comments)
            # 根据文章id,获取用户
            for comment in comments:


                id = comment.co_user
                user = User.query.get(id).u_name
                print(user)

            return_values = {
                'status':fields.Integer,
                # 文章数据
                'strategy':fields.List(fields.Nested(strategy_content)),
                # 评论数据
                'arcomments':fields.List(fields.Nested(comment_content)),
                # 主评论人
                'user':fields.List(fields.Nested(user_name)),
                # 子评论
                'recomment':fields.List(fields.Nested(recomment_content)),
                # 精选好货数据
                'specialgoods':fields.List(fields.Nested(special_goods)),
            }

            # print(strategy_id)
            # print(strategy)
            return marshal({
                'status':0,
                'strategy':strategy,
                'specialgoods':swipergoods,
                'arcomments':comments,
                'user':user,


            },return_values)
        # print(strategy_id)
        return {'status':1,'msg':'获取失败,没有传文章id'}
