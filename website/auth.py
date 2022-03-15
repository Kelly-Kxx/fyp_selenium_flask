from flask import Blueprint, render_template , request, flash,redirect,url_for
import pymongo
from pymongo import MongoClient
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, login_required, logout_user, current_user



auth = Blueprint('auth',__name__)
@auth.route("/signup",methods = ['GET','POST']) #/auth/login
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        passoword1 = request.form.get("password1")
        passoword2 = request.form.get("password2")
        #print("Sign Up", email,firstName,passoword1,passoword2)
        user = User.query.filter_by(email=email).first()
        if(passoword1 != passoword2):
            flash("Password does not match", category="error") #use category to display message color
        elif user:
            flash('Email already exists.', category='error')
        else:
            new_user = User(email = email, firstName = firstName, password = generate_password_hash(passoword1,method='sha256'))
            db.session.add(new_user)   #add user to the db
            db.session.commit()  #I have made changes, Update it
            flash("Account Created Successfully", category="success")
            login_user(user,remember=True)

            return redirect(url_for('views.homepage')) #views: name of blurprint, homepage : function
    return render_template("signup.html",user=current_user)


@auth.route("/login", methods = ['GET','POST']) #/auth/login
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
    
        if user: # if we found a user
            if(check_password_hash(user.password, password)):#check the user password correct or not 
                flash('Login Succress!', category='success')
                login_user(user,remember=True)
                return redirect(url_for("views.homepage"))
            else:
                flash('Incorrect password, Try Again.', category='error')
        else:
            flash('Email does not exist',category='error')
    return render_template("login.html",user=current_user)

@auth.route("/logout") #/auth/login
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))