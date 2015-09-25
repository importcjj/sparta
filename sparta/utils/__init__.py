# -*- coding:utf-8 -*-
from .redis_broker import Redis


def client_visit_controller(client_ip):
    """control the client
    """
    Redis.ip_notebook(client_ip)
