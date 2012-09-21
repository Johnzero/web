# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-21.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask.ext.wtf import Form, TextField, Required, TextAreaField, SubmitField


class PageForm(Form):
    keyword = TextField('关键字', validators=[Required()])
    content = TextAreaField('页面内容', validators=[Required()])
    submit = SubmitField("保存")