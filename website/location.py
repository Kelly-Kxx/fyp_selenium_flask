from flask import Blueprint, jsonify, render_template,request,flash, redirect, url_for
import sqlite3

from os import listdir
from os.path import isfile, join
location = Blueprint('location',__name__)

@location.route('/',methods=['GET','POST']) 
def Location():
    if request.method == "GET":
        db_dir = "./website/database/"
        files = [f for f in listdir(db_dir) if isfile(join(db_dir, f))]
        return files

