from flask import session, request
from flask_restful import Resource






from app.models import Evaluate, Reevaluate, User, db, Goods


# 商品发表评论
class GoodsReviews(Resource):
    def post(self):
        username = session.get('username')
        id = session.get('id')
        if not username:
            return {
                'status':1,
                'msg':'用户未登录'
            }
        goodid = request.form.get('goodid')
        comment = request.form.get('comment')
        user_id = request.form.get('mainid') or 0
        r_id = request.form.get('rid') or 0

        if not goodid:
            return {
                'status':1,
                'msg':'没有商品id'
            }
        if not comment:
            return {
                'status':1,
                'msg':'没有评论内容'
            }
        # zi评论
        if user_id:
            if r_id:
                reevaluate = Reevaluate()
                reevaluate.te_content = comment
                reevaluate.te_parentid = user_id
                reevaluate.te_user = id
                # 根据子评论id获取用户
                user = Reevaluate.query.filter(Reevaluate.te_id == r_id).all()
                name_id = user[0].te_user
                name = User.query.get(name_id).u_name
                reevaluate.te_bname = name
                db.session.add(reevaluate)
                db.session.commit()
                # 增加评论数
                pinglun = Goods.query.get(goodid)
                pinglun.g_commentnum = int(pinglun.g_commentnum) + 1
                db.session.commit()
                return {
                    'starus':0,
                    'msg':'子评论回复成功'
                }
            # 回复朱评论
            reeva = Reevaluate()
            reeva.te_content = comment
            reeva.te_parentid = user_id
            reeva.te_user = id
            # 朱评论id获取用户
            user = Evaluate.query.filter(Evaluate.e_id == user_id).all()
            name_id = user[0].ev_user
            name = User.query.get(name_id).u_name
            reeva.te_bname = name
            db.session.add(reeva)
            db.session.commit()
            # 增加评论数
            pinglun = Goods.query.get(goodid)
            pinglun.g_commentnum = int(pinglun.g_commentnum) + 1
            db.session.commit()

            return {
                'status':1,
                'msg':'回复主评论成功'
            }
        # 父评论
        eva = Evaluate()
        eva.e_content = comment
        eva.ev_goods = goodid
        eva.ev_user = id
        db.session.add(eva)
        db.session.commit()
        # 增加评论数
        pinglun = Goods.query.get(goodid)
        pinglun.g_commentnum = int(pinglun.g_commentnum) + 1
        db.session.commit()
        return {
            'status':0,
            'msg':'主评论发表成功'
        }





