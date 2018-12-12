from flask import session, request, make_response, jsonify
from flask_restful import Resource, fields, marshal_with
from sqlalchemy import and_

from app.models import Goods, Cart, db, Re_address, User, Paygoods, Deal


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

class Payre(Resource):
    def post(self):
        userid = session.get('id')
        if not userid:
            return {
                'status': 1,
                'msg': '用户未登录 请登录',
            }
        gid = request.form.get('id')

        good = Goods.query.filter(Goods.g_id==gid).first()
        adresses = Re_address.query.filter(and_(Re_address.re_user == userid,Re_address.is_default==1)).first()
        if not good:
            return {
                'status': 1,
                'msg': '未选中商品',
            }
        if not adresses:
            return {
                "province": None,
                "city": None,
                "name": None,
                "phone": None,
                "address":None,
                "postalcode":None,
                "gimg":good.g_img,
                "gprice":good.g_price,
                "gname":good.g_name,
                "gid":good.g_id,
            }
        return {
            "province": adresses.country,
            "city": adresses.city,
            "name": adresses.re_name,
            "phone": adresses.phone,
            "address": adresses.detail_address,
            "postalcode": adresses.postalcode,
            "gimg": good.g_img,
            "gprice": good.g_price,
            "gname": good.g_name,
            "gid": good.g_id,
        }
goods_info = {
    "img": fields.String(attribute='g_img'),
    "price": fields.String(attribute='g_price'),
    "name": fields.String(attribute='g_name'),
    "id": fields.Integer(attribute='g_id'),
}
cart_info = {
    'num':fields.Integer(attribute='goodsnum')

}
return_value = {
    "status": fields.Integer,
    "province": fields.String,
    "city": fields.String,
    "name": fields.String,
    "phone": fields.String,
    "address": fields.String,
    "postalcode": fields.String,

    "nums": fields.List(fields.Nested(cart_info)),
    "goods":fields.List(fields.Nested(goods_info)),
}
class Paysre(Resource):
    @marshal_with(return_value)
    def post(self):
        gid = request.form.get('id')
        print(type(gid))
        userid = 4
        print(userid)
        if not userid:
            return {
                'status': 1,
                'msg': '用户未登录 请登录',
            }
        if not gid:
            return {
                'status': 1,
                'msg': '未选中商品',
            }
        good = Goods.query.filter(Goods.g_id.in_(gid)).all()       #商品表
        cartgood = Cart.query.filter(Cart.ca_goods.in_(gid)).all() #购物车表
        adresses = Re_address.query.filter(and_(Re_address.re_user == userid,Re_address.is_default==1)).first()
        print(good)


        return  {
            "status": 1,
            "province": adresses.country,
            "city": adresses.city,
            "name": adresses.re_name,
            "phone": adresses.phone,
            "address": adresses.detail_address,
            "postalcode": adresses.postalcode,
            'nums':cartgood,
            'goods':good,
        }

class Delre(Resource):
    def post(self):
        # userid = session.get('id')
        userid = 4
        id = request.form.get("id")
        print(id)
        nums = request.form.get("num")
        print(nums)
        #将传过来的字符串数组化
        id =eval(id)
        nums =eval(nums)
        print(type(id))
        print(nums)
        # ps 创建 大订单对象 并通过用户最新的订单获得大订单id
        deal = Deal()
        deal.d_user = userid
        db.session.add(deal)
        db.session.commit()
        deal = Deal.query.filter(Deal.d_user==userid).order_by(-Deal.d_id).first()
        print(deal.d_id)
        did = deal.d_id
        index = 0
        if len(id)== 1:
            good = Goods.query.filter(Goods.g_id.in_( id)).first()
            paygood = Paygoods()
            paygood.pa_user = userid
            paygood.pa_goods = good.g_id
            paygood.is_pay = 1
            paygood.pa_deal = did
            paygood.pgoodsnum = nums[0]
            db.session.add(paygood)
            db.session.commit()
            cartgood = Cart.query.filter(Goods.g_id.in_(id)).first()
            if not cartgood:
                return {
                    'status': 0,
                    'msg':'提交订单成功',
                }
            db.session.delete(cartgood)
            db.session.commit()
            return {
                'status': 0,
                'msg': '提交订单成功',
            }
        goods = Goods.query.filter(Goods.g_id.in_(id)).all()

        for good in goods:
            print(good)
            paygood = Paygoods()
            paygood.pa_user = userid
            paygood.pa_goods = good.g_id
            paygood.is_pay = 1
            paygood.pa_deal = did
            paygood.pgoodsnum =nums[index]
            db.session.add(paygood)
            db.session.commit()
            index += 1
            cartgood = Cart.query.filter(Cart.ca_goods==good.g_id).first()
            db.session.delete(cartgood)
            db.session.commit()
        return {
            'status': 0,
            'msg': '提交订单成功'
        }

class Moneyre(Resource):
    def post(self):
        userid = session.get('id')
        #获取商品交易记录最新的用户交易记录

        #根据外键找到订单表里未支付的订单

        #将订单的状态设为已购买

        #返回状态码

        #大功告成



