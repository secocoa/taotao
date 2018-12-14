import os

from flask import request, session
from flask_restful import Resource, fields, marshal

from app.models import Comment, User, Recomment

comment_info = {
    'content': fields.String(attribute='c_content'),
    'id' : fields.Integer(attribute='com_id'),
}
recomment_info = {
    'content':fields.String(attribute='nt_content'),
    'name': fields.String(attribute='nt_bname'),
    'id':fields.Integer(attribute='nt_id')
}
user_info = {
    'name':fields.String(attribute='u_name')
}
class Cqre(Resource):
    def get(self):
        comments = Comment.query.all()
        print(comments)

        cuid = [comment.co_user for comment in comments]
        print(cuid)
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

                reuser_dic[recomment.nt_id] = fields.Nested(user_info)
                return_reuser_dic[recomment.nt_id] = reuser


        res_info = {
            'ceshi':fields.String,
            'return_comment': fields.List(fields.Nested(comment_info)),
            'return_recomments_dic':fields.Nested(recomments_dic),
            'return_reuser_dic':fields.Nested(reuser_dic)


        }
        return marshal({
            'return_comment': comments,
            'ceshi' : "i'm tired",
            'return_recomments_dic':  return_recomments_dic,
            'return_reuser_dic':return_reuser_dic,
        },res_info)





class Changeuinfo(Resource):
    def get(self):
        uid = session.get('id')
        if not uid:
            return {
                'status' : 1,
                'msg': '请先登录',
            }
        user = User.query.filter(User.u_id == uid).first()

        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        return {
            'uname': basedir
        }