# -*- coding:utf-8 -*-
import os
import flask
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sparta.configure import (
    create_app_with,
    DevConfigure,
    ProdConfigure
)


app = create_app_with(
    Flask(__name__),
    ProdConfigure if os.environ.get('produce') else DevConfigure
)

db = SQLAlchemy(app)


from sparta.api import blueprint_register
app = blueprint_register(app)


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('linechart.html')


@app.errorhandler(404)
def notfound(error):
    return flask.redirect('/')
