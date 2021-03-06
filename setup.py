# -*- coding:utf-8 -*-

from setuptools import setup


setup(
    name="sparta",
    version=0.1,
    description="douyu statistics backend",
    long_description="douyu statistics backend",
    author="jiaju.chen",
    author_mail="jiaju.chen@ele.me",
    install_requires=[
        'Flask==0.10.1',
        'Flask-RESTful==0.3.4',
        'Flask-SQLAlchemy==2.0',
        'hiredis==0.2.0',
        'redis==2.10.3'
    ]
)
