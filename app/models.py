from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, LargeBinary, Boolean, DateTime
from app import db

Base = db.Model
metadata = Base.metadata

class Appartenir(Base):
    __tablename__ = 'APPARTENIR'
    id_artiste = Column(Integer, ForeignKey('ARTISTE.id_artiste'), primary_key=True)
    id_groupe = Column(Integer, ForeignKey('GROUPE.id_groupe'), primary_key=True)

    def __init__(self, id_artiste, id_groupe):
        self.id_artiste = id_artiste
        self.id_groupe = id_groupe

class Artiste(Base):
    __tablename__ = 'ARTISTE'
    id_artiste = Column(Integer, primary_key=True)
    nom_artiste = Column(String(42))
    
    def __init__(self, id_artiste, nom_artiste):
        self.nom_artiste = nom_artiste
        self.id_artiste = id_artiste

class Billet(Base):
    __tablename__ = 'BILLET'
    id_billet = Column(Integer, primary_key=True, autoincrement=True)
    date_billet = Column(Date)
    id_type = Column(Integer)
    id_spectateur = Column(Integer, ForeignKey('SPECTATEUR.id_spectateur'))

    def __init__(self, date_billet, id_type, id_spectateur):
        self.date_billet = date_billet
        self.id_type = id_type
        self.id_spectateur = id_spectateur

class Concert(Base):
    __tablename__ = 'CONCERT'
    id_concert = Column(Integer, primary_key=True)
    nom_concert = Column(String(42))
    tps_prepa_concert = Column(Integer)
    date_heure_concert = Column(DateTime)
    duree_concert = Column(Integer)
    id_lieu = Column(Integer, ForeignKey('LIEU.id_lieu'))

    def __init__(self, id_concert, nom_concert, tps_prepa_concert, date_heure_concert, duree_concert, id_lieu):
        self.id_concert = id_concert
        self.nom_concert = nom_concert
        self.tps_prepa_concert = tps_prepa_concert
        self.date_heure_concert = date_heure_concert
        self.duree_concert = duree_concert
        self.id_lieu = id_lieu

class EtreStyle(Base):
    __tablename__ = 'ETRESTYLE'
    id_style = Column(Integer, ForeignKey('STYLE.id_style'), primary_key=True)
    id_groupe = Column(Integer, ForeignKey('GROUPE.id_groupe'), primary_key=True)

    def __init__(self, id_style, id_groupe):
        self.id_style = id_style
        self.id_groupe = id_groupe

class EtreType(Base):
    __tablename__ = 'ETRETYPE'
    id_billet = Column(Integer, ForeignKey('BILLET.id_billet'), primary_key=True)
    id_type = Column(Integer, ForeignKey('TYPE.id_type'), primary_key=True)

    def __init__(self, id_billet, id_type):
        self.id_billet = id_billet
        self.id_type = id_type

class Favoris(Base):
    __tablename__ = 'FAVORIS'
    id_groupe = Column(Integer, ForeignKey('GROUPE.id_groupe'), primary_key=True)
    id_spectateur = Column(Integer, ForeignKey('SPECTATEUR.id_spectateur'), primary_key=True)

    def __init__(self, id_groupe, id_spectateur):
        self.id_groupe = id_groupe
        self.id_spectateur = id_spectateur

class Groupe(Base):
    __tablename__ = 'GROUPE'
    id_groupe = Column(Integer, primary_key=True)
    nom_groupe = Column(String(42))
    photo_groupe = Column(LargeBinary)
    description_groupe = Column(String(42))
    insta_groupe = Column(String(42))
    spotify_groupe = Column(String(42))
    id_hebergement = Column(Integer, ForeignKey('HEBERGEMENT.id_hebergement'))

    def __init__(self, id_groupe, nom_groupe, photo_groupe, description_groupe, insta_groupe, spotify_groupe, id_hebergement):
        self.id_groupe = id_groupe
        self.nom_groupe = nom_groupe
        self.photo_groupe = photo_groupe
        self.description_groupe = description_groupe
        self.insta_groupe = insta_groupe
        self.spotify_groupe = spotify_groupe
        self.id_hebergement = id_hebergement
    

class Hebergement(Base):
    __tablename__ = 'HEBERGEMENT'
    id_hebergement = Column(Integer, primary_key=True)
    nom_hebergement = Column(String(42))
    adresse_hebergement = Column(String(42))

    def __init__(self, id_hebergement, nom_hebergement, adresse_hebergement):
        self.id_hebergement = id_hebergement
        self.nom_hebergement = nom_hebergement
        self.adresse_hebergement = adresse_hebergement

class Instrument(Base):
    __tablename__ = 'INSTRUMENT'
    id_instrument = Column(Integer, primary_key=True)
    nom_instrument = Column(String(42))

    def __init__(self, id_instrument, nom_instrument):
        self.id_instrument = id_instrument
        self.nom_instrument = nom_instrument

class Jouer(Base):
    __tablename__ = 'JOUER'
    id_artiste = Column(Integer, ForeignKey('ARTISTE.id_artiste'), primary_key=True)
    id_instrument = Column(Integer, ForeignKey('INSTRUMENT.id_instrument'), primary_key=True)

    def __init__(self, id_artiste, id_instrument):
        self.id_artiste = id_artiste
        self.id_instrument = id_instrument

class Lieu(Base):
    __tablename__ = 'LIEU'
    id_lieu = Column(Integer, primary_key=True)
    nom_lieu = Column(String(42))
    jauge_lieu = Column(Integer)
    coordonne_X = Column(Float)
    coordonne_Y = Column(Float)

    def __init__(self, id_lieu, nom_lieu, jauge_lieu, coordonne_X, coordonne_Y):
        self.id_lieu = id_lieu
        self.nom_lieu = nom_lieu
        self.jauge_lieu = jauge_lieu
        self.coordonne_X = coordonne_X
        self.coordonne_Y = coordonne_Y

class OrganiserConcert(Base):
    __tablename__ = 'ORGANISERCONCERT'
    id_groupe = Column(Integer, ForeignKey('GROUPE.id_groupe'), primary_key=True)
    id_concert = Column(Integer, ForeignKey('CONCERT.id_concert'), primary_key=True)

    def __init__(self, id_groupe, id_concert):
        self.id_groupe = id_groupe
        self.id_concert = id_concert

class Possede(Base):
    __tablename__ = 'POSSEDE'
    id_style = Column(Integer, ForeignKey('STYLE.id_style'), primary_key=True)
    id_sous_style = Column(Integer, ForeignKey('SOUSSTYLE.id_sous_style'), primary_key=True)

    def __init__(self, id_style, id_sous_style):
        self.id_style = id_style
        self.id_sous_style = id_sous_style

class Reserver(Base):
    __tablename__ = 'RESERVER'
    id_concert = Column(Integer, ForeignKey('CONCERT.id_concert'), primary_key=True)
    id_spectateur = Column(Integer, ForeignKey('SPECTATEUR.id_spectateur'), primary_key=True)

    def __init__(self, id_concert, id_spectateur):
        self.id_concert = id_concert
        self.id_spectateur = id_spectateur

class Style(Base):
    __tablename__ = 'STYLE'
    id_style = Column(Integer, primary_key=True)
    nom_style = Column(String(42))

    def __init__(self, id_style, nom_style):
        self.id_style = id_style
        self.nom_style = nom_style

class SousStyle(Base):
    __tablename__ = 'SOUSSTYLE'
    id_sous_style = Column(Integer, primary_key=True)
    id_style = Column(Integer, ForeignKey('STYLE.id_style'))
    nom_sous_style = Column(String(42))

    def __init__(self, id_sous_style, id_style, nom_sous_style):
        self.id_sous_style = id_sous_style
        self.id_style = id_style
        self.nom_sous_style = nom_sous_style

class Spectateur(Base):
    __tablename__ = 'SPECTATEUR'
    id_spectateur = Column(Integer, primary_key=True)
    nom_spectateur = Column(String(42))
    prenom_spectateur = Column(String(42))
    mdp_spectateur = Column(String(42))
    email_spectateur = Column(String(42), unique=True)
    anniv_spectateur = Column(Date)
    photo_compte = Column(LargeBinary)
    admin=Column(Boolean)

    def __init__(self, nom_spectateur, mdp_spectateur, email_spectateur, id_spectateur=None, prenom_spectateur=None, anniv_spectateur=None, photo_compte=None, admin=False):
        if id_spectateur is not None:
            self.id_spectateur = id_spectateur
        else:
            self.id_spectateur = max([spectateur.id_spectateur for spectateur in Spectateur.query.all()]) + 1
        self.nom_spectateur = nom_spectateur
        self.prenom_spectateur = prenom_spectateur
        self.mdp_spectateur = mdp_spectateur
        self.email_spectateur = email_spectateur
        self.anniv_spectateur = anniv_spectateur
        self.photo_compte = photo_compte
        self.admin = admin
        
        
        
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id_spectateur
    
    def is_admin(self):
        return self.admin

class Type(Base):
    __tablename__ = 'TYPE'
    id_type = Column(Integer, primary_key=True)
    nb_jours = Column(Integer)
    nom_type = Column(String(42))
    prix = Column(Float)
    age_min = Column(Integer)
    age_max = Column(Integer)

    def __init__(self, id_type, nb_jours, nom_type, prix, age_min, age_max):
        self.id_type = id_type
        self.nb_jours = nb_jours
        self.nom_type = nom_type
        self.prix = prix
        self.age_min = age_min
        self.age_max = age_max

class Event(Base):
    __tablename__ = 'EVENT'
    id_event = Column(Integer, primary_key=True)
    nom_event = Column(String(42))
    date_event = Column(Date)
    id_lieu = Column(Integer, ForeignKey('LIEU.id_lieu'))

    def __init__(self, id_event, nom_event, date_event, id_lieu):
        self.id_event = id_event
        self.nom_event = nom_event
        self.date_event = date_event
        self.id_lieu = id_lieu

class OrganiserEvent(Base):
    __tablename__ = 'ORGANISEREVENT'
    id_groupe = Column(Integer, ForeignKey('GROUPE.id_groupe'), primary_key=True)
    id_event = Column(Integer, ForeignKey('EVENT.id_event'), primary_key=True)

    def __init__(self, id_groupe, id_event):
        self.id_groupe = id_groupe
        self.id_event = id_event