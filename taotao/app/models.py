from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# 轮播图
class Slideshow(db.Model):

    e_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 商品ID
    goods_id = db.Column(db.Integer)
# 用户表
class User(db.Model):

    u_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 用户名
    u_name = db.Column(db.String(64),unique=True)
    # 密码
    u_password = db.Column(db.String(512))
    # 邮箱
    u_email = db.Column(db.String(64))
    # 积分
    u_intergration = db.Column(db.String(128),default='0')
    # 金币
    u_gold = db.Column(db.String(128),default='0')
    # 出生日期
    u_date = db.Column(db.String(64))
    # 会员
    is_vip = db.Column(db.Boolean,default=False)
    # 删除
    is_delete = db.Column(db.Boolean,default=False)
    # 地址反向
    re_address = db.relationship('Re_address',backref='user')
    # 收藏反向
    collect = db.relationship('Collect', backref='user')
    # 攻略评论反向
    comment = db.relationship('Comment', backref='user')
    # 购物车反向
    cart = db.relationship('Cart', backref='user')
    # 订单反向
    paygoods = db.relationship('Paygoods', backref='user')
    # 商品评价反向
    evaluate= db.relationship('Evaluate', backref='user')



# 收藏表
class Collect(db.Model):
    collectid = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 商品是否
    is_good = db.Column(db.Boolean,default=False)
    # 用户外键
    c_user = db.Column(db.Integer,db.ForeignKey('user.u_id'))
    # 商品外键
    c_goods = db.Column(db.Integer,db.ForeignKey('goods.g_id'))
    # 攻略外键
    c_strategy = db.Column(db.Integer,db.ForeignKey('strategy.s_id'))

# 商品表
class Goods(db.Model):
    g_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 商品名称
    g_name = db.Column(db.String(128))
    # 商品信息
    g_information = db.Column(db.Text)
    # 商品价格
    g_price = db.Column(db.String(64))
    # 促销价格
    g_saleprice = db.Column(db.String(64))
    # 图片
    g_img = db.Column(db.Text)
    # 收藏数目
    g_collectnum = db.Column(db.String(64))
    # 评论数目
    g_commentnum = db.Column(db.String(64))
    # 精选
    is_chioce = db.Column(db.Boolean,default=False)
    # 删除
    is_delete = db.Column(db.Boolean,default=False)
    # 商品外键
    category = db.Column(db.Integer,db.ForeignKey('category.categoryid'))
    # 收藏反向
    collect = db.relationship('Collect', backref='goods')
    # 购物车反向
    cart = db.relationship('Cart', backref='goods')
    # 商品评论反向
    g_evaluate = db.relationship('Evaluate',backref='goods',lazy='dynamic')




# 商品分类表
class Category(db.Model):
    categoryid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #分类
    c_name = db.Column(db.String(32))
    # 商品反向
    # goods = db.relationship('Goods',backref='category')

#收货地址表
class Re_address(db.Model):
    r_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #国家
    country = db.Column(db.String(64))
    # 市区
    city = db.Column(db.String(64))
    # 具体地址
    detail_address = db.Column(db.String(512))
    # 邮政编码
    postalcode = db.Column(db.String(64))
    # 收件人姓名
    re_name = db.Column(db.String(64))
    # 电话
    phone = db.Column(db.String(64))
    # 身份证号码
    id_num = db.Column(db.String(128))
    # 删除
    is_delete = db.Column(db.Boolean, default=False)
    # 默认
    is_default = db.Column(db.Boolean,default=False)
    #用户外键
    re_user = db.Column(db.Integer,db.ForeignKey('user.u_id'))


# 商品标签
class Tags(db.Model):
    t_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(64))
    is_delete = db.Column(db.Boolean,default=False)


# 攻略表
class Strategy(db.Model):
    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 题目
    s_name = db.Column(db.String(64))
    # 内容
    s_context = db.Column(db.Text)
    # 阅读量
    s_readnum = db.Column(db.String(64))
    # 图片表
    s_image = db.Column(db.Text)
    # 评论数
    s_commentnum = db.Column(db.String(64))
    # 收藏数目
    s_collectnum = db.Column(db.String(64))
    # 删除
    is_delete = db.Column(db.Boolean,default=False)
# 攻略评论表
class Comment(db.Model):
    com_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 时间
    c_time = db.Column(db.DateTime,default=datetime.now)
    # 内容
    c_content = db.Column(db.Text)
    # 用户外键
    co_user = db.Column(db.Integer,db.ForeignKey('user.u_id'))
    # 攻略外键
    c_strategy = db.Column(db.Integer,db.ForeignKey('strategy.s_id'))

# 购物车表
class Cart(db.Model):
    cartid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 商品数量
    goodsnum = db.Column(db.Integer)
    # 用户外键
    ca_user = db.Column(db.Integer,db.ForeignKey('user.u_id'))
    # 商品外键
    ca_goods = db.Column(db.Integer,db.ForeignKey('goods.g_id'))


# 订单表
class Paygoods(db.Model):
    paygoodsid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 待付款
    is_pay = db.Column(db.Boolean,default=False)
    # 待收货
    is_getgood = db.Column(db.Boolean,default=False)
    # 待发货
    is_sendgood = db.Column(db.Boolean,default=False)
    # 取消
    is_cancel = db.Column(db.Boolean,default=False)
    # 用户外键
    pa_user = db.Column(db.Integer, db.ForeignKey('user.u_id'))
    # 商品数目
    pgoodsnum = db.Column(db.Integer)
    # 商品外键
    pa_goods = db.Column(db.Integer, db.ForeignKey('goods.g_id'))
    # 交易记录表外键
    pa_deal = db.Column(db.Integer,db.ForeignKey('deal.d_id'))

# 评价商品表
class Evaluate(db.Model):
    e_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 内容
    e_content = db.Column(db.Text)
    # 时间
    e_time = db.Column(db.DateTime, default=datetime.now)
    # 用户外键
    ev_user = db.Column(db.Integer, db.ForeignKey('user.u_id'))
    # 攻略外键
    ev_goods = db.Column(db.Integer, db.ForeignKey('goods.g_id'))


# 中间表taotao
class Tag_Goods(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    t_id = db.Column(db.Integer,db.ForeignKey('tags.t_id'))
    g_id = db.Column(db.Integer,db.ForeignKey('goods.g_id'))
# 商品交易记录表
class Deal(db.Model):
    d_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 时间
    time = db.Column(db.DateTime,default=datetime.now)
    # 用户外键
    d_user = db.Column(db.Integer,db.ForeignKey('user.u_id'))
<<<<<<< HEAD
    # 订单外键
    # d_pay = db.Column(db.Integer,db.ForeignKey('paygoods.paygoodsid'))
=======
>>>>>>> 57bc97c4d672bfbaaf3e0388179046d804d2e9e1
# 商品回复评论表
class Reevaluate(db.Model):
    # 评论ID
    te_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 评论内容
    te_content = db.Column(db.Text)
    # 父ID
    te_parentid = db.Column(db.Integer)
    # 评论时间
    te_time = db.Column(db.DateTime,default=datetime.now)
    # 被评论人名字
    te_bname = db.Column(db.String(64))
    # 用户外键
    te_user = db.Column(db.Integer,db.ForeignKey('user.u_id'))
# 攻略回复评论表
class Recomment(db.Model):
    # 评论ID
    nt_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 评论内容
    nt_content = db.Column(db.Text)
    # 父ID
    nt_parentid = db.Column(db.Integer)
    # 评论时间
    nt_time = db.Column(db.DateTime,default=datetime.now)
    # 被评论人名字
    nt_bname = db.Column(db.String(64))
    # 用户外键
    nt_user = db.Column(db.Integer,db.ForeignKey('user.u_id'))