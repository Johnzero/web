# encoding: utf-8
"""
model/users.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

import hashlib
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash, cached_property

from flask.ext.sqlalchemy import BaseQuery
from flask.ext.principal import RoleNeed, UserNeed, Permission

from fuguang.extensions import db
from fuguang.permissions import null

class Permissions(object):

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, name):
        return getattr(self.obj, name)


class UserQuery(BaseQuery):
    def from_identity(self, identity):
        """
        Loads user from flaskext.principal.Identity instance and
        assigns permissions from user.

        A "user" instance is monkeypatched to the identity instance.

        If no user found then None is returned.
        """
        try:
            user = self.get(int(identity.name))
        except ValueError:
            user = None

        if user:
            identity.provides.update(user.provides)

        identity.user = user

        return user

    def authenticate(self, login, password):
        
        user = self.filter(db.or_(User.username==login, User.email==login)).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    def authenticate_openid(self, email, openid):

        user = self.filter(User.email==email).first()

        if user:
            authenticated = user.check_openid(openid)
        else:
            authenticated = False

        return user, authenticated


class User(db.Model):
    query_class = UserQuery
    
    # user roles
    MEMBER = 100
    DEALER = 200
    EDITOR = 300
    ADMIN = 400
    
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(60), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.Integer, default=MEMBER)

    _password = db.Column("password", db.String(80))
    _openid = db.Column("openid", db.String(80), unique=True)
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<%s>" % self
    
    @cached_property
    def permissions(self):
        return self.Permissions(self)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym("_password", 
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def _get_openid(self):
        return self._openid

    def _set_openid(self, openid):
        self._openid = generate_password_hash(openid)

    openid = db.synonym("_openid", 
                          descriptor=property(_get_openid,
                                              _set_openid))

    def check_openid(self, openid):
        if self.openid is None:
            return False
        return check_password_hash(self.openid, openid)


    @cached_property
    def gravatar(self):
        if not self.email:
            return ''
        md5 = hashlib.md5()
        md5.update(self.email.strip().lower())
        return md5.hexdigest()

    def gravatar_url(self, size=80):
        if not self.gravatar:
            return ''

        return "http://www.gravatar.com/avatar/%s.jpg?s=%d" % (
            self.gravatar, size)