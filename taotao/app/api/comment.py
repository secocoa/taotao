from flask import session, request
from flask_restful import Resource
from app.models import Recomment, User, db, Comment, Strategy


# 攻略发表评论

class CommentStrategy(Resource):
    def post(self):
        # 用户登录
        username = session.get('username')
        id = session.get('id')
        if not username:
            return {
                'status': 1,
                'msg': '未登录'
            }

        # 内容
        comment = request.form.get('comment')
        # 攻略id
        strategy_id = request.form.get('strategyid')
        # 主评论id
        user_id = request.form.get('mainid') or 0
        # 子评论id
        r_id = request.form.get('rid') or 0

        # 没有攻略id
        if not strategy_id:
            return {
                'status': 1,
                'msg': '攻略id为空'
            }
        # 内容为空,
        if not comment:
            return {
                'status': 1,
                'msg': '评论内容为空'
            }
        # 子评论
        if user_id:
            if r_id:
                recom = Recomment()
                recom.nt_content = comment
                recom.nt_parentid = user_id
                recom.nt_user = id
                # zi评论id 获取名字
                zi_ping = Recomment.query.filter(Recomment.nt_id == r_id).all()
                name_id = zi_ping[0].nt_user
                name = User.query.get(name_id).u_name
                recom.nt_bname = name
                db.session.add(recom)
                db.session.commit()

                # 增加评论数
                pinglun = Strategy.query.get(strategy_id)
                pinglun.s_collectnum = int(pinglun.s_collectnum) + 1
                db.session.commit()
                return {
                    'status': 0,
                    'msg': 'zi评论回复成功'
                }
            recom = Recomment()
            recom.nt_content = comment
            recom.nt_parentid = user_id
            recom.nt_user = id
            # 主评论id 获取名字
            zi_ping = Comment.query.filter(Comment.com_id == user_id).all()
            name_id = zi_ping[0].co_user
            name = User.query.get(name_id).u_name
            recom.nt_bname = name
            db.session.add(recom)
            db.session.commit()
            return {
                'status': 0,
                'msg': '回复主评论成功'
            }

        # 主评论
        com = Comment()
        com.c_content = comment
        com.c_strategy = strategy_id
        com.co_user = id

        db.session.add(com)
        db.session.commit()
        return {
            'status':0,
            'msg':'主评论发表成功'
                }
