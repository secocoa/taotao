import os


def get_db_uri(dbinfo):
    username = dbinfo.get('user') or "taotao"
    password = dbinfo.get('pwd') or "123456"
    host = dbinfo.get('host') or "taotao.buildup.vip"
    port = dbinfo.get('port') or "3306"
    database = dbinfo.get('dbname') or "taotao"
    driver = dbinfo.get('driver') or "pymysql"
    dialect = dbinfo.get('dialect') or "mysql"

    return "{}+{}://{}:{}@{}:{}/{}".format(dialect,driver,username,password,host,port,database)



class Config():
    DEBUG = False
    TESTING = False
    SECRET_KEY = '110'
    SESSION_TYPE = 'redis'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False




class DevelopConfig(Config):
    DEBUG = True
    MAIL_SERVER = "smtp.163.com"
    MAIL_USERNAME = "m18937610182@163.com"
    MAIL_PASSWORD = "19910320hu"




    DATABASE = {
        "user": "taotao",
        "pwd": "123456",
        "host": "taotao.buildup.vip",
        "port": "3306",
        "dialect": "mysql",
        "driver": "pymysql",
        "dbname": "taotao",

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class TestingConfig(Config):
    TESTING = True

    DATABASE = {
        "user": "taotao",
        "pwd": "123456",
        "host": "taotao.buildup.vip",
        "port": "3306",
        "dialect": "mysql",
        "driver": "pymysql",
        "dbname": "taotao",

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class ShowConfig(Config):
    DEBUG = True

    DATABASE = {
        "user": "taotao",
        "pwd": "123456",
        "host": "taotao.buildup.vip",
        "port": "3306",
        "dialect": "mysql",
        "driver": "pymysql",
        "dbname": "taotao",

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class ProductConfig(Config):
    DEBUG = True

    DATABASE = {
        "user": "taotao",
        "pwd": "123456",
        "host": "taotao.buildup.vip",
        "port": "3306",
        "dialect": "mysql",
        "driver": "pymysql",
        "dbname": "taotao",

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


config = {
    "developConfig" : DevelopConfig,
    "testingConfig" : TestingConfig,
    "showConfig" : ShowConfig,
    "productConfig" : ProductConfig,
    "default" : DevelopConfig,
}