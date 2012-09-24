# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-24.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""


from flask.ext.wtf import Form, TextField, TextAreaField, Required, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from fuguang.users.models import User
from .models import Reseller, ResellerCategory

def get_categories():
    return ResellerCategory.query.all()

def get_users():
    return User.query.filter_by(role = User.RESELLER).all()

class ResellerForm(Form):
    name = TextField('经销商名称', validators=[Required()])
    address = TextField('地址', validators=[Required()])
    telephone = TextField('电话')
    geo = TextField('GEO')
    website = TextField('网站')
    excerpt = TextAreaField('摘要')
    description = TextAreaField('内容')
    recomm = BooleanField('是否推荐')
    certified = BooleanField('是否授权过')
    category = QuerySelectField('分类', query_factory=get_categories)
    user = QuerySelectField('关联用户', query_factory=get_users)