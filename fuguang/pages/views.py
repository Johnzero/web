# encoding: utf-8
"""
views/frontend.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, \
    flash, request, current_app, render_template, send_from_directory, views

from flask.ext.login import login_required, fresh_login_required, current_user
from fuguang.helpers import cached, keep_login_url
from fuguang.extensions import db

from .models import Page
from .forms import PageForm

page = Blueprint('page', __name__, url_prefix='/page')

class PageView(views.View):
    def __init__(self, template_name, type):
        self.template_name = template_name
        self.type = type

    def dispatch_request(self, code=None):
        if code:
            item = Page.query.filter_by(code=code, type=self.type).first_or_404()
        else:
            item = Page.query.filter_by(type=self.type).first_or_404()
        
        #add some news and products.
        #news_list = News.query.filter(Category.name=='新闻动态').order_by('created desc').limit(10)
        
        return render_template(self.template_name, page=item, object=Page)

page.add_url_rule('/about/<string:code>', view_func=PageView.as_view('about', template_name='page/about.html', type='about'))
page.add_url_rule('/brand/<string:code>', view_func=PageView.as_view('brand', template_name='page/brand.html', type='brand'))
page.add_url_rule('/service', view_func=PageView.as_view('service', template_name='service.html', type='service'))


@page.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    page = Page.query.get_or_404(id)
    form = PageForm(request.form, page)

    if form.validate_on_submit():
        form.populate_obj(page)
        flash('修改成功。','info')
        db.session.commit()
        return redirect(url_for(('page.%s' % page.type), code=page.code))
    
    return render_template("page/edit.html", form=form, page=page)
