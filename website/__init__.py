import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from os import path

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testapp123'
   
    from .views import views

    app.register_blueprint(views,url_prefix='/')
 
#     app.register_blueprint(auth,url_prefix='/auth/')


#     from .models import User, Note
#     create_database(app)

#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login' #if we not login, where we go?
#     login_manager.init_app(app) #tell login_manager which app we are using
#     @login_manager.user_loader
#     def loaf_user(id):
#         return User.query.get(int(id)) #get : look for the primary key

    return app


# def create_database(app):
#     if(not path.exists('website/' + DB_NAME)):
#         db.create_all(app=app)
#         print('Created Database!')
