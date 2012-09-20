# encoding: utf-8
"""
views/frontend.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, \
    flash, request, current_app, render_template, send_from_directory, views


users = Blueprint('users', __name__, url_prefix='/user')