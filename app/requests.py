import base64
from app import db
from app.models import (Appartenir, Artiste, Billet, Concert, EtreStyle,
                     EtreType, Favoris, Groupe, Hebergement, Instrument,
                     Jouer, Lieu, OrganiserConcert, Possede, Reserver,
                     Style, SousStyle, Spectateur, Type, OrganiserEvent, Event)
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy import desc

def get_user_by_id(id):
    """
    Récupère un utilisateur par son ID.

    Args:
        id (int): L'ID de l'utilisateur à récupérer.

    Returns:
        dict: Un dictionnaire contenant les informations de l'utilisateur.
    """
    return Spectateur.query.filter_by(id_spectateur=id).first()

def get_user_by_email(email):
    """
    Récupère un utilisateur par son email.

    Args:
        email (str): L'email de l'utilisateur à récupérer.

    Returns:
        dict: Un dictionnaire contenant les informations de l'utilisateur.
    """
    return Spectateur.query.filter_by(email_spectateur=email).first()

def get_groupes():
    return Groupe.query.all()

def get_lieux():
    return Lieu.query.all()

def get_artistes():
    return Artiste.query.all()

def get_hebergement():
    return Hebergement.query.all()

def get_styles():
    return Style.query.all()

def get_instrument():
    return Instrument.query.all()

def filter_concerts(date_debut,date_fin, place):
    concert_lieu = Concert.query.filter_by(id_lieu=place).order_by("date_heure_concert").all()
    res = []
    date_debut = datetime.datetime.strptime(date_debut,"%Y-%m-%d")
    date_fin = datetime.datetime.strptime(date_fin,"%Y-%m-%d")
    for concert in concert_lieu:
        if concert.date_heure_concert >= date_debut and concert.date_heure_concert <= date_fin:
            res.append(concert)
    return res

def filter_concerts_date(date):
    concert_lieu = Concert.query.order_by("date_heure_concert").all()
    res = []
    for concert in concert_lieu:
        if concert.date_heure_concert >= date:
            res.append(concert)
    return res

def filter_events_date(date):
    event_lieu = Event.query.order_by("date_event").all()
    res = []
    for event in event_lieu:
        if event.date_event >= date:
            res.append(event)
    return res



def get_all_lieux():
    return Lieu.query.all()
    

def get_favoris(user):
    res = Favoris.query.filter_by(id_spectateur=user).all()
    groupes = []
    for favori in res:
        groupe = Groupe.query.get(favori.id_groupe)
        groupes.append(groupe)
    return groupes

    
def get_groupe_by_id(id):
    return Groupe.query.filter_by(id_groupe=id).first()

def get_style_by_id_groupe(id):
    res = EtreStyle.query.filter_by(id_groupe=id).first()
    return Style.query.get(res.id_style)

def get_sous_style_by_id(id):
    return SousStyle.query.filter_by(id_sous_style=id).all()

def get_artistes_by_id_groupe(id):
    res = Appartenir.query.filter_by(id_groupe=id).all()
    artistes = []
    for artiste in res:
        artistes.append(Artiste.query.get(artiste.id_artiste))
    return artistes

def ajouter_favoris(id_groupe, id_spectateur):
    favoris = Favoris(id_groupe=id_groupe, id_spectateur=id_spectateur)
    db.session.add(favoris)
    db.session.commit()
    
def supprimer_favoris(id_groupe, id_spectateur):
    favoris = Favoris.query.filter_by(id_groupe=id_groupe, id_spectateur=id_spectateur).first()
    db.session.delete(favoris)
    db.session.commit()
    
def est_favoris(id_groupe, id_spectateur):
    return Favoris.query.filter_by(id_groupe=id_groupe, id_spectateur=id_spectateur).first() is not None

def get_groupe_by_style(id_style):
    res = EtreStyle.query.filter_by(id_style=id_style).all()
    if len(res) >= 5:
        res = res[:4]
    groupes = []
    for groupe in res:
        groupes.append(Groupe.query.get(groupe.id_groupe))
    return groupes

def get_concert_by_id_groupe(id_groupe):
    res = OrganiserConcert.query.filter_by(id_groupe=id_groupe).all()
    concerts = []
    for concert in res:
        concerts.append(Concert.query.get(concert.id_concert))
    return concerts

def get_instrument_by_id_artiste(id_artiste):
    res= Jouer.query.filter_by(id_artiste=id_artiste).all()
    instrument= Instrument.query.get(res[0].id_instrument)
    return instrument

def get_event_by_id_groupe(id_groupe):
    res= OrganiserEvent.query.filter_by(id_groupe=id_groupe).all()
    events=[]
    for event in res:
        events.append(Event.query.get(event.id_event))
    return events

def get_lieu_by_id(id_lieu):
    return Lieu.query.filter_by(id_lieu=id_lieu).first()


def delete_groupe(groupe):
    fav= Favoris.query.filter_by(id_groupe=groupe.id_groupe).all()
    for f in fav:
        db.session.delete(f)
    appartient= Appartenir.query.filter_by(id_groupe=groupe.id_groupe).all()
    for a in appartient:
        db.session.delete(a)
    style= EtreStyle.query.filter_by(id_groupe=groupe.id_groupe).all()
    for s in style:
        db.session.delete(s)
    concert= OrganiserConcert.query.filter_by(id_groupe=groupe.id_groupe).all()
    for c in concert:
        db.session.delete(c)
    event= OrganiserEvent.query.filter_by(id_groupe=groupe.id_groupe).all()
    for e in event:
        db.session.delete(e)
    db.session.delete(groupe)
    db.session.commit()

def delete_concert(concert):
    billet= Billet.query.filter_by(id_concert=concert.id_concert).all()
    for b in billet:
        db.session.delete(b)
    reserver= Reserver.query.filter_by(id_concert=concert.id_concert).all()
    for r in reserver:
        db.session.delete(r)
    db.session.delete(concert)
    db.session.commit()

def get_groupes_by_nom(nom):
    return Groupe.query.filter(Groupe.nom_groupe.like('%'+nom+'%')).all()

def get_prochain_id_groupe():
    id_g = Groupe.query.order_by(desc(Groupe.id_groupe)).first().id_groupe
    return id_g + 1

def insere_groupe(id_groupe, nom_groupe, photo_groupe, description_groupe, insta_groupe, spotify_groupe, id_hebergement):
    groupe = Groupe(id_groupe=id_groupe, nom_groupe=nom_groupe, photo_groupe=photo_groupe, description_groupe=description_groupe, insta_groupe=insta_groupe, spotify_groupe=spotify_groupe, id_hebergement=id_hebergement)
    db.session.add(groupe)
    db.session.commit()

def get_prochain_id_artiste():
    id_a = Artiste.query.order_by(desc(Artiste.id_artiste)).first().id_artiste
    return id_a + 1

def insere_artiste(id_artiste, nom_artiste):
    artiste = Artiste(id_artiste=id_artiste, nom_artiste=nom_artiste)
    db.session.add(artiste)
    db.session.commit()

def insere_appartenir(id_artiste, id_groupe):
    appartenir = Appartenir(id_artiste=id_artiste, id_groupe=id_groupe)
    db.session.add(appartenir)
    db.session.commit()

def insere_etrestyle(id_style, id_groupe):
    etrestyle = EtreStyle(id_style=id_style, id_groupe=id_groupe)
    db.session.add(etrestyle)
    db.session.commit()

def get_groupe_by_id_concert(id):
    res = OrganiserConcert.query.filter_by(id_concert=id).first()
    return Groupe.query.get(res.id_groupe)

def get_concert_by_id(id):
    return Concert.query.filter_by(id_concert=id).first()

def get_types_billet():
    return Type.query.all()

def get_billets_by_id_spectateur(id):
    return Billet.query.filter_by(id_spectateur=id).all()

def get_concerts_by_id_billet_dates_lieu(id_billet, date1, date2, id_lieu):
    billet = Billet.query.get(id_billet)
    spectateur = Spectateur.query.get(billet.id_spectateur)
    reservations = Reserver.query.filter_by(id_spectateur=spectateur.id_spectateur).all()
    concerts = []
    date1 = datetime.datetime.combine(date1, datetime.datetime.min.time())
    date2 = datetime.datetime.combine(date2, datetime.datetime.min.time())
    for reservation in reservations:
        concert = Concert.query.filter_by(id_concert=reservation.id_concert).first()
        if date1 <= concert.date_heure_concert <= date2:
            concerts.append(concert)
    return concerts

def get_type_by_id_billet(id_billet):
    billet = Billet.query.get(id_billet)
    type = Type.query.get(billet.id_type)
    return type

def get_concerts_between_dates(date1, date2):
    concerts = Concert.query.filter(Concert.date_heure_concert >= date1, Concert.date_heure_concert <= date2).all()
    return concerts

def get_concerts_by_id_lieu_between_dates(id_lieu, date1, date2):
    concerts = get_concerts_between_dates(date1, date2)
    res = []
    for concert in concerts:
        if concert.id_lieu == id_lieu:
            res.append(concert)
    return res

def get_lieu_by_id_billet_and_dates(id_billet, date1, date2):
    lieu = None
    billet = Billet.query.get(id_billet)
    spectateur = Spectateur.query.get(billet.id_spectateur)
    reservations = Reserver.query.filter_by(id_spectateur=spectateur.id_spectateur).all()
    date1 = datetime.datetime.combine(date1, datetime.datetime.min.time())
    date2 = datetime.datetime.combine(date2, datetime.datetime.min.time())
    for reservation in reservations:
        concert = Concert.query.get(reservation.id_concert)
        if date1 <= concert.date_heure_concert <= date2:
            lieu = Lieu.query.get(concert.id_lieu)
    return lieu

def add_billet(date, id_type, id_spectateur):
    billet = Billet(date_billet=date, id_type=id_type, id_spectateur=id_spectateur)
    db.session.add(billet)
    db.session.commit()

def add_reservation(id_concert, id_spectateur):
    existe_reservation = Reserver.query.filter_by(id_concert=id_concert, id_spectateur=id_spectateur).first()
    if not existe_reservation:
        reservation = Reserver(id_concert=id_concert, id_spectateur=id_spectateur)
        db.session.add(reservation)
        db.session.commit()
        return True
    else:
        return False

def get_artistes():
    return Artiste.query.all()

def modif_groupe(id_groupe, nom_groupe, description_groupe, insta_groupe, spotify_groupe):
    Session = sessionmaker(bind=db.engine)
    session = Session()
    groupe = Groupe.query.get(int(id_groupe))
    groupe.nom_groupe = nom_groupe
    groupe.description_groupe = description_groupe
    groupe.insta_groupe = insta_groupe
    groupe.spotify_groupe = spotify_groupe
    session.commit()
    session.close()

def modif_concert(id_concert, nom_concert, tps_prepa_concert, date_heure_concert, duree_concert):
    Session = sessionmaker(bind=db.engine)
    session = Session()
    concert = get_concert_by_id(id_concert)
    concert.nom_concert = nom_concert
    concert.tps_prepa_concert = int(tps_prepa_concert)
    concert.date_heure_concert = date_heure_concert
    concert.duree_concert = int(duree_concert)
    session.commit()
    session.close()

def modif_event(id_event, date_event, nom_event):
    Session = sessionmaker(bind=db.engine)
    session = Session()
    event = Event.query.get(int(id_event))
    event.date_event = date_event
    event.nom_event = nom_event
    session.commit()
    session.close()
    
def get_hebergement():
    return Hebergement.query.all()

def get_prochain_id_instrument():
    id_i = Instrument.query.order_by(desc(Instrument.id_instrument)).first().id_instrument
    return id_i + 1

def insere_instrument(id_instrument, nom_instrument):
    instrument = Instrument(id_instrument, nom_instrument)
    db.session.add(instrument)
    db.session.commit()

def insere_jouer(id_artiste, id_instrument):
    jouer = Jouer(id_artiste=id_artiste, id_instrument=id_instrument)
    db.session.add(jouer)
    db.session.commit()
    
def get_prochain_id_hebergement():
    id_h = Hebergement.query.order_by(desc(Hebergement.id_hebergement)).first().id_hebergement
    return id_h + 1

def insere_hebergement(id_hebergement, nom_hebergement, adresse_hebergement):
    hebergement = Hebergement(id_hebergement, nom_hebergement, adresse_hebergement)
    db.session.add(hebergement)
    db.session.commit()

def get_prochain_id_concert():
    id_c = Concert.query.order_by(desc(Concert.id_concert)).first().id_concert
    return id_c + 1

def insere_concert(id_concert, nom_concert, tps_prepa_concert, date_heure_concert, duree_concert, id_lieu):
    concert = Concert(id_concert, nom_concert, tps_prepa_concert, date_heure_concert, duree_concert, id_lieu)
    db.session.add(concert)
    db.session.commit()
    
def get_event_by_id(id):
    return Event.query.filter_by(id_event=id).first()

def get_groupe_by_id_event(id):
    res = OrganiserEvent.query.filter_by(id_event=id).first()
    return Groupe.query.get(res.id_groupe)

def delete_event(event):
    organiser= OrganiserEvent.query.filter_by(id_event=event.id_event).all()
    for o in organiser:
        db.session.delete(o)
    db.session.delete(event)
    db.session.commit()

def get_prochain_id_event():
    id_e = Event.query.order_by(desc(Event.id_event)).first().id_event
    return id_e + 1

def insere_event(id_event, nom_event, date_event, id_lieu):
    event = Event(id_event, nom_event, date_event, id_lieu)
    db.session.add(event)
    db.session.commit()

def insere_organiser_event(id_groupe, id_event):
    organiser_event = OrganiserEvent(id_groupe, id_event)
    db.session.add(organiser_event)
    db.session.commit()