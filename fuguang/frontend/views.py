# encoding: utf-8
"""
views/frontend.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 
from flask.ext.login import login_required, fresh_login_required, current_user

from fuguang.helpers import cached, keep_login_url, jsonify
from fuguang.news.models import Category, News
from fuguang.product.models import Product
frontend = Blueprint('frontend', __name__, url_prefix='/')

@frontend.route("/")
def index():
    dialogs = Category.query.filter_by(name=u'对话设计师').first().news_list
    products = Product.query.order_by(Product.id.desc()).limit(3)
    slides = News.query.join(Category).filter(Category.name=='头条').order_by(News.created.desc()).limit(3)
    return render_template('index.html', dialog=(dialogs.count()>0 and dialogs[0] or None), products=products,
                           slides=slides)
