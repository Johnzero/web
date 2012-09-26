# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-23.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""
import os, uuid, Image
from datetime import date

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 
from flask.ext.login import login_required, fresh_login_required, current_user

from fuguang.helpers import cached, keep_login_url, allowed_file
from .models import Product, Tag
from .forms import ProductForm
import webhelpers.paginate as paginate
from fuguang.extensions import db

products = Blueprint('products', __name__, url_prefix='/products')

@products.route("/")
@products.route("/page-<int:page>.asp")
def list(page=None):
    page = page or 1
    pagination = paginate.Page(Product.query.order_by(Product.id.desc()),
                               page=page,
                               items_per_page=current_app.config['PRODUCT_PER_PAGE'],
                               url=url_for, endpoint='products.list')
    
    return render_template('product/list.html', tag_object=Tag, pagination=pagination)


@products.route("/view-<int:id>.asp")
def view(id):
    product = Product.query.get_or_404(id)
    return render_template('product/view.html', product=product)


def save_file(file):
    folder_name = date.today().strftime('%Y-%m-%d')
    dir = os.path.join(current_app.config['PRODUCT_UPLOAD_FOLDER'], folder_name)
    thumb_dir = os.path.join(current_app.config['PRODUCT_UPLOAD_FOLDER'], folder_name, 'thumb')
    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    
    extension = os.path.splitext(file.filename)[1]
    filename = str(uuid.uuid4()) + extension
    file.save(os.path.join(dir, filename))
    #thumb
    im = Image.open(os.path.join(dir, filename))
    
    width,height = im.size
    left, top = width/2-140, height/2-74
    area = (left, top, left+280, top+148)
    crop = im.crop(area)
    crop.save(os.path.join(thumb_dir, 'small-'+filename), "JPEG")
    
    #for front page.
    left, top = width/2-290, height/2-215
    area = (left, top, left+580, top+430)
    crop = im.crop(area)
    crop.save(os.path.join(thumb_dir, 'midium-'+filename), "JPEG")
    
    return '/'.join([folder_name, filename])


@products.route("/create.asp", methods=["GET", "POST"])
def create():
    form = ProductForm(request.form)
        
    if form.validate_on_submit():
        product = Product()
        form.populate_obj(product)
        file = request.files['upload']
        if file and allowed_file(file.filename):
            product.cover = save_file(file)
        
        id = db.session.add(product)
        db.session.commit()
        flash('添加产品成功','info')
        return redirect(url_for('products.view', id=id))
    else:
        flash(','.join([error for error in form.errors ]), 'error')
    return render_template('product/create.html', form=form)

@products.route("/edit-<int:id>.asp", methods=["GET", "POST"])
def edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(request.form, product)
    
    if form.validate_on_submit():
        form.populate_obj(product)
        file = request.files['upload']
        if file and allowed_file(file.filename):
            product.cover = save_file(file)
        
        db.session.commit()
        flash('修改产品成功','info')
        return redirect(url_for('products.view', id= product.id))
    else:
        flash(','.join([error for error in form.errors ]), 'error')
    
    return render_template('product/edit.html', product=product, form=form)