# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-21.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""
import os, uuid, Image
from datetime import date
import webhelpers.paginate as paginate


from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 
from flask.ext.mail import Message
from flask.ext.login import login_required, fresh_login_required, current_user

from fuguang.helpers import cached, keep_login_url, allowed_file
from fuguang.extensions import db

from .models import Category, News
from .forms import NewsForm

news = Blueprint('news', __name__, url_prefix='/news')

@news.route("/")
@news.route("/page/<int:page>")
def list(page=None):
    page = page or 1

    categories = Category.query.all()
    pagination = paginate.Page(News.query.order_by(News.created.desc()),
                               page=page,
                               items_per_page=current_app.config['NEWS_PER_PAGE'],
                               url=url_for, endpoint='news.list')
    return render_template('news/list.html', categories=categories, pagination=pagination)

@news.route("/category/<int:id>/page/<int:page>", defaults={'page':1})
def category(id, page):
    category = Category.query.get_or_404(id)
    categories = Category.query.all()
    
    pagination = paginate.Page(News.query.filter(News.category_id == id).order_by(News.created.desc()),
                               page=page,
                               items_per_page=current_app.config['NEWS_PER_PAGE'],
                               url=url_for, endpoint='news.category', id=id)
    
    return render_template('news/list.html', categories=categories, pagination=pagination, category=category)

@news.route("/view/<int:id>")
def view(id):
    news = News.query.get_or_404(id)
    categories = Category.query.all()
    return render_template('news/view.html', categories=categories, news=news)


def save_file(file):
    folder_name = date.today().strftime('%Y-%m-%d')
    dir = os.path.join(current_app.config['NEWS_UPLOAD_FOLDER'], folder_name)
    thumb_dir = os.path.join(current_app.config['NEWS_UPLOAD_FOLDER'], folder_name, 'thumb')
    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    
    extension = os.path.splitext(file.filename)[1]
    filename = str(uuid.uuid4()) + extension
    file.save(os.path.join(dir, filename))
    #thumb
    small_thumb_size = 50, 50
    im = Image.open(os.path.join(dir, filename))
    
    width,height = im.size
    left, top = width/2-25, height/2-25
    area = (left, top, left+50, top+50)
    crop = im.crop(area)
    crop.save(os.path.join(thumb_dir, 'small-'+filename), "JPEG")
    
    #for front page.
    left, top = width/2-130, height/2-79
    area = (left, top, left+260, top+158)
    crop = im.crop(area)
    crop.save(os.path.join(thumb_dir, 'midium-'+filename), "JPEG")
    
    return '/'.join([folder_name, filename])

@news.route("/create", methods=["GET", "POST"])
def news_create():
    form = NewsForm(request.form)

    if form.validate_on_submit():
        news = News()
        form.populate_obj(news)
        news.user =current_user
        
        file = request.files['upload']
        if file and allowed_file(file.filename):
            news.cover = save_file(file)
        
        db.session.add(news)
        db.session.commit()
        flash('已经添加成功。','info')
        return redirect(url_for('news.list'))
    
    return render_template("news/news_create.html", form=form)

@news.route("/edit/<int:id>", methods=["GET", "POST"])
def news_edit(id):
    news = News.query.get_or_404(id)
    form = NewsForm(request.form, news)
    
    if form.validate_on_submit():
        form.populate_obj(news)
        
        file = request.files['upload']
        if file and allowed_file(file.filename):
            news.cover = save_file(file)
        
        db.session.commit()
        flash('已经修改成功。','info')
        return redirect(url_for('news.list'))
    
    return render_template("news/news_edit.html", form=form, news=news)


@news.route("/delete/<int:id>")
def news_delete(id):
    news = News.query.get_or_404(id)
    flash('已经删除新闻 %s。' % news.title , 'info')
    db.session.delete(news)
    db.session.commit()
    return redirect(url_for('news.list'))


