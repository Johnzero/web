# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-26.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 

from fuguang.helpers import cached, keep_login_url, jsonify

service = Blueprint('service', __name__, url_prefix='/service')

@service.route("/")
def index():
    return render_template('service/index.html')
