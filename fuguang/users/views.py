# encoding: utf-8
"""
users/views.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, \
    flash, request, current_app, render_template, send_from_directory, views, session

from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user, confirm_login

from fuguang.extensions import login as login_manager, db

from .models import User
from .forms import LoginForm, UserForm

users = Blueprint('users', __name__, url_prefix='/user')

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@users.route("/login.asp", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user, success = User.query.authenticate(form.username.data, form.password.data)
        if success:
            flash("欢迎登录。")
            login_user(user, remember=form.remember.data)

            return redirect(request.args.get('next') or '/')
        else:
            flash("登录名称或者密码错误。请重试", "error")

    return render_template('users/login.html', form=form)

@users.route('/logout.asp')
@login_required
def logout():
    logout_user()
    return redirect(request.args.get('next') or '/')

@users.route('/reauth', methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or '/')
    return render_template("users/reauth.html")

@users.route('/list.asp')
@login_required
def list():
    users = User.query.order_by(User.id.desc()).all()
    
    return render_template("users/list.html", users=users)


@users.route('/create.asp', methods=["GET", "POST"])
@login_required
def create():
    if not current_user.is_admin:
        flash('没有权限','error')
        return redirect('/')
    
    form = UserForm(request.form)
    
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('已经添加成功','info')
        return redirect(url_for('users.list'))

    return render_template("users/new.html", form=form)

@users.route('/edit-<int:id>.asp', methods=["GET", "POST"])
@login_required
def edit(id):
    if not current_user.is_admin:
        flash('没有权限','error')
        return redirect('/')
    user = User.query.get_or_404(id)
    form = UserForm(request.form, user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        if form.password.data:
            user.password = form.password.data
        db.session.commit()
        flash('已经修改成功','info')
        return redirect(url_for('users.list'))

    return render_template("users/edit.html", form=form, user=user)

@users.route('/delete-<int:id>.asp')
@login_required
def delete(id):
    if not current_user.is_admin:
        flash('没有权限','error')
        return redirect('/')
    user = User.query.get_or_404(id)
    
    flash('已经删除用户 %s。' % user.username , 'info')
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.list'))