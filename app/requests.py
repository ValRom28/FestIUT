import base64
from app import db
from app.models import (Appartenir, Artiste, Billet, Concert, EtreStyle,
                     EtreType, Favoris, Groupe, Hebergement, Instrument,
                     Jouer, Lieu, OrganiserConcert, Possede, Reserver,
                     Style, SousStyle, Spectateur, Type, OrganiserEvent, Event)
import datetime

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
    print(res)
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

def get_groupe_by_id_concert(id):
    res = OrganiserConcert.query.filter_by(id_concert=id).first()
    return Groupe.query.get(res.id_groupe)

def get_concert_by_id(id):
    return Concert.query.filter_by(id_concert=id).first()

def get_types_billet():
    return Type.query.all()