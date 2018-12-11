from flask import session
from flask_restful import Resource, marshal, fields

from app.models import User

goods_info = {
    'gid':fields.Integer(attribute=''),
    'gname':fields.String,

}
class CollectModel(Resource):
    def get(self):
        id = session.get('id')
        # 获取用户
        user = User.query.get(id)
        # 获取收藏
        collects = user.collect
        # 商品 攻略表
        is_good = []
        is_stategy = []
        goods_id = []
        stategy_id = []
        goods = []
        stategy = []
        # 将收藏表中攻略和商品分类
        for collect in collects:
            if collect.is_good == 1:
                is_good.append(collect)
            else:
                is_stategy.append(collect)
        # 获取商品ID
        for good in is_good:
            goods_id.append(good.c_goods)
        # 获取商品对象
        return marshal({'msg':1,
                        'status':1,
                        'goods':goods,
                        'stategy':stategy},)
