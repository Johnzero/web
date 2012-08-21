#!/usr/bin/env python
# encoding: utf-8
"""
fg_app.py

Created by Daniel Yang on 2012-08-08.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""
#Sqlalchemy, Admin, Cache, Login, WTF, WTForms, Mail, 

import sys, os, datetime, uuid, simplejson as json
from flask import Flask, session, request, render_template, redirect, url_for, flash, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.sqlamodel import ModelView

from PIL import Image

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fuguang:fuguang@localhost:5432/fuguang'

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'upload')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['SECRET_KEY'] = 'zuSAyu3XRqGRvAg0HxsKX12Nrvf6Hk3AgZCWg1S1j9Y='

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

db = SQLAlchemy(app)

admin = Admin(app, name='FG Admin')
path = os.path.join(os.path.dirname(__file__), 'static', 'upload')
admin.add_view(FileAdmin(path, '/static/upload/', name='Files'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    news_list = db.relationship('News', backref='category', lazy='dynamic')

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text())


product2tag = db.Table('product_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    model = db.Column(db.String(50))
    description = db.Column(db.Text())
    
    
    tags = db.relationship('Tag', secondary=product2tag,
        backref=db.backref('products', lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(News, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Tag, db.session))

#helper
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
	return render_template('index.html')


#------------------------------------------------------------------------------------------------

def create_db():
    return db.create_all()

def run():
    app.run(debug=True)
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'run':
            run()
        elif sys.argv[1] == 'create_db':
            create_db()
            
            
    
    