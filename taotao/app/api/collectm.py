from flask import session
from flask_restful import Resource, marshal, fields

from app.models import User, Goods, Strategy

goods_info = {
    'gid':fields.Integer(attribute='g_id'),
    'gname':fields.String(attribute='g_name'),
    'gcollectnum':fields.String(attribute='g_collectnum'),
    'gcommentnum':fields.String(attribute='g_commentnum'),
    'gimg':fields.String(attribute='g_img'),
    'gprice':fields.String(attribute='g_price')
}
strategy_info = {
    'sid':fields.Integer(attribute='s_id'),
    'sname':fields.String(attribute='s_name'),
    'scommentnum':fields.String(attribute='s_commentnum'),
    'scollectnum':fields.String(attribute='s_collectnum'),
    'simg':fields.String(attribute='s_image'),
}
class CollectModel(Resource):
    def get(self):
        id = session.get('id')
        if id:
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
            goods = Goods.query.filter(Goods.g_id.in_(goods_id)).all()
            # 获取攻略对象集
            strategy = Strategy.query.filter(Strategy.s_id.in_(strategy_id)).all()
            collect_info = {
                'msg': fields.String,
                'status':fields.Integer,
                'goods':fields.List(fields.Nested(goods_info)),
                'strategy':fields.List(fields.Nested(strategy_info))
            }
            return marshal({'msg':'返回成功',
                            'status':1,
                            'goods':goods,
                            'strategy':strategy},collect_info)
        else:
            return {'msg':'请先登录','status':0}

