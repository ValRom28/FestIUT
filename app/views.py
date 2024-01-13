import os
from app import app
from flask import render_template, request, redirect, url_for, make_response, send_file, jsonify, Response
from flask_login import login_required, login_user, logout_user, current_user
from io import BytesIO
from functools import wraps
from werkzeug.utils import secure_filename
from app.requests import *
from app.forms import *
from app import login_manager
from app.models import *
import base64

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = get_user_by_email(form.mail.data)
    if form.validate_on_submit():
        if user:
            if user.mdp_spectateur == form.mdp.data:
                login_user(user, force=True)
                return redirect(url_for('home'))
    return render_template('connexion.html', form=form)

@app.route('/')
def home():
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('accueil.html',connecter=connecter,admin=admin)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registration',methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('inscription.html', form=form)



@app.route("/groupes")
def groupes():
    """
        Cette fonction nous permet de nous diriger vers la page qui
        liste les parcours
    """
    liste_groupe = get_groupes()
    return render_template('groupes.html', liste_groupes = liste_groupe)



