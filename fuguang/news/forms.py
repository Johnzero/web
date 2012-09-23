# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-22.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""


from flask.ext.wtf import Form, TextField, TextAreaField, Required, FileField, FieldList
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Category, News

def get_categories():
    return Category.query.all()

class NewsForm(Form):
    title = TextField('标题', validators=[Required()])
    excerpt = TextAreaField('摘要')
    content = TextAreaField('内容')
    category = QuerySelectField('分类', query_factory=get_categories)
    upload  = FileField('新闻主图')