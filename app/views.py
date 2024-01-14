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
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    liste_groupe = get_groupes()
    return render_template('groupes.html', liste_groupes = liste_groupe,connecter=connecter,admin=admin)

@app.route("/favoris")
def favoris():
    """
        Cette fonction nous permet de nous diriger vers la page qui
        liste les parcours
    """
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
        liste_favoris = get_favoris(current_user.get_id())
    
    print(current_user.get_id())
    print(liste_favoris)
    return render_template('favorie.html', liste_favoris = liste_favoris,connecter=connecter,admin=admin)


@app.route("/groupe/<int:id_groupe>")
def groupe_detail(id_groupe):
    groupes_semblable =[]
    lieux_concerts=[]
    lieux_events=[]
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    groupe = get_groupes_by_id(id_groupe)
    style = get_style_by_id(groupe[0].id_groupe)
    artistes= get_artistes_by_id_groupe(groupe[0].id_groupe)
    groupe = groupe[0]
    like= est_favoris(id_groupe, current_user.get_id())
    if(len(style)>0):
        groupes_semblable=get_groupe_by_style(style[0].id_style)  
        style=style[0]
    concerts=get_concert_by_id_groupe(id_groupe)
    instrument=[]
    for artiste in artistes:
        instrument.append(get_instrument_by_id_artiste(artiste.id_artiste))
   
    event = (get_event_by_id_groupe(groupe.id_groupe))
    concerts_et_lieux = [(concert, get_lieu_by_id(concert.id_lieu)) for concert in concerts]
    events_et_lieux = [(e, get_lieu_by_id(e.id_lieu)) for e in event]
    print(lieux_events)
    print(lieux_concerts)
    return render_template('groupe_info.html', groupe=groupe, style=style, connecter=connecter,admin=admin,artistes=artistes,like=like,groupes_semblable=groupes_semblable,concerts_et_lieux=concerts_et_lieux,instruments=instrument,events_et_lieux=events_et_lieux)

@app.route('/ajouter_aux_favoris/<int:id_groupe>', methods=['POST'])
def ajouter_aux_favoris(id_groupe):
    ajouter_favoris(id_groupe, current_user.get_id())
    return redirect(url_for('groupe_detail', id_groupe=id_groupe))

@app.route('/supprimer_des_favoris/<int:id_groupe>', methods=['POST'])
def supprimer_des_favoris(id_groupe):
    supprimer_favoris(id_groupe, current_user.get_id())
    return redirect(url_for('groupe_detail', id_groupe=id_groupe))
    
