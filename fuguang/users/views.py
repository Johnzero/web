# encoding: utf-8
"""
users/views.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, \
    flash, request, current_app, render_template, send_from_directory, views, session

from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
     identity_changed
from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user

from fuguang.extensions import login as login_manager

from .models import User
from .forms import LoginForm

users = Blueprint('users', __name__, url_prefix='/user')


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@users.route("/login/", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user, success = User.query.authenticate(form.username.data, form.password.data)
        if success:
            login_user(user, remember=form.remember.data)

            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            return redirect(request.args.get('next') or '/')
        else:
            flash("Sorry, invalid login", "error")
            
    return render_template('users/login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
        
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    
    return redirect(request.args.get('next') or '/')