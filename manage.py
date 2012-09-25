# encoding: utf-8

import sys,os
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


from flask import current_app
from flask.ext.script import Manager, prompt, prompt_pass, \
    prompt_bool, prompt_choices

from flask.ext.mail import Message

from fuguang import create_app
from fuguang.extensions import db, mail
from fuguang.users.models import User

manager = Manager(create_app)


@manager.option('-u', '--username', dest="username", required=False)
@manager.option('-p', '--password', dest="password", required=False)
@manager.option('-e', '--email', dest="email", required=False)
@manager.option('-r', '--role', dest="role", required=False)
def createuser(username=None, password=None, email=None, role=None):
    """
    Create a new user
    """
    
    if username is None:
        while True:
            username = prompt("Username")
            user = User.query.filter(User.username==username).first()
            if user is not None:
                print "Username %s is already taken" % username
            else:
                break

    if email is None:
        while True:
            email = prompt("Email address")
            user = User.query.filter(User.email==email).first()
            if user is not None:
                print "Email %s is already taken" % email
            else:
                break

    if password is None:
        password = prompt_pass("Password")

        while True:
            password_again = prompt_pass("Password again")
            if password != password_again:
                print "Passwords do not match"
            else:
                break
    
    roles = (
        (User.MEMBER, "member"),
        (User.MODERATOR, "moderator"),
        (User.ADMIN, "admin"),
    )

    if role is None:
        role = prompt_choices("Role", roles, resolve=int, default=User.MEMBER)

    user = User(username=username,
                email=email,
                password=password,
                role=role)

    db.session.add(user)
    db.session.commit()

    print "User created with ID", user.id
    
@manager.command
def initdb():
    from fuguang.fixture import init_db
    init_db(db)

@manager.command
def initproduct():
    from fuguang.fixture import init_products
    
    init_products(db)

@manager.command
def createall():
    "Creates database tables"
    
    db.create_all()
    
@manager.command
def dropall():
    "Drops all database tables"
    
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

@manager.command
def mailall():
    "Sends an email to all users"
    
    subject = prompt("Subject")
    message = prompt("Message")
    from_address = prompt("From", default="support@thenewsmeme.com")
    if prompt_bool("Are you sure ? Email will be sent to everyone!"):
        with mail.connect() as conn:
            for user in User.query:
                message = Message(subject=subject,
                                  body=message,
                                  sender=from_address,
                                  recipients=[user.email])

                conn.send(message)

#@manager.shell
#def make_shell_context():
#    return dict(app=current_app, 
#                db=db,
#                User=User,
#                Page=Page)


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")


if __name__ == "__main__":
    manager.run()