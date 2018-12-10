

from flask import session, request
from flask_restful import fields, Resource, marshal


from app.models import Re_address, db

waddresses_info = {
    'province': fields.String(attribute='country'),
    'city': fields.String(attribute='city'),
    'detail': fields.String(attribute='detail_address'),
    'default': fields.Boolean(attribute='is_default'),
    'phone':fields.String(attribute='phone'),
    'name':fields.String(attribute='re_name')

}

class AddressModel(Resource):
    def get(self):
        id = session.get('id')
        print(id)
        # 判断是否登录
        if id :
            addresses = Re_address.query.filter(Re_address.re_user==id).all()
            print(addresses,type(addresses))
            addresses_info = {
                'msg':fields.String,
                'status':fields.Integer,
                'addresses':fields.List(fields.Nested(waddresses_info))
            }
            # 判断是否有地址
            if len(addresses) > 0:
                return marshal({'msg':'返回成功','status':1,'addresses':addresses},addresses_info)
            return {'msg':'没有地址，请先添加','status':0}
        else:
            return {'msg': '请先登录', 'status': 0}
    def post(self):
        id = session.get('id')
        country = request.form.get('province')
        city = request.form.get('city')
        detail_address = request.form.get('detail')
        postalcode = request.form.get('postalcode')
        name = request.form.get('name')
        phone = request.form.get('phone')
        # 判断手机号长度是否为11位
        if len(phone) != 11:
            return {'msg': '手机号只能为11位', 'status': 0}
        id_num = request.form.get('idcard')
        is_default = int(request.form.get('default'))
        # 设置默认地址
        if is_default == 1:
            addresses = Re_address.query.filter(Re_address.re_user == id).all()
            if len(addresses) > 0:
                for j in addresses:
                    j.is_default = 0
                    db.session.add(j)
                    db.session.commit()
        address = Re_address()
        address.re_user = id
        address.country = country
        address.city = city
        address.detail_address = detail_address
        address.re_name = name
        address.phone = phone
        address.id_num = id_num
        address.postalcode = postalcode
        address.is_default = is_default
        db.session.add(address)
        db.session.commit()
        return {'msg':'OK','status':1}