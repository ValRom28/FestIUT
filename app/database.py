from app import app, db
from sqlalchemy.orm import sessionmaker
from .models import (Appartenir, Artiste, Billet, Concert, EtreStyle,
                     EtreType, Favoris, Groupe, Hebergement, Instrument,
                     Jouer, Lieu, OrganiserConcert, Possede, Reserver,
                     Style, SousStyle, Spectateur, Type)

@app.cli.command('initdb')
def initdb():
    db.create_all()
    print('Base de données initialisée.')

    # Créer une session pour interagir avec la base de données
    Session = sessionmaker(bind=db.engine)
    session = Session()

    # Insertions pour la table ARTISTE
    artistes = [
        Artiste(id_artiste=1, nom_artiste='DJ Snake'),
        Artiste(id_artiste=2, nom_artiste='Louane'),
        Artiste(id_artiste=3, nom_artiste='Liam Sottier'),
        Artiste(id_artiste=4, nom_artiste='Adele'),
        Artiste(id_artiste=5, nom_artiste='Ed Sheeran'),
        Artiste(id_artiste=6, nom_artiste='Beyoncé'),
        Artiste(id_artiste=7, nom_artiste='Taylor Swift'),
        Artiste(id_artiste=8, nom_artiste='Bruno Mars'),
        Artiste(id_artiste=9, nom_artiste='Alicia Keys'),
        Artiste(id_artiste=10, nom_artiste='John Legend'),
    ]
    session.add_all(artistes)

    # Insertions pour la table HEBERGEMENT
    hebergements = [
        Hebergement(id_hebergement=1, nom_hebergement='Hôtel Luxe', addresse_hebergement='123 Rue Principale'),
        Hebergement(id_hebergement=2, nom_hebergement='Auberge Charme', addresse_hebergement='456 Avenue Centrale'),
        Hebergement(id_hebergement=3, nom_hebergement='Motel Repos', addresse_hebergement='789 Boulevard Tranquille'),
    ]
    session.add_all(hebergements)

    # Insertions pour la table GROUPE
    groupes = [
        Groupe(id_groupe=1, nom_groupe='Les Artistes Brillants', id_hebergement=1),
        Groupe(id_groupe=2, nom_groupe='Thibault et ses esclaves', id_hebergement=2),
        Groupe(id_groupe=3, nom_groupe='La Saint-Leger tout puissant', id_hebergement=3),
        Groupe(id_groupe=4, nom_groupe='IUTO', id_hebergement=1),
        Groupe(id_groupe=5, nom_groupe='SLR', id_hebergement=2),
        Groupe(id_groupe=6, nom_groupe='La Z compagnie', id_hebergement=3),
        Groupe(id_groupe=7, nom_groupe='Je fait toutou seul', id_hebergement=3),
    ]
    session.add_all(groupes)

    # Insertions pour la table LIEU
    lieux = [
        Lieu(id_lieu=1, nom_lieu='Stade Olympique', jauge_lieu=50000),
        Lieu(id_lieu=2, nom_lieu='Arena Music', jauge_lieu=10000),
        Lieu(id_lieu=3, nom_lieu='Théâtre Royal', jauge_lieu=1500),
    ]
    session.add_all(lieux)

    # Insertions pour la table CONCERT
    concerts = [
        Concert(id_concert=1, nom_concert='Concert d ouverture', tps_prepa_concert=30, date_heure_concert='2023-10-25 19:00:00', duree_concert=120, id_lieu=1),
        Concert(id_concert=2, nom_concert='Soirée Musicale', tps_prepa_concert=40, date_heure_concert='2023-11-05 20:00:00', duree_concert=90, id_lieu=2),
        Concert(id_concert=3, nom_concert='Symphonie en Soirée', tps_prepa_concert=25, date_heure_concert='2023-11-15 18:30:00', duree_concert=150, id_lieu=3),
    ]
    session.add_all(concerts)

    # Insertions pour la table SPECTATEUR
    spectateurs = [
        Spectateur(id_spectateur=1, nom_spectateur='Valentin', prenom_spectateur='Romanet', mot_passe_spectateur='mdpRomanet', email_spectateur='valentin@example.com', anniversaire_spectateur='2004-05-15'),
        Spectateur(id_spectateur=2, nom_spectateur='Hugo', prenom_spectateur='Sainson', mot_passe_spectateur='mdpSainson', email_spectateur='hugo@example.com', anniversaire_spectateur='2004-12-20'),
        Spectateur(id_spectateur=3, nom_spectateur='Thibault', prenom_spectateur='Saint-Leger', mot_passe_spectateur='mdpSaint', email_spectateur='thibault@example.com', anniversaire_spectateur='2004-17-06'),
        Spectateur(id_spectateur=4, nom_spectateur='Arthur', prenom_spectateur='Villet', mot_passe_spectateur='mdpVillet', email_spectateur='arthur@example.com', anniversaire_spectateur='2004-03-10'),
    ]
    session.add_all(spectateurs)

    # Insertions pour la table SOUSSTYLE
    sousstyles = [
        SousStyle(id_sous_style=1, id_style=1, nom_sous_style='Rock alternatif'),
        SousStyle(id_sous_style=2, id_style=1, nom_sous_style='Hard rock'),
        SousStyle(id_sous_style=3, id_style=2, nom_sous_style='Pop-rock'),
    ]
    session.add_all(sousstyles)

    # Insertions pour la table INSTRUMENT
    instruments = [
        Instrument(id_instrument=1, nom_instrument='Guitare'),
        Instrument(id_instrument=2, nom_instrument='Batterie'),
        Instrument(id_instrument=3, nom_instrument='Piano'),
    ]
    session.add_all(instruments)

    # Insertions pour la table JOUER
    jouer = [
        Jouer(id_artiste=1, id_instrument=1),
        Jouer(id_artiste=2, id_instrument=2),
        Jouer(id_artiste=3, id_instrument=3),
        Jouer(id_artiste=4, id_instrument=3),
        Jouer(id_artiste=5, id_instrument=1),
        Jouer(id_artiste=6, id_instrument=2),
        Jouer(id_artiste=7, id_instrument=1),
        Jouer(id_artiste=8, id_instrument=2),
        Jouer(id_artiste=9, id_instrument=3),
        Jouer(id_artiste=10, id_instrument=1),
    ]
    session.add_all(jouer)

    # Insertions pour la table POSSEDE
    possede = [
        Possede(id_style=1, id_sous_style=1),
        Possede(id_style=1, id_sous_style=2),
        Possede(id_style=2, id_sous_style=3),
    ]
    session.add_all(possede)

    # Insertions pour la table APPARTENIR
    appartenir = [
        Appartenir(id_artiste=1, id_groupe=1),
        Appartenir(id_artiste=2, id_groupe=2),
        Appartenir(id_artiste=3, id_groupe=3),
        Appartenir(id_artiste=4, id_groupe=4),
        Appartenir(id_artiste=5, id_groupe=5),
        Appartenir(id_artiste=6, id_groupe=6),
        Appartenir(id_artiste=7, id_groupe=7),
        Appartenir(id_artiste=8, id_groupe=7),
        Appartenir(id_artiste=9, id_groupe=7),
        Appartenir(id_artiste=10, id_groupe=7),
    ]
    session.add_all(appartenir)

    # Insertions pour la table ETRESTYLE
    etrestyle = [
        EtreStyle(id_style=1, id_groupe=1),
        EtreStyle(id_style=2, id_groupe=2),
        EtreStyle(id_style=3, id_groupe=3),
        EtreStyle(id_style=2, id_groupe=4),
        EtreStyle(id_style=1, id_groupe=5),
        EtreStyle(id_style=3, id_groupe=6),
        EtreStyle(id_style=2, id_groupe=7),
    ]
    session.add_all(etrestyle)

    # Insertions pour la table TYPE
    types = [
        Type(id_type=1, nb_jours=3, prix=50.0, age_min=18, age_max=60),
        Type(id_type=2, nb_jours=1, prix=25.0, age_min=16, age_max=45),
        Type(id_type=3, nb_jours=2, prix=35.0, age_min=21, age_max=70),
    ]
    session.add_all(types)

    # Insertions pour la table BILLET
    billets = [
        Billet(id_billet=1, date_billet='2023-10-15', id_type=1, id_spectateur=1),
        Billet(id_billet=2, date_billet='2023-11-02', id_type=2, id_spectateur=2),
        Billet(id_billet=3, date_billet='2023-11-20', id_type=3, id_spectateur=3),
    ]
    session.add_all(billets)

     # Insertions pour la table ETRETYPE
    etretype = [
        EtreType(id_billet=1, id_type=1),
        EtreType(id_billet=2, id_type=2),
        EtreType(id_billet=3, id_type=3),
    ]
    session.add_all(etretype)

    # Insertions pour la table ORGANISERCONCERT
    organiserconcert = [
        OrganiserConcert(id_groupe=1, id_concert=1),
        OrganiserConcert(id_groupe=2, id_concert=2),
        OrganiserConcert(id_groupe=3, id_concert=3),
    ]
    session.add_all(organiserconcert)

    # Insertions pour la table FAVORIS
    favoris = [
        Favoris(id_groupe=1, id_spectateur=1),
        Favoris(id_groupe=2, id_spectateur=2),
        Favoris(id_groupe=3, id_spectateur=3),
    ]
    session.add_all(favoris)

    # Insertions pour la table RESERVER
    reserver = [
        Reserver(id_concert=1, id_spectateur=1),
        Reserver(id_concert=2, id_spectateur=2),
        Reserver(id_concert=3, id_spectateur=3),
    ]
    session.add_all(reserver)

    style = [
        Style(id_style=1, nom_style='Rock'),
        Style(id_style=2, nom_style='Pop'),
        Style(id_style=3, nom_style='Jazz'),
    ]
    session.add_all(style)

    # Valider les modifications dans la base de données
    session.commit()
    print('Insertions terminées.')
