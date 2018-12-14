import random

from flask import session, request
from flask_restful import Resource, marshal, fields

from app.models import Goods, User, Reevaluate

good_info = {
    'id':fields.Integer(attribute='g_id'),
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
    'time':fields.String(attribute='e_time'),
}
specialgoods_info = {
    'saleprice':fields.String(attribute='g_saleprice'),
    'name':fields.String(attribute='g_name'),
    'price':fields.String(attribute='g_price'),
    'id':fields.Integer(attribute='g_id'),
    'img':fields.String(attribute='g_img')

}
user_info = {
    'uid':fields.Integer(attribute='u_id'),
    'uname':fields.String(attribute='u_name'),
}
recom_info = {
    'rid':fields.Integer(attribute='te_id'),
    'uid':fields.Integer(attribute='te_parentid'),
    'time':fields.String(attribute='te_time'),
    'body':fields.String(attribute='te_content'),
    'rname':fields.String(attribute='te_bname')
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
            u_id = []
            r_id = []
            recom = []
            for comment in comments:
                u_id.append(comment.ev_user)
                r_id.append(comment.e_id)
            for i in r_id:
                recomments = Reevaluate.query.filter(Reevaluate.te_parentid == i).all()
                recom.append(recomments)
            user = User.query.filter(User.u_id.in_(u_id)).all()
            # 找到所有精选
            specialgoods = Goods.query.filter(Goods.is_chioce==1).all()
            # 随机10个精选
            specialgoods = random.sample(specialgoods,10)
            # 获取子评论
            all_info = {
                'msg':fields.String,
                'status':fields.Integer,
                'good':fields.Nested(good_info),
                'comments':fields.List(fields.Nested(comments_info)),
                'user':fields.List(fields.Nested(user_info)),
                'recom': fields.List(fields.List(fields.Nested(recom_info))),
                'specialgoods':fields.List(fields.Nested(specialgoods_info))
            }
            return marshal({'msg':'OK',
                            'status':1,
                            'good':good,
                            'comments':comments,

                            'user':user,
                            'recom':recom,
                            'specialgoods':specialgoods},all_info)

        else:
            return {'msg':'没有获取ID','status':0}
