# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-24.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""


from flask.ext.wtf import Form, TextField, TextAreaField, Required, BooleanField, IntegerField, SelectField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from fuguang.users.models import User
from .models import Product, Tag

def get_meterials():
    return Tag.query.filter_by(type='meterial')

def get_applicables():
    return Tag.query.filter_by(type='applicable')

def get_colors():
    return Tag.query.filter_by(type='color')

def get_scenarios():
    return Tag.query.filter_by(type='scenario')

class ProductForm(Form):
    name = TextField('名称', validators=[Required()])
    code = TextField('货号')
    brand = SelectField('品牌', choices=[('富光', '富光'), ('FGA', 'FGA'), ('拾喜', '拾喜'), ('茶马士', '茶马士')],
                        coerce=str)
    excerpt = TextField('简短介绍', validators=[Required()])
    description = TextAreaField('描述')
    capacity = IntegerField('容量(ML)')
    price =  IntegerField('参考价格')
    meterials = QuerySelectMultipleField('材质', validators=[Required()], query_factory=get_meterials)
    applicables = QuerySelectMultipleField('适用人群', validators=[Required()], query_factory=get_applicables)
    colors = QuerySelectMultipleField('颜色', validators=[Required()], query_factory=get_colors)
    scenarios = QuerySelectMultipleField('场景', validators=[Required()], query_factory=get_scenarios)
    upload  = FileField('产品主图')