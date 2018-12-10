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
        page = int(request.args.get('page') or 1)
        size = int(request.args.get('size') or 3)

        strategy = Strategy.query.paginate(page=page,per_page=size).items
        print(strategy,type(strategy))
        strategy_fields={
            'status':fields.Integer,
            'strategy':fields.List(fields.Nested(stategys_info)),
        }

        return marshal({'status':1,'strategy':strategy},strategy_fields)








