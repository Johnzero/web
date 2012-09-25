# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-23.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 
from flask.ext.login import login_required, fresh_login_required, current_user
from .models import Product, Tag
import webhelpers.paginate as paginate

products = Blueprint('products', __name__, url_prefix='/products')

@products.route("/")
@products.route("/page/<int:page>")
def list(page=None):
    page = page or 1
    
    pagination = paginate.Page(Product.query.order_by(Product.id.desc()),
                               page=page,
                               items_per_page=current_app.config['PRODUCT_PER_PAGE'],
                               url=url_for, endpoint='products.list')
    
    return render_template('product/list.html', tag_object=Tag, pagination=pagination)