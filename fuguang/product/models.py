# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-23.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from fuguang.extensions import db
from datetime import datetime



product2tag = db.Table('product_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    model = db.Column(db.String(50))
    description = db.Column(db.Text())
    tags = db.relationship('Tag', secondary=product2tag,
        backref=db.backref('products', lazy='dynamic'))
    
    
    
    def __unicode__(self):
        return self.name

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    def __unicode__(self):
        return self.name
