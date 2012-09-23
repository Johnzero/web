# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-21.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from fuguang.extensions import db
from datetime import datetime
from fuguang.users.models import User

from flask.ext.sqlalchemy import BaseQuery

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50))
    news_list = db.relationship('News', backref='category', order_by='desc(News.created)', lazy='dynamic')
    
    def __unicode__(self):
        return self.name

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(150))
    excerpt = db.Column(db.Unicode(300))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=datetime.now)
    updated = db.Column(db.DateTime(), onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, primaryjoin=user_id == User.id)
    cover = db.Column(db.Text())
    
    def __unicode__(self):
        return self.title
    
    def get_cover(self):
        if self.cover:
            return '/static/upload/news/' + self.cover
        return 'http://placekitten.com/580/150'
    
    def get_thumb(self):
        if self.cover:
            l = self.cover.split('/')
            return '/static/upload/news/%s/thumb/%s' % (l[0], 'small-'+l[1])
        return 'http://placekitten.com/50/50'
    
    def get_midium_thumb(self):
        if self.cover:
            l = self.cover.split('/')
            return '/static/upload/news/%s/thumb/%s' % (l[0], 'midium-'+l[1])
        return 'http://placekitten.com/260/158'