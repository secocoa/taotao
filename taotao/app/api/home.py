import random

from flask import request, session
from flask_restful import Resource, fields, marshal

# 首页
# 商品
from app.models import Goods, Strategy, Comment, User, Recomment, db

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
comment_info = {
    # 主评论id
    'id':fields.String(attribute='com_id'),
    'content':fields.String(attribute='c_content'),
    'time':fields.String(attribute='c_time'),
}
# 主评论人
user_name = {
    'uid':fields.Integer(attribute='u_id'),
    'uname':fields.String(attribute='u_name'),
}
# 子评论
recomment_info = {
    'rid':fields.Integer(attribute='nt_id'),
    'body':fields.String(attribute='nt_content'),
    # 'uid':fields.String(attribute='nt_user'),
    'time':fields.String(attribute='nt_time'),
    'bname':fields.String(attribute='nt_bname'),
}
# 子评论人 名字
user_info = {
    'name':fields.String(attribute='u_name'),
}

# 攻略详情页面
class StrategyContent(Resource):
    def get(self):
         # 文章id
        strategy_id = request.args.get('id')
        if not strategy_id:
            return {
                'status' :1 ,
                'msg': '未获取文章'
            }
        strategy = Strategy.query.get(strategy_id)
        # print(strategy)
        # 所有商品
        goodall = Goods.query.all()
        # print(goodall)
        # 随机取商品2个
        swipergoods = random.sample(goodall, 4)


        comments = Comment.query.filter(Comment.c_strategy==strategy_id).all()

        cuid = [comment.co_user for comment in comments]
        print(cuid)
        user = []
        for i in cuid:
            user.append(User.query.get(i))

        commetuser = User.query.filter(User.u_id.in_(cuid)).all()


        #自评论表
        return_recomments_dic = {

        }
        recomments_dic = {

        }
        #自评论表外键uerid
        return_reuser_dic = {

        }

        reuser_dic = {

        }
        list1  = []
        for comment in comments:
            recomments = Recomment.query.filter(Recomment.nt_parentid == comment.com_id).all()
            # recommentid = comment.c_content + str(comment.com_id) #拼接内容和父评论id作为返回字内容表的键值
            recomments_dic[comment.com_id] = fields.List(fields.Nested(recomment_info))
            return_recomments_dic[comment.com_id]  = recomments
            for recomment in recomments:
                reuser = User.query.filter(User.u_id == recomment.nt_user).first()


                reuser_dic[recomment.nt_id] = fields.Nested(user_info)  #

                return_reuser_dic[recomment.nt_id] = reuser   #




        return_values = {
            'status':fields.Integer,
            # 文章数据
            'strategy':fields.List(fields.Nested(strategy_content)),
            # 评论数据
            'arcomments':fields.List(fields.Nested(comment_info)),
            # 主评论人
            'user':fields.List(fields.Nested(user_name)),
            # 子评论
            'recomment':fields.Nested(recomments_dic),
            # 子评论人名字
            'recommentname':fields.Nested(reuser_dic),
            # 精选好货数据
            'specialgoods':fields.List(fields.Nested(special_goods)),
        }

        return marshal({
            'status':0,
            'strategy':strategy,
            'specialgoods':swipergoods,
            'arcomments':comments,
            'user':user,
            'recomment':return_recomments_dic,
            'recommentname': return_reuser_dic,
        },return_values)


