# encoding: utf-8
"""
extensions.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask.ext.mail import Mail
from flaskext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.cache import Cache

__all__ = ['oid', 'mail', 'db']

oid = OpenID()
mail = Mail()
db = SQLAlchemy()
cache = Cache()