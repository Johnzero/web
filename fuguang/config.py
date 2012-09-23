# encoding: utf-8
"""
config.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

import os

def get_upload_folder():
    path = os.path.join(os.path.dirname(__file__), 'static', 'upload')
    if not os.path.exists(path):
        os.mkdir(path)
        os.mkdir(os.path.join(path, 'product'))
        os.mkdir(os.path.join(path, 'editor'))
        os.mkdir(os.path.join(path, 'news'))
    return path


class DefaultConfig(object):
    """
    Default configuration for a newsmeme application.
    """

    DEBUG = True
    
    SECRET_KEY = "zuSAyu3XRqGRvAg0HxsKX12Nrvf6Hk3AgZCWg1S1j9Y="

    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://fuguang:fuguang@127.0.0.1/fuguang_web?charset=utf8"

    SQLALCHEMY_ECHO = False

    MAIL_DEBUG = DEBUG

    ADMINS = ()

    DEFAULT_MAIL_SENDER = "fg@fuguang.com"

    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'


    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    
    UPLOAD_FOLDER = get_upload_folder()
    EDITOR_UPLOAD_FOLDER = os.path.join(get_upload_folder(), 'editor')
    PRODUCT_UPLOAD_FOLDER = os.path.join(get_upload_folder(), 'product')
    NEWS_UPLOAD_FOLDER = os.path.join(get_upload_folder(), 'news')
    
    NEWS_PER_PAGE = 5
    
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    

class TestConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///fuguang_web.db"
    
    SECRET_KEY = "secret"