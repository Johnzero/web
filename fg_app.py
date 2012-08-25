#!/usr/bin/env python
# encoding: utf-8
"""
fg_app.py

Created by Daniel Yang on 2012-08-08.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""
#Sqlalchemy, Admin, Cache, Login, WTF, WTForms, Mail

import sys, os, uuid, simplejson as json
from datetime import date, datetime

from flask import Flask, session, request, render_template, redirect, url_for, flash, send_from_directory, views
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, Required, SelectField

from PIL import Image

try:
    from json import dumps
except ImportError:
    from simplejson import dumps

#------------------------------------------------------------------------------------------------------------
#配置定义
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fuguang:fuguang@localhost:5432/fuguang'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'upload')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['SECRET_KEY'] = 'zuSAyu3XRqGRvAg0HxsKX12Nrvf6Hk3AgZCWg1S1j9Y='

#upload file extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#thumb
thumb_size = 250, 200

#------------------------------------------------------------------------------------------------------------
#用户认证
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    roles = db.Column(db.String(100))
    active = db.Column(db.Boolean())
    
    def __init__(self, name, password, roles='', active=True):
        self.name = name
        self.password = password
        self.roles = roles
        self.active = active

    def is_active(self):
        return self.active

class Anonymous(AnonymousUser):
    name = u"Anonymous"

# set up flask login
login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    print userid,'userid'
    return User.query.get(userid)

#------------------------------------------------------------------------------------------------------------
#工具

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def path2url(path):
    return '/%s/' % ('/'.join(path.split('\\')))

def jsonify(f):
    """返回json"""
    def inner(*args, **kwargs):
        return Response(dumps(f(*args, **kwargs)), mimetype='application/json')
    return inner

@app.context_processor
def active_processor():
    def page_active(code_list, path):
        base_name = os.path.basename(path)
        return base_name in code_list
    return dict(page_active=page_active)
#------------------------------------------------------------------------------------------------------------
#模型

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(50))
    type = db.Column(db.String(50))
    keyword = db.Column(db.Text())
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=datetime.now)
    updated = db.Column(db.DateTime(), onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, user_id, code, title, type, keyword, content):
        self.code = code
        self.user_id = user_id
        self.content = content
        self.title = title
        self.keyword = keyword
        self.type = type

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    news_list = db.relationship('News', backref='category', order_by='desc(News.created)', lazy='dynamic')
    
    def __init__(self, name):
        self.name = name

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=datetime.now)
    updated = db.Column(db.DateTime(), onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

product2tag = db.Table('product_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    model = db.Column(db.String(50))
    description = db.Column(db.Text())
    tags = db.relationship('Tag', secondary=product2tag,
        backref=db.backref('products', lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class ResellerCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    reseller_list = db.relationship('Reseller', backref='category', lazy='dynamic')
    
    def __init__(self, name):
        self.name = name

class Reseller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('reseller_category.id'))
    province = db.Column(db.String(50))
    address = db.Column(db.String(200))
    geo = db.Column(db.String(50))
    telephone = db.Column(db.String(50))
    description = db.Column(db.Text())

#------------------------------------------------------------------------------------------------------------
#Views
class PageView(views.View):
    def __init__(self, template_name, type):
        self.template_name = template_name
        self.type = type

    def dispatch_request(self, code=None):
        if code:
            item = Page.query.filter_by(code=code, type=self.type).first_or_404()
        else:
            item = Page.query.filter_by(type=self.type).first_or_404()
        return render_template(self.template_name, page=item)

app.add_url_rule('/about/<string:code>', view_func=PageView.as_view('about', template_name='about.html', type='about'))
app.add_url_rule('/brand/<string:code>', view_func=PageView.as_view('brand', template_name='brand.html', type='brand'))
app.add_url_rule('/service', view_func=PageView.as_view('service', template_name='service.html', type='service'))

#------------------------------------------------------------------------------------------------------------
#表单 
class PageForm(Form):
    code = TextField('简写', validators=[Required()])
    title = TextField('标题', validators=[Required()])
    type = SelectField('类型', choices=[('aim', 'AIM'), ('msn', 'MSN')], validators=[Required()])
    keyword = TextAreaField('关键字')
    content = TextAreaField('内容')
    submit = SubmitField('保存')

#------------------------------------------------------------------------------------------------------------
#首页
@app.route('/')
def index():
    return render_template('index.html')

#------------------------------------------------------------------------------------------------------------
#页面
@app.route('/page/edit/<int:page_id>', methods=['GET','POST'])
def page_save(page_id):
    item = Page.query.filter_by(id=page_id).first_or_404()
    
    form = PageForm(request.form, obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('成功')
    
    return render_template('edit.html', item=item, form=form)
    
#------------------------------------------------------------------------------------------------------------
#新闻动态-分页
@app.route('/news', defaults={'page': 1})
@app.route('/news/p/<int:page>')
def news(page):
    pass

#查看新闻
@app.route('/news/view/<int:news_id>')
def news_view(news_id):
    pass

#------------------------------------------------------------------------------------------------------------
#产品中心
@app.route('/product', defaults={'page': 1})
@app.route('/product/p/<int:page>')
def product(page):
    return render_template('products.html')

@app.route('/product/view/<int:product_id>')
def product_view(product_id):
    pass

@app.route('/product/tag', defaults={'page': 1})
@app.route('/product/tag/<int:tag_id>/<int:page>')
def product_tag(tag_id, page):
    pass

#------------------------------------------------------------------------------------------------------------
#销售渠道
@app.route('/sales', defaults={'page': 1, 'category_id': 1})
@app.route('/sales/<int:category_id>/<int:page>')
def sales(category_id, page):
    return render_template('service.html')

#------------------------------------------------------------------------------------------------------------
# 用户

@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        user_in_db = User.query.filter_by(name=username, password=password).first()
        
        if user_in_db:
            remember = request.form.get('remember', 'no') == 'yes'
            if login_user(user_in_db, remember=remember):
                flash('Logged in!')
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash('Sorry, but you could not log in.')
        else:
            flash(u'Invalid username or password.')
    return render_template('login.html')

@app.route('/user/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/user/reauth', methods=['GET', 'POST'])
@login_required
def reauth():
    if request.method == 'POST':
        confirm_login()
        flash(u'Reauthenticated.')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('reauth.html')

#------------------------------------------------------------------------------------------------------------
#文本编辑器-文件上传
@app.route('/rd/upload', methods=['GET', 'POST'])
@jsonify
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            folder_name = date.today().strftime('%Y-%m-%d')
            dir = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
            thumb_dir = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, 'thumb')
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
            
            return {'filelink':'/static/upload/%s/%s' % (folder_name, filename)}
    else:
        file_list = []
        for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
            if dirs:
                url_prefix = path2url(root)
                for f in files:
                    file_list.append({
                        'thumb': url_prefix + 'thumb/' + f,
                        'image': url_prefix + f,
                        'folder': url_prefix,
                    })

        return file_list

#------------------------------------------------------------------------------------------------------------

def run():
    app.config.from_object(__name__)
    app.run(debug=True)
    
if __name__ == '__main__':
    import fixture
    if len(sys.argv) == 2:
        fixture.process(sys.argv[1], db, Category, ResellerCategory, User, Page)
    else:
        if sys.getdefaultencoding() != 'utf-8':
        	reload(sys)
        	sys.setdefaultencoding('utf-8')
        run()