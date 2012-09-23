# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-23.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 
from flask.ext.login import login_required, fresh_login_required, current_user
from .models import Reseller, ResellerCategory

resellers = Blueprint('resellers', __name__, url_prefix='/resellers')