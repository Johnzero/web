# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-22.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""


from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form

from .models import Category, News

CategoryForm = model_form(Category, Form, field_args={
    'name':{'label':'名称'}
    })
NewsForm = model_form(News, Form)