# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-23.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from fuguang.extensions import db
from datetime import datetime


product2meterial = db.Table('product_meterial',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
)

product2applicable = db.Table('product_applicable',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
)

product2color = db.Table('product_color',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
)

product2scenario = db.Table('product_product2scenario',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    model = db.Column(db.String(50))
    description = db.Column(db.Text())
    brand = db.Column(db.String(50))
    meterials = db.relationship('Tag', secondary=product2meterial,
        backref=db.backref('m_products', lazy='dynamic'))
    
    applicables = db.relationship('Tag', secondary=product2applicable,
        backref=db.backref('a_products', lazy='dynamic'))
    
    colors = db.relationship('Tag', secondary=product2color,
        backref=db.backref('c_products', lazy='dynamic'))
    
    scenarios = db.relationship('Tag', secondary=product2scenario,
        backref=db.backref('s_products', lazy='dynamic'))
    
    capacity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    
    cover = db.Column(db.String(150))
    
    def __unicode__(self):
        return self.name

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    def __unicode__(self):
        return self.name
