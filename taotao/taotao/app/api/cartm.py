from flask import request, session, make_response
from flask.json import jsonify
from flask_restful import Resource, fields, marshal_with, reqparse
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
parse = reqparse.RequestParser()
parse.add_argument("id",type=int,help='未传入id')
parse.add_argument("cid",type=list,help='未传入id')
class CartResource(Resource):
    @marshal_with(return_cartvalueq)
    def get(self):
        id = session.get('id')
        print(id)

        cid = request.args.get('cid')
        print(cid)

        if not id: # 判断是否登录
            return {
                'status': 1,
                'msg': '请先登录',
            }
        cartgoods = Cart.query.filter(Cart.ca_user==id).all() #获取购物车中商品
        print(cartgoods)
        c_id = []
        for cartgood in cartgoods:     #获得购物车表单中关联的商品id  放入c_id列表中
            c_id.append(cartgood.ca_goods)
        print(c_id)
        goods = Goods.query.filter(Goods.g_id.in_(c_id)).all() #购物车中用户的商品对象
        print(goods)
        return {
            'status': 0,
            'nums': cartgoods,
            'cartgoods':goods,
        }
    def post(self):
        uid = session.get('id') #获取用户id
        if not uid: #判断用户是否登录
            return  {
                'status':1,
                'msg':'添加失败,请用户先登录'
            }
        args = parse.parse_args()
        gid  = args.get('id')
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
    def delete(self):
        # args = parse.parse_args()
        # id = args.get('cid')

        id = request.args.get('cid')
        print(id)
        cartgoods = Cart.query.filter(Cart.cartid.in_(id)).all()
        if not cartgoods:
            return {
                'status': 0,
                'msg': '删除发生错误'
            }
        db.session.delete(cartgoods)
        db.session.commit()

        response = jsonify({'status':1,})

        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

        return response


class Cartres(Resource):
    def get(self):
        print(request.args)
        id = request.args.get('cid')

        print(id)


        cartgoods = Cart.query.filter(Cart.cartid.in_(id)).all()
        print(cartgoods)
        response1 = jsonify({'status': 1,'msg':'删除发生错误' })

        response1.headers['Access-Control-Allow-Origin'] = '*'
        response1.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response1.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

        if not cartgoods:
            return response1
        for cartgood in cartgoods:
            db.session.delete(cartgood)
            db.session.commit()
        response = jsonify({'status': 1,'msg': '删除成功'})

        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'


        return response