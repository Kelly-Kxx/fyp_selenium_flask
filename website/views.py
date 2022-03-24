from flask import Blueprint, jsonify, render_template,request,flash
# from flask_login import login_required,  current_user
# from .models import Note
import sqlite3
# # from . import db
# import json
views = Blueprint('views',__name__)

def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    
    
    return conn


@views.route('/',methods=['GET','POST']) 
def homepage():
    table_name = "I_HKBCF_001_GF_AUS_PCW"
    conn = get_db_connection("./website/database/HKBCF_001.db")
    cursor = conn.cursor()
    data_list = cursor.execute(f""" SELECT * 
                                    FROM {table_name}
                                     """)
    attr_list = []
    data = []
    for col in data_list.description:
        
        attr_list.append(col[0])
    for row in data_list:
        print(row)
        data.append(row)
    conn.commit()
    conn.close()
    return render_template("index.html",data =data , attr_list = attr_list) # 



# @login_required
# def homepage():
#     if(request.method=='POST'):
#         note = request.form.get('note')
#         if(len(note)<1):
#             flash('Note is too short!',category='error')
#         else:
#             new_note = Note(data=note,user_id = current_user.id)
#             db.session.add(new_note)
#             db.session.commit()
#             flash("Note is created!", category='success')
#     return render_template("home.html",user=current_user) #allows the template to check user
    
