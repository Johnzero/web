# encoding: utf-8
"""
Created by Daniel Yang on 2012-09-21.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

import os, uuid
from datetime import date
from flask import Blueprint, url_for, redirect, g, flash, request, current_app, \
    render_template, send_from_directory
from PIL import Image
from fuguang.helpers import jsonify,  allowed_file

rd = Blueprint('rd', __name__, url_prefix='/rd')

thumb_size = 250, 200

@rd.route('/upload', methods=['GET', 'POST'])
@jsonify
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            folder_name = date.today().strftime('%Y-%m-%d')
            dir = os.path.join(current_app.config['EDITOR_UPLOAD_FOLDER'], folder_name)
            thumb_dir = os.path.join(current_app.config['EDITOR_UPLOAD_FOLDER'], folder_name, 'thumb')
            if not os.path.exists(dir):
                os.makedirs(dir)
            if not os.path.exists(thumb_dir):
                os.makedirs(thumb_dir)
            
            extension = os.path.splitext(file.filename)[1]
            filename = str(uuid.uuid4()) + extension
            file.save(os.path.join(dir, filename))
            #thumb
            im = Image.open(os.path.join(dir, filename))
            im.thumbnail(thumb_size)
            im.save(os.path.join(thumb_dir, filename), "JPEG")
            
            return {'filelink':'/static/upload/editor/%s/%s' % (folder_name, filename)}
    else:
        file_list = []

        for root, dirs, files in os.walk(current_app.config['EDITOR_UPLOAD_FOLDER']):
            for d in dirs:
                folder = '/static/upload/editor/%s' % os.path.basename(root)
                for f in files:
                    file_list.append({
                        'thumb': os.path.join(folder, 'thumb', f),
                        'image': os.path.join(folder, f),
                        'folder': folder,
                    })
                print root, dirs, files
        return file_list