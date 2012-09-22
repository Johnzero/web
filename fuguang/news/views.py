# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-21.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 
from flask.ext.mail import Message
from flask.ext.login import login_required, fresh_login_required, current_user

from fuguang.helpers import cached, keep_login_url
from fuguang.extensions import db

from .models import Category, News
from .forms import CategoryForm, NewsForm

news = Blueprint('news', __name__, url_prefix='/news')

@news.route("/")
def list():
    categories = Category.query.all()
    news_list = News.query.all()
    return render_template('news/list.html', categories=categories, news_list=news_list)


@news.route("/view/<int:id>")
def view(id):
    pass


@news.route("/category/create", methods=["GET", "POST"])
def category_create():
    form = CategoryForm(request.form)
    
    if form.validate_on_submit():
        category = Category()
        form.populate_obj(category)
        db.session.add(category)
        db.session.commit()
        flash('已经添加成功。','info')
        return redirect(url_for('news.list'))
    
    return render_template("news/category_create.html", form=form)

@news.route("/category/edit/<int:id>", methods=["GET", "POST"])
def category_edit(id):
    
    category = Category.query.get_or_404(id)
    form = CategoryForm(request.form, category)
    
    if form.validate_on_submit():
        category = Category()
        form.populate_obj(category)
        db.session.commit()
        flash('已经修改成功。','info')
        return redirect(url_for('news.list'))
    
    return render_template("news/category_edit.html", form=form, category=category)