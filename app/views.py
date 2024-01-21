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
    events = filter_events_date(datetime.date.today())
    concerts = filter_concerts_date(datetime.datetime.now())
    lieux = get_lieux()
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('programmation.html', concerts=concerts,lieux=lieux,connecter=connecter,admin=admin,events=events)

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
@login_required
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
@login_required
def ajouter_aux_favoris(id_groupe):
    ajouter_favoris(id_groupe, current_user.get_id())
    return redirect(url_for('groupe_detail', id_groupe=id_groupe))

@app.route('/supprimer_des_favoris/<int:id_groupe>', methods=['POST'])
@login_required
def supprimer_des_favoris(id_groupe):
    supprimer_favoris(id_groupe, current_user.get_id())
    return redirect(url_for('groupe_detail', id_groupe=id_groupe))

@app.route("/ajout_groupe")
@login_required
def ajout_groupe():
    liste_artiste = get_artistes()
    liste_hebergement = get_hebergement()
    styles = get_styles()
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('ajout_groupe.html', liste = liste_artiste, hebergements = liste_hebergement, styles = styles,connecter=connecter,admin=admin)

@app.route("/ajout_groupe", methods=['POST'])
@login_required
def inserer_groupe():
    hebergement_plein = False
    connecter = False
    admin = False
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
    
    obj_hebergement = get_hebergement_by_id(hebergement)
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    if obj_hebergement.jauge_hebergement > 0:
        for artiste in artistes:
            insere_appartenir(artiste, id_groupe)
        insere_etrestyle(style, id_groupe)
        insere_groupe(id_groupe, nom_groupe, None, description, nom_insta, nom_spotify, hebergement)
        obj_hebergement.jauge_hebergement -= 1
        db.session.commit()
    else:
        hebergement_plein = True
        return render_template('ajout_groupe.html', connecter=connecter, admin=admin, hebergement_plein=hebergement_plein, hebergements=get_hebergement(), styles=get_styles(), liste=get_artistes())
    return redirect(url_for("groupes")) 
  
@app.route("/groupe/<int:id_groupe>/modification", methods=['GET', 'POST'])
@login_required
def groupe_modification(id_groupe):
    admin = True
    connecter = True
    instrument = []

    groupe = get_groupe_by_id(id_groupe)
    style = get_style_by_id_groupe(groupe.id_groupe)
    artistes = get_artistes_by_id_groupe(groupe.id_groupe)
    concerts = get_concert_by_id_groupe(id_groupe)
    instrument = [get_instrument_by_id_artiste(artiste.id_artiste) for artiste in artistes]
    events = get_event_by_id_groupe(groupe.id_groupe)
    lieux = get_all_lieux()

    form_groupe = GroupeForm(obj=groupe)

    liste_form_concerts = [ConcertForm(obj=concert) for concert in concerts]
    liste_form_events = [EventForm(obj=event) for event in events]
            
    if request.method == 'POST':
        errors = []

        if form_groupe.validate_on_submit():
            form_groupe.populate_obj(groupe)
            modif_groupe(id_groupe, groupe.nom_groupe, groupe.description_groupe, groupe.insta_groupe, groupe.spotify_groupe)

        for form_concert in liste_form_concerts:
            if form_concert.validate_on_submit():
                id_concert = form_concert.id_concert.data
                concert = get_concert_by_id(id_concert)
                form_concert.populate_obj(concert)
                modif_concert(concert.id_concert, form_concert.nom_concert.data, form_concert.tps_prepa_concert.data, form_concert.date_heure_concert.data, form_concert.duree_concert.data)
            else:
                errors.append(form_concert.errors)

        for form_event in liste_form_events:
            if form_event.validate_on_submit():
                id_event = form_event.id_event.data
                event = get_event_by_id(id_event)
                form_event.populate_obj(event)
                modif_event(event.id_event, form_event.nom_event.data, form_event.date_event.data)
            else:
                errors.append(form_event.errors)

        if not errors:
            return redirect(url_for('groupe_detail', id_groupe=id_groupe))
        else:
            print(errors)

    return render_template('modif_groupe.html', groupe=groupe, style=style, 
                           artistes=artistes, instrument=instrument, connecter=connecter,
                           admin=admin, form_groupe=form_groupe, liste_form_concerts=liste_form_concerts,
                           liste_form_events=liste_form_events, lieux=lieux)

    
@app.route("/groupe/<int:id_groupe>/delete", methods=['GET'])
@login_required
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

@app.route("/evenement")
def evenement():
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    event = get_event_by_id(int(request.args.get("event")))
    lieu = get_lieu_by_id(event.id_lieu)
    groupe = get_groupe_by_id_event(event.id_event)
    style = get_style_by_id_groupe(groupe.id_groupe)
    return render_template('event_info.html', event = event,groupe=groupe,lieu=lieu,style = style,connecter=connecter,admin=admin)

@app.route("/evenement_delete/<int:id_event>")
@login_required
def evenement_delete(id_event):
    event = get_event_by_id(id_event)
    delete_event(event)
    return redirect(url_for('programmation'))

@app.route("/concert_delete")
@login_required
def concert_delete(id_concert):
    concert = get_concert_by_id(id_concert)
    delete_concert(concert)
    return redirect(url_for('programmation'))

@app.route("/billetterie")
@login_required
def billetterie():
    admin = False
    connecter = False
    age = None
    mes_billets = []
    billets_concerts_types_lieu = []
    lieu = None
    if current_user.is_authenticated:
        connecter = True
        admin = current_user.is_admin()
        age = datetime.datetime.now().year - current_user.anniv_spectateur.year
        mes_billets = get_billets_by_id_spectateur(current_user.get_id())
        for billet in mes_billets:
            type = Type.query.get(billet.id_type)
            lieu = get_lieu_by_id_billet_and_dates(billet.id_billet, billet.date_billet,
                                                    billet.date_billet + datetime.timedelta(days=type.nb_jours))
            billets_concerts_types_lieu.append((billet, get_concerts_by_id_billet_dates_lieu(billet.id_billet,
                                        billet.date_billet, billet.date_billet + datetime.timedelta(days=type.nb_jours), lieu.id_lieu), 
                                        get_type_by_id_billet(billet.id_billet), lieu))
    types_billets = get_types_billet()
    return render_template('billetterie.html', types_billets=types_billets, mes_billets=billets_concerts_types_lieu, 
                           age=age, connecter=connecter, admin=admin, datetime=datetime)

@app.route("/achat_billet/<int:id_type_billet>", methods=['POST', 'GET'])
@login_required
def achat_billet(id_type_billet):
    admin = False
    connecter = False
    no_festival = False
    billet_existe = False
    valide = False
    jauge = None
    plus_place = False
    form = AchatBillet()
    lieux = Lieu.query.all()
    form.lieux.choices = [(lieu.id_lieu, lieu.nom_lieu) for lieu in lieux]
    if current_user.is_authenticated:
        connecter = True
        admin = current_user.is_admin()
    if form.validate_on_submit():
        selected_lieu = Lieu.query.get(int(form.lieux.data))
        jauge = selected_lieu.jauge_lieu
        type = Type.query.get(id_type_billet)
        concerts = concerts = get_concerts_by_id_lieu_between_dates(int(form.lieux.data), form.date.data, form.date.data + datetime.timedelta(days=type.nb_jours))
        if jauge == 0:
            plus_place = True
            return render_template('achat_billet.html', connecter=connecter, admin=admin, id_type_billet=id_type_billet,
                                      form=form, no_festival=no_festival, billet_existe=billet_existe, plus_place=plus_place)
        if concerts == []:
            no_festival = True
            return render_template('achat_billet.html', connecter=connecter, admin=admin, id_type_billet=id_type_billet, 
                                   form=form, no_festival=no_festival, billet_existe=billet_existe, plus_place=plus_place)
        for concert in concerts:
            valide = add_reservation(concert.id_concert, current_user.get_id())
            if not valide:
                billet_existe = True
                return render_template('achat_billet.html', connecter=connecter, admin=admin, id_type_billet=id_type_billet, 
                                       form=form, no_festival=no_festival, billet_existe=billet_existe, plus_place=plus_place)
        if valide:
            selected_lieu.jauge_lieu -= 1
            db.session.commit()
            add_billet(form.date.data, id_type_billet, current_user.get_id())
        return redirect(url_for('billetterie'))
    return render_template('achat_billet.html', connecter=connecter, admin=admin, id_type_billet=id_type_billet, 
                           form=form, no_festival=no_festival, billet_existe=billet_existe, plus_place=plus_place)

@app.route("/ajout_instrument")
@login_required
def ajout_instrument():
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('ajout_instrument.html',connecter=connecter,admin=admin)

@app.route("/ajout_instrument", methods=['POST'])
@login_required
def inserer_instrument():
    id_instrument = get_prochain_id_instrument()
    # Récupérer les données du formulaire
    nom_instrument = request.form.get('nom_instrument')

    insere_instrument(id_instrument, nom_instrument)
    return redirect(url_for("administration")) 

@app.route("/ajout_artiste")
@login_required
def ajout_artiste():
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    instruments = get_instrument()
    return render_template('ajout_artiste.html', instruments = instruments,connecter=connecter,admin=admin)

@app.route("/ajout_artiste", methods=['POST'])
@login_required
def inserer_artiste():
    id_artiste = get_prochain_id_artiste()
    # Récupérer les données du formulaire
    nom_artiste = request.form.get('nom_artiste')


    # Récupérer les hébergements sélectionnés
    id_instrument = request.form.get('instrument')

    insere_artiste(id_artiste, nom_artiste)
    insere_jouer(id_artiste, id_instrument)
    return redirect(url_for("administration")) 
 
@app.route("/ajout_hebergement")
@login_required
def ajout_hebergement():
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('ajout_hebergement.html',connecter=connecter,admin=admin)

@app.route("/ajout_hebergement", methods=['POST'])
@login_required
def inserer_hebergement():
    id_hebergement = get_prochain_id_hebergement()
    # Récupérer les données du formulaire
    nom_hebergement = request.form.get('nom_hebergement')
    adresse_hebergement = request.form.get('adresse_hebergement')

    insere_hebergement(id_hebergement, nom_hebergement, adresse_hebergement)
    return redirect(url_for("administration")) 

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

@app.route("/administration")
@login_required
def administration():
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('administration.html',connecter=connecter,admin=admin)

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

@app.route("/ajout_event")
@login_required
def ajout_event():
    lieux = get_all_lieux()
    groupes = get_groupes()
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('ajout_evenement.html', lieux = lieux, connecter=connecter,admin=admin, groupes = groupes)

@app.route("/ajout_event", methods=['POST'])
@login_required
def inserer_event():
    id_event = get_prochain_id_event()

    nom_event = request.form.get('nom_event')
    date_event_str = request.form.get('date_event')
    id_lieu = request.form.get('lieu')
    id_groupe = request.form.get('groupe')
    date_event = datetime.datetime.strptime(date_event_str, '%Y-%m-%dT%H:%M')

    
    insere_event(id_event, nom_event, date_event, id_lieu)
    insere_organiser_event(id_groupe, id_event)
    return redirect(url_for("programmation"))

@app.route("/ajout_lieu")
@login_required
def ajout_lieu():
    lieux = get_all_lieux()
    groupes = get_groupes()
    admin=False
    connecter=False
    if current_user.is_authenticated:
        connecter=True
        admin=current_user.is_admin()
    return render_template('ajout_lieu.html', lieux = lieux, connecter=connecter,admin=admin, groupes = groupes)

@app.route("/ajout_lieu", methods=['POST'])
@login_required
def inserer_lieu():
    id_lieu = get_prochain_id_lieu()

    nom_lieu = request.form.get('nom_lieu')
    jauge_lieu = request.form.get('jauge_lieu')
    coordonne_X = request.form.get('coordonne_X')
    coordonne_Y = request.form.get('coordonne_Y')

    insere_lieu(id_lieu, nom_lieu, jauge_lieu, coordonne_X, coordonne_Y)

    return redirect(url_for("home"))
