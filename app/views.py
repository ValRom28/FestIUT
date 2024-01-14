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


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


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
    form.validate_password(form.password)
    if form.validate_on_submit() and form.password.data == form.confirm_password.data:
        spectateur = Spectateur(nom_spectateur=form.username.data, email_spectateur=form.email.data, mdp_spectateur=form.password.data)
        db.session.add(spectateur)
        db.session.commit()
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
    liste_favoris = []
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
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    groupe = get_groupes_by_id(id_groupe)
    groupe = groupe[0]
    style = get_style_by_id_groupe(groupe.id_groupe)
    style = style[0]
    print(style)
    artistes= get_artistes_by_id_groupe(groupe.id_groupe)
    
    like= est_favoris(id_groupe, current_user.get_id())
    groupes_semblable=get_groupe_by_style(style.id_style)  
    concerts=get_concert_by_id_groupe(id_groupe)
    instrument=[]
    for artiste in artistes:
        instrument.append(get_instrument_by_id_artiste(artiste.id_artiste))
   
    event = (get_event_by_id_groupe(groupe.id_groupe))
    concerts_et_lieux = [(concert, get_lieu_by_id(concert.id_lieu)) for concert in concerts]
    events_et_lieux = [(e, get_lieu_by_id(e.id_lieu)) for e in event]
    return render_template('groupe_info.html', groupe=groupe, style=style, connecter=connecter,admin=admin,artistes=artistes,like=like,groupes_semblable=groupes_semblable,concerts_et_lieux=concerts_et_lieux,instruments=instrument,events_et_lieux=events_et_lieux)

@app.route('/ajouter_aux_favoris/<int:id_groupe>', methods=['POST'])
def ajouter_aux_favoris(id_groupe):
    ajouter_favoris(id_groupe, current_user.get_id())
    return redirect(url_for('groupe_detail', id_groupe=id_groupe))

@app.route('/supprimer_des_favoris/<int:id_groupe>', methods=['POST'])
def supprimer_des_favoris(id_groupe):
    supprimer_favoris(id_groupe, current_user.get_id())
    return redirect(url_for('groupe_detail', id_groupe=id_groupe))


@app.route("/groupe/<int:id_groupe>/modification", methods=['GET', 'POST'])
def groupe_modification(id_groupe):
    form= GroupeForm()
    formConcert= ConcertForm()
    formEvent= EventForm()
    formLieu= LieuForm()
    admin=True
    connecter=True
    instrument=[]
    groupe = get_groupes_by_id(id_groupe)
    groupe = groupe[0]
    style = get_style_by_id_groupe(groupe.id_groupe)
    style = style[0]
    artistes= get_artistes_by_id_groupe(groupe.id_groupe)
    concerts=get_concert_by_id_groupe(id_groupe)
    instrument=[]
    for artiste in artistes:
        instrument.append(get_instrument_by_id_artiste(artiste.id_artiste))
   
    event = (get_event_by_id_groupe(groupe.id_groupe))
    concerts_et_lieux = [(concert, get_lieu_by_id(concert.id_lieu)) for concert in concerts]
    events_et_lieux = [(e, get_lieu_by_id(e.id_lieu)) for e in event]
    form.description_groupe.data = groupe.description_groupe
    form.spotify_groupe.data = groupe.spotify_groupe
    form.insta_groupe.data = groupe.insta_groupe
    for concert in concerts_et_lieux:
        formConcert.tps_prepa_concert.data = concert[0].tps_prepa_concert
        formConcert.date_heure_concert.data = concert[0].date_heure_concert
        formConcert.duree_concert.data = concert[0].duree_concert
        formLieu.nom_lieu.data = concert[1].nom_lieu
        formLieu.jauge_lieu.data = concert[1].jauge_lieu
        formLieu.coordonne_X.data = concert[1].coordonne_X
        formLieu.coordonne_Y.data = concert[1].coordonne_Y
        
    for event in events_et_lieux:
        formEvent.date_event.data = event[0].date_event
        formLieu.nom_lieu.data = event[1].nom_lieu
        formLieu.jauge_lieu.data = event[1].jauge_lieu
        formLieu.coordonne_X.data = event[1].coordonne_X
        formLieu.coordonne_Y.data = event[1].coordonne_Y
    # if form.validate_on_submit():
    #     groupe.description_groupe = form.description_groupe.data
    #     groupe.spotify_groupe = form.spotify_groupe.data
    #     groupe.insta_groupe = form.insta_groupe.data
    #     db.session.commit()
        
    # for concert,lieu in concerts_et_lieux:
    #     if formConcert.validate_on_submit():
    #         concert.tps_prepa_concert = formConcert.tps_prepa_concert.data
    #         concert.date_heure_concert = formConcert.date_heure_concert.data
    #         concert.duree_concert = formConcert.duree_concert.data
    #         lieu.nom_lieu = formLieu.nom_lieu.data
    #         lieu.jauge_lieu = formLieu.jauge_lieu.data
    #         lieu.coordonne_X = formLieu.coordonne_X.data
    #         lieu.coordonne_Y = formLieu.coordonne_Y.data
    #         db.session.commit()
    #         return redirect(url_for('groupe_detail', id_groupe=id_groupe))
        
    return render_template('modif_groupe.html', groupe=groupe, style=style, artistes=artistes,instrument=instrument,connecter=connecter,admin=admin,form=form,formConcert=formConcert,formEvent=formEvent,concerts_et_lieux=concerts_et_lieux,events_et_lieux=events_et_lieux,formLieu=formLieu)
    
@app.route("/groupe/<int:id_groupe>/delete", methods=['GET'])
def groupe_delete(id_groupe):
    print("delete")
    groupe = get_groupes_by_id(id_groupe)
    groupe = groupe[0]
    delete_groupe(groupe)
    print("true")
    return redirect(url_for('groupes'))
