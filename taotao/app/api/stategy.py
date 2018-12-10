from flask import request
from flask_restful import Resource, fields, marshal

# 数据结构化
from app.models import Strategy

stategys_info = {
    'id' : fields.Integer(attribute='s_id'),
    'name':fields.String(attribute='s_name'),
    'img':fields.String(attribute='s_img'),
    'collectnum':fields.String(attribute='s_collectnum'),
    'commentnum':fields.String(attribute='s_commentnum')
}


# 攻略
class CategoryModel(Resource):
    def get(self):
        page = int(request.args.get('page'))
        size = int(request.args.get('size'))

        strategy = Strategy.query.all().limit(size).offset((page-1) * size)

        strategy_fields={
            'status':fields.Integer,
            'strategy':fields.Nested(stategys_info)
        }

        res = marshal({'status':1,'strategy':strategy},strategy_fields)

        return res






