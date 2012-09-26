# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-23.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from fuguang.extensions import db
from datetime import datetime
from fuguang.users.models import User

class ResellerCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50))
    reseller_list = db.relationship('Reseller', backref='category', lazy='dynamic')

    def __unicode__(self):
        return self.name

class Reseller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50))
    category_id = db.Column(db.Integer, db.ForeignKey('reseller_category.id'))
    address = db.Column(db.Unicode(200))
    geo = db.Column(db.Unicode(50))
    telephone = db.Column(db.Unicode(50))
    excerpt = db.Column(db.Text())
    description = db.Column(db.Text())
    recomm = db.Column(db.Boolean(), default=False)
    website = db.Column(db.Unicode(200))
    certified = db.Column(db.Boolean(), default=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, primaryjoin= user_id == User.id, backref='reseller')
    
    
    def __unicode__(self):
        return self.name