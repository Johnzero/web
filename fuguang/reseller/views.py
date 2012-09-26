# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-23.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 
from flask.ext.login import login_required, fresh_login_required, current_user

from fuguang.extensions import db
from .models import Reseller, ResellerCategory
from .forms import ResellerForm
import webhelpers.paginate as paginate

resellers = Blueprint('resellers', __name__, url_prefix='/resellers')


@resellers.route("/")
@resellers.route("/page-<int:page>")
def list(page=None):
    page = page or 1
    categories = ResellerCategory.query.all()
    
    pagination = paginate.Page(Reseller.query.order_by(Reseller.id.desc()),
                               page=page,
                               items_per_page=current_app.config['RESELLER_PER_PAGE'],
                               url=url_for, endpoint='resellers.list')
    
    return render_template('reseller/list.html', categories=categories, pagination=pagination)

@resellers.route("/category-<int:id>-<int:page>.asp")
def category(id, page):
    category = ResellerCategory.query.get_or_404(id)
    categories = ResellerCategory.query.all()
    
    pagination = paginate.Page(Reseller.query.filter(Reseller.category_id == id).order_by(Reseller.id.desc()),
                               page=page,
                               items_per_page=current_app.config['RESELLER_PER_PAGE'],
                               url=url_for, endpoint='resellers.category', id=id)
    return render_template('reseller/list.html', categories=categories, pagination=pagination, category=category)


@resellers.route("/view-<int:id>.asp")
def view(id):
    reseller = Reseller.query.get_or_404(id)
    categories = ResellerCategory.query.all()
    
    return render_template('reseller/view.html', categories=categories, reseller=reseller)

@resellers.route("/create.asp", methods=["GET", "POST"])
def create():
    form = ResellerForm(request.form)
    if form.validate_on_submit():
        reseller = Reseller()
        form.populate_obj(reseller)
        
        db.session.add(reseller)
        db.session.commit()
        flash('已经添加成功。','info')
        return redirect(url_for('resellers.list'))
    
    return render_template("reseller/edit.html", form=form, mode='create')

@resellers.route("/edit-<int:id>.asp", methods=["GET", "POST"])
def edit(id):
    reseller = Reseller.query.get_or_404(id)
    form = ResellerForm(request.form, reseller)
    
    if form.validate_on_submit():
        form.populate_obj(reseller)

        db.session.commit()
        flash('已经修改成功。','info')
        return redirect(url_for('resellers.list'))
    
    return render_template("reseller/edit.html", form=form, reseller=reseller, mode='edit')

@resellers.route("/delete-<int:id>.asp", methods=["GET"])
def delete(id):
    reseller = Reseller.query.get_or_404(id)
    flash('已经删除经销商 %s。' % reseller.name , 'info')
    db.session.delete(reseller)
    db.session.commit()
    return redirect(url_for('resellers.list'))