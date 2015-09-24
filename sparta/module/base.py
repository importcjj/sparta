# -*- coding:utf-8 -*-
from sparta import db

from sparta.model import (
    Index,
    Outline
)
import time


def _total_viewer(cards):
    return sum([card.zbViewer for card in cards])


def _top_one(f, type):
    pass


def _section_judge(from_index, limit, max_limit=144):
    latest_index_obj = Index.latest()
    last_index = latest_index_obj.id
    if not limit:
        limit = 144
    if not from_index:
        from_index = last_index
    if limit > max_limit:
        limit = max_limit
    to_index = from_index - limit + 1
    if to_index < 0:
        to_index = 0

    return range(to_index, from_index + 1)


def analyse_one(index=None):
    latest_index_obj = Index.latest()
    last_index = latest_index_obj.id
    if not index:
        index = last_index
    if index > last_index or index < 0:
        return

    cards = Outline.get_by_index(index)
    outline = dict()
    outline['created_at'] = time.mktime(
        latest_index_obj.created_at.timetuple())
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


def outline_section(from_index=None, limit=None):

    indexs = _section_judge(from_index, limit)
    sections = db.session.query(
        Outline.crawlIndex,
        db.func.count(Outline.id),
        db.func.sum(Outline.zbViewer)
    ).\
        filter(Outline.crawlIndex.in_(indexs)).\
        group_by(Outline.crawlIndex).all()

    section_lists = []
    for section in sections:
        sec = {}
        sec['index'] = section[0]
        sec['created_at'] = \
            time.mktime(
            Index.query.
            filter_by(id=sec['index']).first().created_at.timetuple())
        sec['zbRooms'] = section[1]
        sec['zbViewer'] = float(section[2])
        section_lists.append(sec)
    return section_lists


def zbtype_section(from_index=None, limit=None):
    indexs = _section_judge(from_index, limit=20)
    sections = []
    for index in indexs:
        index_types = {}
        card = db.session.query(Outline.created_at, db.func.sum(Outline.zbViewer)).\
            filter_by(crawlIndex=index).first()
        total_viewer = float(card[1])
        index_types['created_at'] = time.mktime(card[0].timetuple())
        info_by_types = db.session.query(Outline.zbType, db.func.sum(
            Outline.zbViewer)).\
            filter_by(crawlIndex=index).\
            group_by(Outline.zbType).\
            order_by(db.func.sum(
                Outline.zbViewer).desc()).all()[0:3]
        index_types['type'] = []
        for type_info in info_by_types:
            info = {}
            info['zbType'] = type_info[0]
            info['percent'] = float(
                '{:0.2f}'.format(int(type_info[1]) / total_viewer * 100))
            index_types['type'].append(info)
        sections.append(index_types)
    return sections
