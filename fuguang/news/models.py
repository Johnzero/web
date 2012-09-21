# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-21.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from fuguang.extensions import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    news_list = db.relationship('News', backref='category', order_by='desc(News.created)', lazy='dynamic')
    
    def __unicode__(self):
        return self.name
    
    def __init__(self, name):
        self.name = name

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=datetime.now)
    updated = db.Column(db.DateTime(), onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __unicode__(self):
        return self.title