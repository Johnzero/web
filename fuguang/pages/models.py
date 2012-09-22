# encoding: utf-8
"""
model/page.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from fuguang.extensions import db
from datetime import datetime

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Unicode(50))
    title = db.Column(db.Unicode(150))
    keyword = db.Column(db.Text())
    type = db.Column(db.Unicode(50))
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=datetime.now)
    updated = db.Column(db.DateTime(), onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __unicode__(self):
        return self.title
        
    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)