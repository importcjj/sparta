# -*- coding:utf-8 -*-


from sparta import db


class Outline(db.Model):
    __tablename__ = 'tb_card'
    __fields__ = ['crawlIndex', 'zbTitle', 'zbPlayer', 'zbViewer', 'zbType']

    id = db.Column(db.Integer, primary_key=True)
    crawlIndex = db.Column(db.Integer, default=0)
    zbTitle = db.Column(db.String(255), default='')
    zbPlayer = db.Column(db.String(255), default='')
    zbViewer = db.Column(db.Integer, default=0)
    zbType = db.Column(db.String(255), default='')

    @classmethod
    def get_by_index(cls, index):
        return cls.query.filter_by(crawlIndex=index).all()


class Index(db.Model):
    __tablename__ = 'tb_index'
    __fields__ = ['id', 'created_at']

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)

    @classmethod
    def latest(cls):
        return cls.query.order_by(cls.id.desc()).limit(1).first()
