#!/usr/bin/python
# encoding: utf-8

import sys,os
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from fuguang import create_app
application = create_app()