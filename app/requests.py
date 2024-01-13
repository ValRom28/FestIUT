from app import db
from app.models import (Appartenir, Artiste, Billet, Concert, EtreStyle,
                     EtreType, Favoris, Groupe, Hebergement, Instrument,
                     Jouer, Lieu, OrganiserConcert, Possede, Reserver,
                     Style, SousStyle, Spectateur, Type)

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

def get_favoris(user):
    res = Favoris.query.filter_by(id_spectateur=user).all()
    groupes = []
    for favori in res:
        groupe = Groupe.query.get(favori.id_groupe)
        groupes.append(groupe)
    return groupes

    
def get_groupes_by_id(id):
    return Groupe.query.filter_by(id_groupe=id).all()

def get_style_by_id(id):
    return Style.query.filter_by(id_style=id).all()

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