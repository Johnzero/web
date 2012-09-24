#!/usr/bin/python
import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from fuguang import create_app
application = create_app()