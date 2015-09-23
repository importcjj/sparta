# -*- coding:utf-8 -*-
from flask import Blueprint
from flask.ext.restful import (
    Api,
    reqparse,
    Resource
)

from sparta.module import base as module_base

Base = Blueprint('Base', __name__)


class OutLine(Resource):

    def __init__(self):
        pass

    def get(self):
        return module_base.analyse_one()


base_api = Api(Base)
base_api.add_resource(OutLine, '/latest')
