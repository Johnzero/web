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

admin = Admin(app, name='PaoPao')
path = os.path.join(os.path.dirname(__file__), 'static', 'upload')
admin.add_view(FileAdmin(path, '/static/upload/', name='Files'))

class NewsCate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('News', backref='cate', lazy='dynamic')


class News(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	thumbnail = db.Column(db.String(80))
	content = db.Column(db.Text())
	newcate_id = db.Column(db.Integer, db.ForeignKey('newcate.id'))
    
	created = db.Column(db.DateTime, default=datetime.datetime.now)
	updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)


#helper
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
	return render_template('index.html')
    
    
if __name__ == '__main__':
	app.run(debug=True)