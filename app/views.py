import os
from app import app
from flask import render_template, request, redirect, url_for, make_response, send_file, jsonify, Response
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from io import BytesIO
from functools import wraps
from werkzeug.utils import secure_filename
from app.requests import *
from app.forms import *
from app import login_manager
import base64

# @app.route('/editUser', methods=['GET', 'POST'])
# @activated_required
# @login_required
# def editUser():
#     user = get_user_by_id(current_user.get_id())
#     form = EditUserForm(id=user.idPompier, nom=user.nomPompier, prenom=user.prenomPompier, mail=user.emailPompier, mdp=user.mdpPompier, photo=user.photoPompier,telephone=user.telephonePompier)
#     page_name = f'Modifier le profil : {user.nomPompier} {user.prenomPompier}'
#     if form.validate_on_submit():
#         password = generate_password_hash(form.mdp.data).decode('utf-8')
#         if form.photo.data:
#             encoded_photo = base64.b64encode(form.photo.data.read())
#             update_user_photo(user.idPompier, encoded_photo)
#         update_user(user.idPompier, form.prenom.data, form.nom.data, form.mail.data, form.telephone.data, password)
#         return redirect(url_for('user'))
#     return render_template('editUser.html', nom_page=page_name, user=user, form=form, notification_enabled=user_has_notifications(current_user.get_id()), is_admin =get_user_by_id(current_user.get_id()).idRole == 1)

@app.route('/login')
def login():
    return render_template('connexion.html')