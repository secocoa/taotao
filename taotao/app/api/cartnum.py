from flask import session, request
from flask_restful import Resource
from sqlalchemy import and_

from app.models import Goods, Cart, db


class CartnumResource(Resource):
    def post(self):
        userid = session.get('id')
        if not userid:
            return {
                'status':1,
                'msg': '用户未登录 请登录',
            }
        gid = request.form.get('id')
        if not gid :
            return {
                'status': 1,
                'msg': '未选中商品',
            }
        cartgood = Cart.query.filter(and_(Cart.ca_goods == gid,Cart.ca_user == userid)).first()
        if not cartgood :
            return {
                'status':1,
                'msg': '未获得商品',
            }
        cartgood.goodsnum += 1
        db.session.commit()
        return {
            'status': 0,
            'msg':'操作成功'
        }
    def delete(self):
        userid = session.get('id')
        if not userid:
            return {
                'status': 1,
                'msg': '用户未登录 请登录',
            }
        gid = request.args.get('id')
        if not gid:
            return {
                'status': 1,
                'msg': '未选中商品',
            }
        cartgood = Cart.query.filter(and_(Cart.ca_goods == gid, Cart.ca_user == userid)).first()
        if not cartgood:
            return {
                'status': 1,
                'msg': '未获得商品',
            }
        if cartgood.goodsnum == 1:
            return {
                'status': 1,
                'msg': '亲，不能再减少了'
            }
        cartgood.goodsnum -= 1
        db.session.commit()
        return {
            'status': 0,
            'msg':'操作成功'
        }