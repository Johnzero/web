# encoding: utf-8
"""
users/forms.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, HiddenField, SubmitField, SelectField

from .models import User

class LoginForm(Form):
    username = TextField('用户名')
    password = PasswordField('密码')
    remember = BooleanField('记住登录')
    next = HiddenField()
    submit = SubmitField('登录')

class UserForm(Form):
    username = TextField('用户名')
    password = TextField('密码')
    email = TextField('Email')
    role = SelectField('角色', choices=[(User.ADMIN, '管理员'), (User.EDITOR, '编辑'), (User.RESELLER, '经销商')],
                       coerce=int)