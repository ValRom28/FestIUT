from app import db
import base64
from PIL import Image
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
from datetime import datetime
import datetime

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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get("rechercheGroupe") != None:
            return redirect(url_for('rechercheGroupe', nomGroupe=request.form.get("rechercheGroupe")))
        selected_date_debut = request.form.get('dateDebut')
        selected_date_fin = request.form.get('dateFin')
        selected_place = request.form.get('place')
        filtered_concerts = filter_concerts(selected_date_debut,selected_date_fin, selected_place)
    else:
        date = datetime.datetime.now()
        selected_date_debut = date.today().strftime("%Y-%m-%d")
        selected_date_fin = (date + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        selected_place = '1'
        filtered_concerts = filter_concerts(selected_date_debut,selected_date_fin, selected_place)
    lieux = get_lieux()
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('accueil.html', 
                           concerts=filtered_concerts, 
                           selected_date_debut=selected_date_debut,
                           selected_date_fin=selected_date_fin, 
                           selected_place=selected_place,
                           connecter=connecter,
                           admin=admin,
                           lieux = lieux)

@app.route('/rechercheGroupe')
def rechercheGroupe():
    nomGroupe = request.args.get('nomGroupe')
    groupes = get_groupes_by_nom(nomGroupe)
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    images = dict()
    for groupe in groupes:
        if groupe.photo_groupe != None:
            images[groupe.id_groupe] = base64.b64encode(groupe.photo_groupe).decode('utf-8')
        else:
            images[groupe.id_groupe] = None
    return render_template('favoris.html', liste_favoris=groupes,connecter=connecter,admin=admin, images=images)

@app.route('/programmation')
def programmation():
    concerts = filter_concerts_date(datetime.datetime.now())
    lieux = get_lieux()
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('programmation.html', concerts=concerts,lieux=lieux,connecter=connecter,admin=admin)

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

    images = dict()
    for groupe in liste_favoris:
        images[groupe.id_groupe] = base64.b64encode(groupe.photo_groupe).decode('utf-8')
        if groupe.photo_groupe != None:
            images[groupe.id_groupe] = base64.b64encode(groupe.photo_groupe).decode('utf-8')
        else:
            images[groupe.id_groupe] = None
    print(current_user.get_id())
    print(liste_favoris)
    return render_template('favoris.html', liste_favoris = liste_favoris,connecter=connecter,admin=admin, images=images)


@app.route("/groupe/<int:id_groupe>")
def groupe_detail(id_groupe):
    groupes_semblable =[]
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    groupe = get_groupe_by_id(id_groupe)
    style = get_style_by_id_groupe(groupe.id_groupe)
    artistes= get_artistes_by_id_groupe(groupe.id_groupe)
    like= est_favoris(id_groupe, current_user.get_id())
    groupes_semblable=get_groupe_by_style(style.id_style)
    images_propositions = dict()
    concerts=get_concert_by_id_groupe(id_groupe)
    instrument=[]
    if groupe.photo_groupe is not None:
        photo_groupe = base64.b64encode(groupe.photo_groupe).decode('utf-8')
        for groupe_semb in groupes_semblable:
            images_propositions[groupe_semb.id_groupe] = base64.b64encode(groupe_semb.photo_groupe).decode('utf-8')
    else:
        photo_groupe = None
    for artiste in artistes:
        instrument.append(get_instrument_by_id_artiste(artiste.id_artiste))
   
    event = (get_event_by_id_groupe(groupe.id_groupe))
    concerts_et_lieux = [(concert, get_lieu_by_id(concert.id_lieu)) for concert in concerts]
    events_et_lieux = [(e, get_lieu_by_id(e.id_lieu)) for e in event]
    return render_template('groupe_info.html', groupe=groupe, style=style, connecter=connecter,
                           admin=admin,artistes=artistes,like=like,groupes_semblable=groupes_semblable,
                           concerts_et_lieux=concerts_et_lieux,instruments=instrument,
                           events_et_lieux=events_et_lieux, photo_groupe=photo_groupe, 
                           images_prop=images_propositions)

@app.route('/ajouter_aux_favoris/<int:id_groupe>', methods=['POST'])
def ajouter_aux_favoris(id_groupe):
    ajouter_favoris(id_groupe, current_user.get_id())
    return redirect(url_for('groupe_detail', id_groupe=id_groupe))

@app.route('/supprimer_des_favoris/<int:id_groupe>', methods=['POST'])
def supprimer_des_favoris(id_groupe):
    supprimer_favoris(id_groupe, current_user.get_id())
    return redirect(url_for('groupe_detail', id_groupe=id_groupe))

@app.route("/ajout_groupe")
def ajout_groupe():
    liste_artiste = get_artistes()
    liste_hebergement = get_hebergement()
    styles = get_styles()
    return render_template('ajout_groupe.html', liste = liste_artiste, hebergements = liste_hebergement, styles = styles)

@app.route("/ajout_groupe", methods=['POST'])
def inserer_groupe():
    id_groupe = get_prochain_id_groupe()
    # Récupérer les données du formulaire
    nom_groupe = request.form.get('nom_groupe')
    description = request.form.get('textarea')
    nom_insta = request.form.get('nom_insta')
    nom_spotify = request.form.get('nom_spotify')

    # Récupérer les artistes sélectionnés
    artistes = request.form.getlist('artiste[]')

    # Récupérer les hébergements sélectionnés
    hebergement = request.form.get('hebergement')

    style = request.form.get('style')


    for artiste in artistes:
        insere_appartenir(artiste, id_groupe)

    insere_etrestyle(style, id_groupe)
    insere_groupe(id_groupe, nom_groupe, None, description, nom_insta, nom_spotify, hebergement)
    return redirect(url_for("ajout_groupe")) # ca faudra le changer quand t'aura fait la page admin
  
@app.route("/groupe/<int:id_groupe>/modification", methods=['GET', 'POST'])
def groupe_modification(id_groupe):
    form = GroupeForm()
    formConcert = ConcertForm()
    formEvent = EventForm()
    formLieu = LieuForm()
    admin = True
    connecter = True
    instrument = []

    groupe = get_groupe_by_id(id_groupe)
    style = get_style_by_id_groupe(groupe.id_groupe)
    artistes = get_artistes_by_id_groupe(groupe.id_groupe)
    concerts = get_concert_by_id_groupe(id_groupe)
    instrument = []
    event = get_event_by_id_groupe(groupe.id_groupe)
    concerts_et_lieux = [(concert, get_lieu_by_id(concert.id_lieu)) for concert in concerts]
    events_et_lieux = [(e, get_lieu_by_id(e.id_lieu)) for e in event]
    
    for e, lieu in events_et_lieux:
        formEvent = EventForm()
        formEvent.id_event.data = e.id_event
        if formEvent.validate_on_submit():
            e.nom_event = formEvent.nom_event.data
            e.date_event =  datetime.strptime(formEvent.date_event.data, '%Y-%m-%d')
            lieu.nom_lieu = formLieu.nom_lieu.data
            lieu.jauge_lieu = formLieu.jauge_lieu.data
            lieu.coordonne_X = formLieu.coordonne_X.data
            lieu.coordonne_Y = formLieu.coordonne_Y.data
            db.session.commit()
            return redirect(url_for('groupe_detail', id_groupe=id_groupe))

    for concert, lieu in concerts_et_lieux:
        formConcert = ConcertForm()
        formConcert.id_concert.data = concert.id_concert
        if formConcert.validate_on_submit():
            concert.nom_concert = formConcert.nom_concert.data
            concert.tps_prepa_concert = formConcert.tps_prepa_concert.data
            concert.date_heure_concert = datetime.strptime(formConcert.date_heure_concert.data, '%Y-%m-%d')
            concert.duree_concert = formConcert.duree_concert.data
            lieu.nom_lieu = formLieu.nom_lieu.data
            lieu.jauge_lieu = formLieu.jauge_lieu.data
            lieu.coordonne_X = formLieu.coordonne_X.data
            lieu.coordonne_Y = formLieu.coordonne_Y.data
            db.session.commit()
            return redirect(url_for('groupe_detail', id_groupe=id_groupe))

    
            

    
    if form.validate_on_submit():
        groupe.description_groupe = form.description_groupe.data
        groupe.spotify_groupe = form.spotify_groupe.data
        groupe.insta_groupe = form.insta_groupe.data
        db.session.commit()
        return redirect(url_for('groupe_detail', id_groupe=groupe.id_groupe))
    
    for artiste in artistes:
        instrument.append(get_instrument_by_id_artiste(artiste.id_artiste))
   
    
    form.description_groupe.data = groupe.description_groupe
    form.spotify_groupe.data = groupe.spotify_groupe
    form.insta_groupe.data = groupe.insta_groupe
    for concert in concerts_et_lieux:
        formConcert.nom_concert.data = concert[0].nom_concert
        formConcert.tps_prepa_concert.data = concert[0].tps_prepa_concert
        formConcert.date_heure_concert.data = concert[0].date_heure_concert
        formConcert.duree_concert.data = concert[0].duree_concert
        formLieu.nom_lieu.data = concert[1].nom_lieu
        formLieu.jauge_lieu.data = concert[1].jauge_lieu
        formLieu.coordonne_X.data = concert[1].coordonne_X
        formLieu.coordonne_Y.data = concert[1].coordonne_Y
        
    for event in events_et_lieux: 
        formEvent.id_event.data = event[0].id_event
        formEvent.nom_event.data = event[0].nom_event
        formEvent.date_event.data = event[0].date_event
        formLieu.nom_lieu.data = event[1].nom_lieu
        formLieu.jauge_lieu.data = event[1].jauge_lieu
        formLieu.coordonne_X.data = event[1].coordonne_X
        formLieu.coordonne_Y.data = event[1].coordonne_Y
        
        
    return render_template('modif_groupe.html', groupe=groupe, style=style, artistes=artistes,instrument=instrument,connecter=connecter,admin=admin,form=form,formConcert=formConcert,formEvent=formEvent,concerts_et_lieux=concerts_et_lieux,events_et_lieux=events_et_lieux,formLieu=formLieu)
    
@app.route("/groupe/<int:id_groupe>/delete", methods=['GET'])
def groupe_delete(id_groupe):
    groupe = get_groupe_by_id(id_groupe)
    delete_groupe(groupe)
    return redirect(url_for('groupes'))

@app.route("/concert")
def concert():
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    concert = get_concert_by_id(int(request.args.get("concert")))
    lieu = get_lieu_by_id(concert.id_lieu)
    groupe = get_groupe_by_id_concert(concert.id_concert)
    style = get_style_by_id_groupe(groupe.id_groupe)
    return render_template('concert_info.html', concert = concert,groupe=groupe,lieu=lieu,style = style,connecter=connecter,admin=admin)

@app.route("/concert_delete")
def concert_delete(id_concert):
    concert = get_concert_by_id(id_concert)
    delete_concert(concert)
    return redirect(url_for('programmation'))

@app.route("/ajout_instrument")
def ajout_instrument():
    return render_template('ajout_instrument.html')

@app.route("/ajout_instrument", methods=['POST'])
def inserer_instrument():
    id_instrument = get_prochain_id_instrument()
    # Récupérer les données du formulaire
    nom_instrument = request.form.get('nom_instrument')

    insere_instrument(id_instrument, nom_instrument)
    return redirect(url_for("ajout_instrument")) # ca faudra le changer quand t'aura fait la page admin

@app.route("/ajout_artiste")
def ajout_artiste():
    instruments = get_instrument()
    return render_template('ajout_artiste.html', instruments = instruments)

@app.route("/ajout_artiste", methods=['POST'])
def inserer_artiste():
    id_artiste = get_prochain_id_artiste()
    # Récupérer les données du formulaire
    nom_artiste = request.form.get('nom_artiste')


    # Récupérer les hébergements sélectionnés
    id_instrument = request.form.get('instrument')

    insere_artiste(id_artiste, nom_artiste)
    insere_jouer(id_artiste, id_instrument)
    return redirect(url_for("ajout_artiste")) # ca faudra le changer quand t'aura fait la page admin
 
@app.route("/ajout_hebergement")
def ajout_hebergement():
    return render_template('ajout_hebergement.html')

@app.route("/ajout_hebergement", methods=['POST'])
def inserer_hebergement():
    id_hebergement = get_prochain_id_hebergement()
    # Récupérer les données du formulaire
    nom_hebergement = request.form.get('nom_hebergement')
    adresse_hebergement = request.form.get('adresse_hebergement')

    insere_hebergement(id_hebergement, nom_hebergement, adresse_hebergement)

    return redirect(url_for("ajout_hebergement")) # ca faudra le changer quand t'aura fait la page admin


@app.route("/ajout_concert")
@login_required
def ajout_concert():
    lieux = get_all_lieux()
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('ajout_concert.html', lieux = lieux, connecter=connecter,admin=admin)

@app.route("/ajout_concert", methods=['POST'])
@login_required
def inserer_concert():
    id_concert = get_prochain_id_concert()
    # Récupérer les données du formulaire
    nom_concert = request.form.get('nom_concert')
    tps_prepa_concert = request.form.get('tps_prepa_concert')
    duree_concert = request.form.get('duree_concert')
    date_concert_str = request.form.get('date_concert')
    id_lieu = request.form.get('lieu')

    date_concert = datetime.datetime.strptime(date_concert_str, '%Y-%m-%dT%H:%M')

    insere_concert(id_concert, nom_concert, tps_prepa_concert, date_concert, duree_concert, id_lieu)

    return redirect(url_for("programmation"))