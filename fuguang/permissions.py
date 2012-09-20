# encoding: utf-8
"""
permissions.py

Created by Daniel Yang on 2012-09-20.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from flask_principal import Permission, RoleNeed

admin = Permission(RoleNeed('admin'))
editor = Permission(RoleNeed('editor'))
dealer = Permission(RoleNeed('dealer'))
auth = Permission(RoleNeed('authenticated'))

# this is assigned when you want to block a permission to all
# never assign this role to anyone !
null = Permission(RoleNeed('null'))