from flask import Blueprint, jsonify, render_template,request,flash
from flask_login import login_required,  current_user
from .models import Note
from . import db
import json
views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST']) 
@login_required
def homepage():
    if(request.method=='POST'):
        note = request.form.get('note')
        if(len(note)<1):
            flash('Note is too short!',category='error')
        else:
            new_note = Note(data=note,user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note is created!", category='success')
    return render_template("home.html",user=current_user) #allows the template to check user
    


<<<<<<< HEAD
# @views.route('/delete-note',method=['POST'])
=======
# @views.route('/delete-note',method=['POST']) #not index.js problem
>>>>>>> 2a7d6be (create table, create model, insert data)
# def delete_note():
   
#     note = json.loads(request.data)

<<<<<<< HEAD
#     # noteId = note['noteId'] #index.js
#     # note = Note.query.get(noteId)
#     # if(note):
#     #     if(note.user_Id==current_user.id):
#     #         db.session.delete(note)
#     #         db.session.commit()
=======
#     noteId = note['noteId'] #index.js
#     note = Note.query.get(noteId)
#     if(note):
#         if(note.user_Id==current_user.id):
#             db.session.delete(note)
#             db.session.commit()
>>>>>>> 2a7d6be (create table, create model, insert data)
#     return jsonify({}) # turn into json object