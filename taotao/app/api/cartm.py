from flask import request, session, make_response, jsonify
from flask_restful import Resource, fields, marshal_with

from app.models import User, db, Re_address, Cart, Goods


#格式化商品表
goodsq_info = {
    'name': fields.String(attribute='g_name'),
    'img':fields.String(attribute='g_img'),
    'id': fields.Integer(attribute='g_id'),
    'price':fields.String(attribute='g_price')
}
#格式化购物车表
cartgoodq_info = {
    'num': fields.Integer(attribute='goodsnum')
}
#序列化返回数据
return_cartvalueq = {
    'status': fields.Integer,
    'cartgoods':fields.List(fields.Nested(goodsq_info)),
    'nums': fields.List(fields.Nested(cartgoodq_info))
}
class CartResource(Resource):
    @marshal_with(return_cartvalueq)
    def get(self):
        id = session.get('id')
        if not id: # 判断是否登录
            return {
                'status': 1,
                'msg': '请先登录',
            }
        cartgoods = Cart.query.filter(Cart.ca_user==id).all() #获取购物车中商品
        c_id = []
        for cartgood in cartgoods:     #获得购物车表单中关联的商品id  放入c_id列表中
            c_id.append(cartgood.ca_goods)

        goods = Goods.query.filter(Goods.g_id.in_(c_id)).all() #购物车中用户的商品对象
        res =  {
            'status': 0,
            'nums': cartgoods,
            'cartgoods':goods,
        }
        return res
    def post(self):
        uid = session.get('id') #获取用户id
        if not uid: #判断用户是否登录
            return  {
                'status':1,
                'msg':'添加失败,请用户先登录'
            }
        gid  = request.form.get('id')
        cartgood = Cart.query.filter(Cart.ca_goods==gid).first()
        if cartgood: #判断购物车是否存在该商品 若是存在则购物车商品数目 + 1
            cartgood.goodsnum += 1
            db.session.commit()
            return {
                'status':0,
                'msg': '添加成功，在购物车等亲～',
            }
        cartgood = Cart(goodsnum=1,ca_user=uid,ca_goods=gid)
        db.session.add(cartgood)
        db.session.commit()
        return {
            'status': 0,
            'msg': '添加成功，在购物车等亲～',
        }
class Cartbk(Resource):
    def get(self):
        id = request.args.get('cid')
        cartgoods = Cart.query.filter(Cart.ca_goods.in_(id))
        if not cartgoods:
            return {
                'status':1,
                'msg': '删除失败'
            }
        for cartgood in cartgoods:
            db.session.delete(cartgood)
            db.session.commit()
        return {
            'status':0,
            'msg': '删除成功'
        }
