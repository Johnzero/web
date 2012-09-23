# encoding: utf-8
"""
views/frontend.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 
from flask.ext.login import login_required, fresh_login_required, current_user

from fuguang.helpers import cached, keep_login_url, jsonify
from fuguang.news.models import Category

frontend = Blueprint('frontend', __name__, url_prefix='/')

@frontend.route("/")
def index():
    
    dialog = Category.query.filter_by(name=u'对话设计师').first().news_list[0]

    return render_template('index.html', dialog=dialog)
