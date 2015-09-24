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


class Overview(Resource):

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument(
            'from_index', type=int, location='json')
        self.get_parser.add_argument(
            'limit', type=int, location='json')

    def get(self):
        args = self.get_parser.parse_args()
        return module_base.outline_section(**args)


class Type(Resource):

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument(
            'from_index', type=int, location='json')
        self.get_parser.add_argument(
            'limit', type=int, location='json')

    def get(self):
        return module_base.zbtype_section()


base_api = Api(Base)
base_api.add_resource(OutLine, '/latest')
base_api.add_resource(Overview, '/sections')
base_api.add_resource(Type, '/type')
