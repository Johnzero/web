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
from flask.ext.login import LoginManager, AnonymousUser

__all__ = ['oid', 'mail', 'db', 'login']

class Anonymous(AnonymousUser):
    name = u"Anonymous"


oid = OpenID()
mail = Mail()
db = SQLAlchemy()
cache = Cache()
login = LoginManager()

login.anonymous_user = Anonymous
login.login_view = "users.login"
login.login_message = u"请登录后再使用本功能."
login.refresh_view = "users.reauth"