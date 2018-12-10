from flask import request, session
from flask_restful import Resource

from sqlalchemy import and_
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app.models import User, db, Re_address


class UserModel(Resource):
    def get(self):
        username = request.args.get('username')
        password = request.args.get('password')
        print(username)
        # 输入是否为空
        if not username:
            return  {'status': 1,'msg':'请输入账号'}
        if not password:
            return  {'status': 1,'msg':'请输入密码'}
        user = User.query.filter(User.u_name==username)
        #用户是否存在
        if user.count() == 0 :
            return {'status': 1,'msg':'用户名或者密码错误'}

        user = user.first()
        if check_password_hash(user.u_password,password):
            gold = user.u_gold
            intergration = user.u_intergration
            id = user.u_id
            address = Re_address.query.filter(and_(Re_address.r_id==id,Re_address.is_default==1)).first()
            session['username'] = username
            session['id'] = id
            if not address:
                return {
                    'status': 0,
                    'msg': '登录成功',
                    'gold': gold,
                    'intergration': intergration,
                    'province':None,
                    'city': None,
                    'name': None,
                    'phone': None,
                    'address': None,
                }
            province = address.country
            city = address.city
            name = address.re_name
            phone = address.phone
            address = address.detail_address
            return {
                'status':0,
                'msg': '登录成功',
                'gold':gold,
                'intergration': intergration,
                'province':province,
                'city': city,
                'name':name,
                'phone':phone,
                'address':address,
            }
        return  {
            'status': 1,
            'msg':'登录失败'
        }

    def post(self):
        uname = request.form.get('Username')
        password = request.form.get('Password')
        if len(password) < 6:
            return {'msg': '密码需要至少6位', 'status': 0}
        password = generate_password_hash(password)
        email = request.form.get('email')
        unames = User.query.filter(User.u_name == uname).all()
        emails = User.query.filter(User.u_email == email).all()
        # 判断用户名和邮箱是否存在
        if len(emails) == 0 and len(unames) == 0:
            user = User()
            user.u_email = email
            user.u_name = uname
            user.u_password = password
            db.session.add(user)
            db.session.commit()
            return {'msg':'注册成功','status':1}
        else:
            if len(emails) > 0:
                return {'msg': '注册失败,邮箱已存在', 'status': 0}
            return {'msg': '注册失败,用户名已存在', 'status': 0}

