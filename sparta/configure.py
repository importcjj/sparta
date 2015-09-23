# -*- coding:utf-8 -*-
try:
    import sparta.sparta_config as Z
except ImportError:
    import sparta.setting as Z
import logging
from logging.handlers import RotatingFileHandler


class Basic:
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
            **Z.MYSQL)


class DevConfigure(Basic):
    DEBUG = True


class ProdConfigure(Basic):
    pass


def create_app_with(app, config):
    app.config.from_object(config)
    filehandler = RotatingFileHandler('log/kratos.log', mode='a')
    filehandler.setLevel(logging.NOTSET)
    app.logger.addHandler(filehandler)
    return app
