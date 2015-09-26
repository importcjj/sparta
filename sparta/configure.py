# -*- coding:utf-8 -*-
try:
    import sparta.sparta_config as Z
except ImportError:
    import sparta.setting as Z
import logging.config


class Basic:
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
            **Z.MYSQL)


class DevConfigure(Basic):
    DEBUG = False


class ProdConfigure(Basic):
    pass


def create_app_with(app, config):
    app.config.from_object(config)
    if not app.debug:
        logging.config.dictConfig(Z.LOGGING)
    return app
