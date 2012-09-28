# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-23.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from fuguang.extensions import db
from datetime import datetime
from fuguang.reseller.models import Reseller

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
    name = db.Column(db.Unicode(150))
    model = db.Column(db.Unicode(50))
    excerpt = db.Column(db.Unicode(300))
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
    
    links = db.relationship('ResellerLink', backref='product', lazy='dynamic')
    
    cover = db.Column(db.Unicode(150))
    
    def __unicode__(self):
        return self.name

    def get_thumb(self):
        if self.cover:
            l = self.cover.split('/')
            return '/static/upload/products/%s/thumb/%s' % (l[0], 'small-'+l[1])
        return "http://flickholdr.com/280/148/cup"
    
    def get_midium_thumb(self):
        if self.cover:
            l = self.cover.split('/')
            return '/static/upload/products/%s/thumb/%s' % (l[0], 'midium-'+l[1])
        return 'http://flickholdr.com/580/430/cup'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50))
    type = db.Column(db.Unicode(50))
    def __unicode__(self):
        return self.name


class ResellerLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    reseller_id = db.Column(db.Integer, db.ForeignKey('reseller.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    reseller = db.relationship(Reseller, primaryjoin= reseller_id == Reseller.id, backref='ilnks')
    price = db.Column(db.Integer)
    
    