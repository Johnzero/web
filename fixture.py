#!/usr/bin/env python
# encoding: utf-8
"""
fixture.py

Created by Daniel Yang on 2012-08-25.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

def process(command, db, Category, ResellerCategory, User, Page):
    if command == 'syncdb':
        sync_db(db)
    elif command == 'dropdb':
        drop_db(db)
    elif command == 'initdb':
        init_db(db, Category, ResellerCategory, User, Page)
    elif command == 'resetdb':
        reset_db(db, Category, ResellerCategory, User, Page)
    else:
        print 'unkown command. support sycndb, initdb, dropdb.'

def sync_db(db):
    db.create_all()

def drop_db(db):
    db.drop_all()

def init_db(db, Category, ResellerCategory, User, Page):
    db.session.add(User('admin','admin', 'admin', True))
    db.session.add(Category('新闻动态'))
    db.session.add(Category('公告'))
    db.session.add(Category('首页大图'))
    db.session.add(Category('对话设计师'))
    db.session.add(ResellerCategory('直营店'))
    db.session.add(ResellerCategory('批发'))
    db.session.add(ResellerCategory('FGA'))
    db.session.add(ResellerCategory('网络'))
    
    db.session.commit()
    #user_id, code, title, type, keyword, content
    db.session.add(Page(1, 'fuguang', '关于富光', 'about', '富光', 'fuguang'))
    db.session.add(Page(1, 'history', '富光历史', 'about', '富光', 'history'))
    db.session.add(Page(1, 'philosophy', '理念', 'about', '富光','philosophy'))
    db.session.add(Page(1, 'honor', '荣誉资质', 'about', '富光', 'honor'))
    db.session.add(Page(1, 'service', '客户服务', 'service', '富光service', 'service'))
    db.session.add(Page(1, 'fg', '富光', 'brand', '富光', 'brand'))
    db.session.add(Page(1, 'fga', 'FGA', 'brand', '富光,FGA', 'brand'))
    db.session.add(Page(1, 'bestjoy', '拾喜', 'brand', '富光,拾喜', 'brand'))
    db.session.add(Page(1, 'teamaster', '茶马士', 'brand', '茶马士', 'brand'))
    db.session.commit()

def reset_db(db, Category, ResellerCategory, User, Page):
    drop_db(db)
    sync_db(db)
    init_db(db, Category, ResellerCategory, User, Page)