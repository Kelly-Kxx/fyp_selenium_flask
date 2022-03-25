from random import choices
from flask import Blueprint, jsonify, render_template,request,flash,redirect,url_for

import sqlite3

from numpy import empty
from .device import Device_Excel_Table
from .location import Location
from website import device
views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST']) 
def Homepage():
    print("Homepage",request.method)
    
    if request.method =="GET":
        [data, attr_list] = Device_Excel_Table()
        loc_list = Location()
        return render_template("home.html",
                                data =data , 
                                attr_list = attr_list, 
                                loc_list = loc_list) 
    if request.method =="POST":
        loc = request.form.get("location")
        return redirect(url_for("views.location_list", loc=loc))

@views.route('/<loc>',methods=['GET','POST'])
def location_list(loc):
    if loc == "Location":
        return (redirect(url_for("views.Homepage")))
    if ".db" not in loc:
        loc = loc + ".db"
    db_dir = "./website/database/"
    conn = sqlite3.connect(db_dir + '/'+ loc)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table'""")
    table_arr = cursor.fetchall()
    loc_no_filetype = loc.split('.')[0]
    sys_arr, device_arr = [], []
    for i in table_arr:
        spl = i[0].split('_')
        if spl[-2] not in sys_arr:
            sys_arr.append(spl[-2])
        if spl[-1] not in device_arr:
            device_arr.append(spl[-1])
    
    
    print(f"Method: {request.method} in location list")
    print(f"device_arr : {device_arr}")
    if request.method == "GET":
        print("in location get")
        return render_template("sys.html", sys_arr = sys_arr, Location = loc, location_link = loc_no_filetype, device_arr = device_arr)
    if request.method == "POST": 
        print("in location post")
        sys = request.form.get("system")
        print(f"sys: {sys}, device_arr : {device_arr}")
        return redirect(url_for("views.system_list", loc= loc, sys= sys, device_arr = device_arr)) #, loc = loc_no_filetype, sys = sys, device_arr = device_arr



@views.route('/<loc>/<sys>',methods=['GET','POST'])
def system_list(loc, sys,device_arr): #loc,sys,device_arr
    print(f"Method: {request.method} {loc} {sys} in system_list")
    return f"<h1>hihi</h1>"
    