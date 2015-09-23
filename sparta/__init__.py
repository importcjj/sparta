# -*- coding:utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sparta.configure import (
    create_app_with,
    DevConfigure
)


app = create_app_with(
    Flask(__name__),
    DevConfigure
)

db = SQLAlchemy(app)


from sparta.api import blueprint_register
app = blueprint_register(app)
