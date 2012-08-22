#!/usr/bin/env python
# encoding: utf-8
"""
fg_app.py

Created by Daniel Yang on 2012-08-08.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""
#Sqlalchemy, Admin, Cache, Login, WTF, WTForms, Mail, 

import sys, os, datetime, uuid, simplejson as json
from datetime import date

from flask import Flask, session, request, render_template, redirect, url_for, flash, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.sqlamodel import ModelView

from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

from PIL import Image

try:
    from json import dumps
except ImportError:
    from simplejson import dumps

#------------------------------------------------------------------------------------------------------------
def jsonify(f):
    """返回json"""
    def inner(*args, **kwargs):
        return Response(dumps(f(*args, **kwargs)), mimetype='application/json')
    return inner


#------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fuguang:fuguang@localhost:5432/fuguang'

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'upload')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['SECRET_KEY'] = 'zuSAyu3XRqGRvAg0HxsKX12Nrvf6Hk3AgZCWg1S1j9Y='


#upload file extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#thumb
thumb_size = 250, 200

#admin = Admin(app, name='FG Admin')
#path = os.path.join(os.path.dirname(__file__), 'static', 'upload')
#admin.add_view(FileAdmin(path, '/static/upload/', name='Files'))

#helper
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#------------------------------------------------------------------------------------------------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    roles = db.Column(db.String(100))
    active = db.Column(db.Boolean())
    
    def __init__(self, name, password, roles='', active=True):
        self.name = name
        self.password = password
        self.roles = roles
        self.active = active

    def is_active(self):
        return self.active

class Anonymous(AnonymousUser):
    name = u"Anonymous"

# set up flask login
login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    print userid,'userid'
    return User.query.get(userid)

#------------------------------------------------------------------------------------------------------------

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

# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Category, db.session))
# admin.add_view(ModelView(News, db.session))
# admin.add_view(ModelView(Product, db.session))
# admin.add_view(ModelView(Tag, db.session))

#------------------------------------------------------------------------------------------------------------

@app.route('/')
def index():
	return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        
        user_in_db = User.query.filter_by(name=username, password=password).first()
        
        if user_in_db:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(user_in_db, remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username or password.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

#------------------------------------------------------------------------------------------------------------
@app.context_processor
def get_urlmap():
    for url in app.url_map:
        print url
    return dict(urlmap=[])


#------------------------------------------------------------------------------------------------------------
def create_db():
    return db.create_all()

def run():
    app.config.from_object(__name__)
    app.run(debug=True)
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'run':
            run()
        elif sys.argv[1] == 'create_db':
            create_db()