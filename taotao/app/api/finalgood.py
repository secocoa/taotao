import random

from flask import request, session
from flask_restful import Resource, fields, marshal
from sqlalchemy import and_

from app.models import Goods, Reevaluate, User, Evaluate, db, Collect

good_info = {
    'id':fields.Integer(attribute='g_id'),
    'gname':fields.String(attribute='g_name'),
    'ginformation':fields.String(attribute='g_information'),
    'gprice':fields.String(attribute='g_price'),
    'gimg':fields.String(attribute='g_img'),
    'gcollectnum':fields.Integer(attribute='g_collectnum'),
    'gcommentnum':fields.Integer(attribute='g_commentnum'),
}

specialgoods_info = {
    'saleprice':fields.String(attribute='g_saleprice'),
    'name':fields.String(attribute='g_name'),
    'price':fields.String(attribute='g_price'),
    'id':fields.Integer(attribute='g_id'),
    'img':fields.String(attribute='g_img')

}
#评论人
user_name = {
    'uid':fields.Integer(attribute='u_id'),
    'uname':fields.String(attribute='u_name'),
}
#父评论
comments_info = {
    'body':fields.String(attribute='e_content'),
    'id':fields.Integer(attribute='e_id'),
    'time':fields.String(attribute='e_time'),
}
#子评论
recom_info = {
    'rid':fields.Integer(attribute='te_id'),
    # 'uid':fields.Integer(attribute='te_parentid'),
    'time':fields.String(attribute='te_time'),
    'body':fields.String(attribute='te_content'),
    'rname':fields.String(attribute='te_bname')
}

class FinalGood(Resource):
    def get(self):
        id = request.args.get('id')
        uid = session.get('id')
        if not id:
            return {
                'stutas': 1,
                'msg':'未找到商品'
            }
        # 找到商品
        good = Goods.query.get(id)
        # 找到所有精选
        specialgoods = Goods.query.filter(Goods.is_chioce == 1).all()
        # 随机10个精选
        specialgoods = random.sample(specialgoods, 10)

        comments = Evaluate.query.filter(Evaluate.ev_goods==id).all()

        cuid = [comment.ev_user for comment in comments]

        user = []
        for i in cuid:
            user.append(User.query.get(i))

        print(uid)
        commetuser = User.query.filter(User.u_id.in_(cuid)).all()
        try:
            col = Collect.query.filter(and_(Collect.c_goods==id,Collect.c_user==uid)).first()
        except Exception:
            col = None
        print(col)
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
            recomments = Reevaluate.query.filter(Reevaluate.te_parentid == comment.e_id).all()
            # recommentid = comment.c_content + str(comment.com_id) #拼接内容和父评论id作为返回字内容表的键值
            recomments_dic[comment.e_id] = fields.List(fields.Nested(recom_info))
            return_recomments_dic[comment.e_id]  = recomments
            for recomment in recomments:
                reuser = User.query.filter(User.u_id == recomment.te_user).first()
                reuser_dic[recomment.te_id] = fields.Nested(user_name)  #

                return_reuser_dic[recomment.te_id] = reuser   #
        return_value = {
            'msg': fields.String,
            'status': fields.Integer,
            'good': fields.Nested(good_info),
             # 评论数据
            'arcomments':fields.List(fields.Nested(comments_info)),
            # 主评论人
            'user':fields.List(fields.Nested(user_name)),
            # 子评论
            'recomment':fields.Nested(recomments_dic),
            # 子评论人名字
            'recommentname':fields.Nested(reuser_dic),
            'specialgoods': fields.List(fields.Nested(specialgoods_info)),
            'collect':fields.Integer,
        }
        return marshal({'msg': 'OK',
                        'status': 1,
                        'good': good,
                        'specialgoods': specialgoods,
                        'arcomments':comments,
                        'user':user,
                        'recomment':return_recomments_dic,
                        'recommentname': return_reuser_dic,
                        'collect':1 if col else 0,
                        }, return_value)