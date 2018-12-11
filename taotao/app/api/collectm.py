from flask import session
from flask_restful import Resource, marshal, fields

from app.models import User, Goods, Strategy

# goods_info = {
#     'gid':fields.Integer(attribute=''),
#     'gname':fields.String,
#
# }
class CollectModel(Resource):
    def get(self):
        id = session.get('id')
        # 获取用户
        user = User.query.get(id)
        # 获取收藏
        collects = user.collect
        # 商品 攻略表
        is_good = []
        is_strategy = []
        goods_id = []
        strategy_id = []
        # 将收藏表中攻略和商品分类
        for collect in collects:
            if collect.is_good == 1:
                is_good.append(collect)
            else:
                is_strategy.append(collect)
        # 获取商品ID
        for good in is_good:
            goods_id.append(good.c_goods)
        # 获取攻略ID
        for i in is_strategy:
            strategy_id.append(i.c_strategy)
        # 获取商品对象集
        print(goods_id,strategy_id)
        goods = Goods.query.filter(Goods.g_id.in_(goods_id)).all()
        print(goods)
        # 获取攻略对象集
        strategy = Strategy.query.filter(Strategy.s_id.in_(strategy_id)).all()
        print(strategy)
        # return marshal({'msg':1,
        #                 'status':1,
        #                 'goods':goods,
        #                 'stategy':strategy},)
        return {'msg':'ok'}
