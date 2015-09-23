# -*- coding:utf-8 -*-
from sparta import db

from sparta.model import (
    Index,
    Outline
)
from datetime import datetime


def _total_viewer(cards):
    return sum([card.zbViewer for card in cards])


def _top_one(f, type):
    pass


def analyse_one(index=None):
    latest_index_obj = Index.latest()
    last_index = latest_index_obj.id
    if not index:
        index = last_index
    if index > last_index or index < 0:
        return

    cards = Outline.get_by_index(index)
    outline = dict()
    outline['created_at'] = datetime.strftime(
        latest_index_obj.created_at, '%Y-%m-%d %H:%M')
    outline['total_viewer'] = float(_total_viewer(cards))
    outline['zbTypes'] = []
    rooms = db.session.query(
        Outline.zbType,
        db.func.sum(Outline.zbViewer),
        db.func.count(Outline.id)).\
        filter_by(crawlIndex=index).\
        group_by(Outline.zbType).\
        order_by(db.func.sum(Outline.zbViewer).desc()).\
        all()
    for room in rooms:
        zb = {}
        zb['zbType'] = room[0]
        zb['zbViewer'] = int(room[1])
        zb['rooms'] = room[2]
        zb['percent'] = float(
            '{:0.2f}'.format(zb['zbViewer'] / outline['total_viewer'] * 100))
        top_one = sorted(
            filter(lambda y: y.zbType == zb['zbType'], cards),
            key=lambda x: x.zbViewer,
            reverse=True
        )[0]
        zb['top_one'] = {
            'Title': top_one.zbTitle,
            'player': top_one.zbPlayer,
            'viewer': top_one.zbViewer
        }
        outline['zbTypes'].append(zb)

    return outline
