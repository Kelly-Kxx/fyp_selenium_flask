from random import choices
from flask import Blueprint, jsonify, render_template,request,flash,redirect,url_for

import sqlite3
from numpy import empty
from .excel_data import Device_Excel_Table, get_arr, get_by_ID_from_table
from .location import get_all_location
# from website import excel_data
# from downloadFiles
views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST']) 
def Homepage():
    print("Homepage",request.method)
    if request.method =="GET":
        loc_list = get_all_location()
        return render_template("home.html", loc_list = loc_list) 
    if request.method =="POST":   
        if request.form.get("selenium"):
            print("in selenium")
            return redirect(url_for("views.Homepage"))
        elif request.form.get("location"):
            print("selection")
            loc = request.form.get("location")
            return redirect(url_for("views.location_list", loc=loc))
        elif request.form.get("input_location"):
            print("in input")
            loc = request.form.get("input_location")
            if request.form.get("input_system"):
                print("can get sys")
                sys = request.form.get("input_system")
                if request.form.get("input_device"):
                    print("can get dev")
                    dev = request.form.get("input_device")
                    if request.form.get("input_equip"):
                        print("if loop")
                        equip_no = request.form.get("input_equip")
                        return redirect(url_for("views.get_by_ID", loc= loc, sys= sys, device = dev,eqipID =equip_no))
                    else:
                        print(f"else loop {loc}, {sys} {dev}")
                        return redirect(url_for("views.table_list", loc= loc, sys= sys, device = dev))
                else:
                    print("cannot get dev")
                    flash("Please enter Decive Short Form eg. CTR", category="error") 
                    return redirect("/")
                
            else:
                print("cannot get sys")
                flash("Please enter System Short Form eg. AUS", category="error")    
                return redirect(url_for("views.Homepage"))   
        else:
            print("cannot get loc")
            flash("Please enter Location Short Form eg. HKBCF_001", category="error")
            return redirect(url_for("views.Homepage"))
            
                
            
            
            

@views.route('/<loc>',methods=['GET','POST'])
def location_list(loc):
    if loc == "Location":
        return (redirect(url_for("views.Homepage")))
    if ".db" not in loc:
        loc = loc + ".db"
    loc_no_filetype = loc.split('.')[0]
    sys_arr = get_arr(loc,True)
    print(f"Method: {request.method} in location list")
    
    if request.method == "GET":
        print("in location get")
        return render_template("sys.html", sys_arr = sys_arr, Location = loc, location_link = loc_no_filetype)
    if request.method == "POST": 
        print("in location post")
        
        sys = request.form.get("system") 
        print(f"sys: {sys}")
        return redirect(url_for("views.system_list", loc= loc_no_filetype, sys= sys)) #, loc = loc_no_filetype, sys = sys, device_arr = device_arr



@views.route('/<loc>/<sys>',methods=['GET','POST'])
def system_list(loc, sys): #loc,sys,device_arr
    print(f"Method: {request.method} {loc} {sys} in system_list")
    if ".db" not in loc:
        loc = loc + ".db"
    loc_no_filetype = loc.split('.')[0]
    device_arr = get_arr(loc,False)
    if request.method == "GET":
        print(f"in sys_list GET")
        return render_template("device.html", System = sys, device_arr = device_arr)
    if request.method == "POST": 
        print("in sys post")
        dev = request.form.get("device") 
        return redirect(url_for("views.table_list", loc= loc_no_filetype, sys= sys, device = dev))


@views.route('/<loc>/<sys>/<device>',methods=['GET','POST'])
def table_list(loc, sys, device):
    print(f"Method: {request.method} {loc} {sys} {device} in table_list")
    if request.method =="GET":
        [data, attr_list] = Device_Excel_Table(loc,sys,device)
        return render_template("table.html",
                                data =data , 
                                attr_list = attr_list,
                                loc = loc,
                                sys = sys,
                                device = device
                                ) 


@views.route('/<loc>/<sys>/<device>/<eqipID>',methods=['GET','POST', 'PUT'])
def get_by_ID(loc, sys, device, eqipID):
    print(f"Method: {request.method} {loc} {sys} {device}  {eqipID}in table_list")
    if request.method =="GET":
        [data, attr_list] = get_by_ID_from_table(loc,sys,device,eqipID)
        return render_template("table.html",
                                data =data , 
                                attr_list = attr_list,
                                loc = loc,
                                sys = sys,
                                device = device
                                ) 
    if request.method =="POST":
        pass