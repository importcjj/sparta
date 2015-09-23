# -*- coding:utf-8 -*-
try:
    import sparta.sparta_config as Z
except ImportError:
    import sparta.setting as Z


class Basic:
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
            **Z.MYSQL)
    HOST = '0.0.0.0'


class DevConfigure(Basic):
    DEBUG = True


class ProdConfigure(Basic):
    pass


def create_app_with(app, config):
    app.config.from_object(config)
    return app
