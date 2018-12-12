from flask_restful import Api



from app.api.addressm import AddressModel

from app.api.cartm import CartResource, Cartbk
from app.api.cartnum import CartnumResource, Payre, Paysre, Delre

from app.api.collectm import CollectModel

from app.api.goodsm import GoodsModel

from app.api.stategy import CategoryModel

from app.api.home import Home, Category_good, StrategyContent

from app.api.userm import UserModel

api = Api()
def init_urls(app):
    api.init_app(app)
# 登录注册
api.add_resource(UserModel,'/user/')



# 攻略
api.add_resource(CategoryModel,'/strategy/')

# 地址
api.add_resource(AddressModel,'/address/')
# 商品详情
api.add_resource(GoodsModel,'/good/')
# 收藏
api.add_resource(CollectModel,'/collect/')






# 首页
api.add_resource(Home,'/')
# 首页分类详情
api.add_resource(Category_good,'/category/')
# 攻略详情页面
api.add_resource(StrategyContent,'/article/')


#购物车增加以及展示
api.add_resource(CartResource,'/cart/')
#购物车删除
api.add_resource(Cartbk,'/cartbk/')
#购物车加减
api.add_resource(CartnumResource,'/cartgnum/')
#立即购买
api.add_resource(Payre,'/pay/')
#购物车结算
api.add_resource(Paysre,'/pays/')
#提交订单
api.add_resource(Delre,'/deal/')
#支付