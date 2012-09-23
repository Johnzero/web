# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-23.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from fuguang.extensions import db
from datetime import datetime


class ResellerCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    reseller_list = db.relationship('Reseller', backref='category', lazy='dynamic')

    
    def __unicode__(self):
        return self.name

class Reseller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('reseller_category.id'))
    province = db.Column(db.String(50))
    address = db.Column(db.String(200))
    geo = db.Column(db.String(50))
    telephone = db.Column(db.String(50))
    description = db.Column(db.Text())
    recomm = db.Column(db.Boolean(), default=False)
    
    def __unicode__(self):
        return self.name