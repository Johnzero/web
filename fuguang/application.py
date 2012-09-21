# encoding: utf-8
"""
application.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""


import os
import logging

from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask, Response, request, g, jsonify, redirect, url_for, flash, render_template


from fuguang.extensions import db, mail, oid, cache, login
from fuguang.config import DefaultConfig
from fuguang import helpers

from fuguang.users import bp_users
from fuguang.frontend import bp_frontend
from fuguang.pages import bp_page

from fuguang.users.models import User


__all__ = ["create_app"]

DEFAULT_APP_NAME = 'fuguang'

DEFAULT_MODULES = (
    (bp_users, bp_frontend, bp_page)
)

def create_app(config=None, app_name=None, modules=None):
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(app_name)
    configure_app(app, config)
    configure_logging(app)
    configure_errorhandlers(app)
    configure_extensions(app)

    configure_template_filters(app)

    configure_modules(app, modules)
    
    return app


def configure_app(app, config):
    
    app.config.from_object(DefaultConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('APP_CONFIG', silent=True)
    
def configure_modules(app, modules):
    for module in modules:
        app.register_blueprint(module)

def configure_template_filters(app):
    @app.template_filter()
    def timesince(value):
        return helpers.timesince(value)


def configure_extensions(app):

    mail.init_app(app)
    db.init_app(app)
    oid.init_app(app)
    cache.init_app(app)
    login.setup_app(app)


def configure_errorhandlers(app):

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/404.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed'))
        return render_template("errors/403.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return render_template("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonfiy(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("account.login", next=request.path))


def configure_logging(app):
    if app.debug or app.testing:
        return

    mail_handler = \
        SMTPHandler(app.config['MAIL_SERVER'],
                    'error@newsmeme.com',
                    app.config['ADMINS'], 
                    'application error',
                    (
                        app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'],
                    ))

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path, 
                             app.config['DEBUG_LOG'])

    debug_file_handler = \
        RotatingFileHandler(debug_log,
                            maxBytes=100000,
                            backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path, 
                             app.config['ERROR_LOG'])

    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)



