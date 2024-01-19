import base64
from app import app, db
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .models import (Appartenir, Artiste, Billet, Concert, EtreStyle,
                    EtreType, Favoris, Groupe, Hebergement, Instrument,
                    Jouer, Lieu, OrganiserConcert, Possede, Reserver,
                    Style, SousStyle, Spectateur, Type, Event, OrganiserEvent)

@app.cli.command('initdb')
def initdb():
    db.drop_all()
    db.create_all()
    print('Base de données initialisée.')

    # Créer une session pour interagir avec la base de données
    Session = sessionmaker(bind=db.engine)
    session = Session()

    # Insertions pour la table ARTISTE
    artistes = [
        Artiste(id_artiste=1, nom_artiste='DJ Snake'),
        Artiste(id_artiste=2, nom_artiste='David Guetta'),
        #chanteurs des rollings stones
        Artiste(id_artiste=3, nom_artiste='Mick Jagger'),
        Artiste(id_artiste=4, nom_artiste='Keith Richards'),
        Artiste(id_artiste=5, nom_artiste='Charlie Watts'),
        Artiste(id_artiste=6, nom_artiste='Ronnie Wood'),
        #chanteurs des beatles
        Artiste(id_artiste=7, nom_artiste='John Lennon'),
        Artiste(id_artiste=8, nom_artiste='Paul McCartney'),
        Artiste(id_artiste=9, nom_artiste='George Harrison'),
        Artiste(id_artiste=10, nom_artiste='Ringo Starr'),
        #chanteurs de queen
        Artiste(id_artiste=11, nom_artiste='Freddie Mercury'),
        Artiste(id_artiste=12, nom_artiste='Brian May'),
        Artiste(id_artiste=13, nom_artiste='Roger Taylor'),
        Artiste(id_artiste=14, nom_artiste='John Deacon'),
        #chanteurs de AC/DC
        Artiste(id_artiste=15, nom_artiste='Angus Young'),
        Artiste(id_artiste=16, nom_artiste='Brian Johnson'),
        Artiste(id_artiste=17, nom_artiste='Malcolm Young'),
        Artiste(id_artiste=18, nom_artiste='Cliff Williams'),
    ]
    session.add_all(artistes)

    # Insertions pour la table HEBERGEMENT
    hebergements = [
        Hebergement(id_hebergement=1, nom_hebergement='Hôtel Luxe', adresse_hebergement='123 Rue Principale', jauge_hebergement=8),
        Hebergement(id_hebergement=2, nom_hebergement='Auberge Charme', adresse_hebergement='456 Avenue Centrale', jauge_hebergement=30),
        Hebergement(id_hebergement=3, nom_hebergement='Motel Repos', adresse_hebergement='789 Boulevard Tranquille', jauge_hebergement=15),
        Hebergement(id_hebergement=4, nom_hebergement='Hôtel de la Marée', adresse_hebergement='457 Avenue Charles de Gaulle', jauge_hebergement=1)
    ]
    session.add_all(hebergements)

    # Insertions pour la table GROUPE
    bytes_img = open('app/static/img/logo.png', 'rb').read()
    groupes = [
        Groupe(id_groupe=1, nom_groupe='The Rolling Stones', id_hebergement=1,
            photo_groupe=open('app/static/img/RollingStones.png', 'rb').read(), 
            description_groupe='Célèbre groupe de rock', 
            insta_groupe='https://www.instagram.com/therollingstones/', spotify_groupe='https://open.spotify.com/intl-fr/artist/22bE4uQ6baNwSHPVcDxLCe'),
        Groupe(id_groupe=2, nom_groupe='The Beatles', id_hebergement=1,
            photo_groupe=open('app/static/img/Beatles.jpg', 'rb').read(), 
            description_groupe='Célèbre groupe de pop', 
            insta_groupe='https://www.instagram.com/thebeatles/', spotify_groupe='https://open.spotify.com/intl-fr/artist/3WrFJ7ztbogyGnTHbHJFl2'),
        Groupe(id_groupe=3, nom_groupe='Queen', id_hebergement=3,
            photo_groupe=open('app/static/img/Queen.jpg', 'rb').read(), 
            description_groupe='Groupe de rock mythique avec le Célèbre Freddie Mercury', 
            insta_groupe='https://www.instagram.com/officialqueenmusic/', spotify_groupe='https://open.spotify.com/intl-fr/artist/1dfeR4HaWDbWqFHLkxsg1d'),
        Groupe(id_groupe=4, nom_groupe='AC/DC', id_hebergement=1,
            photo_groupe=open('app/static/img/ACDC.png', 'rb').read(), 
            description_groupe='Célèbre groupe de rock', 
            insta_groupe='https://www.instagram.com/acdc/', spotify_groupe='https://open.spotify.com/intl-fr/artist/711MCceyCBcFnzjGY4Q7Un'),
        Groupe(id_groupe=5, nom_groupe='Dj Snake', id_hebergement=2,
            photo_groupe=open('app/static/img/DJSnake.jpg', 'rb').read(), 
            description_groupe='Célèbre DJ Francais', 
            insta_groupe='https://www.instagram.com/djsnake/', spotify_groupe='https://open.spotify.com/intl-fr/artist/540vIaP2JwjQb9dm3aArA4'),
        Groupe(id_groupe=6, nom_groupe='David Guetta', id_hebergement=2,
            photo_groupe=open('app/static/img/DavidGuetta.jpg', 'rb').read(), 
            description_groupe='Célèbre DJ Francais', 
            insta_groupe='https://www.instagram.com/davidguetta/', spotify_groupe='https://open.spotify.com/intl-fr/artist/1Cs0zKBU1kc0i8ypK3B9ai'),
        Groupe(id_groupe=7, nom_groupe='Mick Jagger', id_hebergement=2,
            photo_groupe=open('app/static/img/noice.gif', 'rb').read(), 
            description_groupe='Célèbre chanteur des Rolling Stones', 
            insta_groupe='https://www.instagram.com/mickjagger/', spotify_groupe='https://open.spotify.com/intl-fr/artist/22bE4uQ6baNwSHPVcDxLCe'),
        Groupe(id_groupe=8, nom_groupe='Keith Richards', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre guitariste des Rolling Stones', 
            insta_groupe='https://www.instagram.com/officialkeef/', spotify_groupe='https://open.spotify.com/intl-fr/artist/22bE4uQ6baNwSHPVcDxLCe'),
        Groupe(id_groupe=9, nom_groupe='Charlie Watts', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre batteur des Rolling Stones', 
            insta_groupe='https://www.instagram.com/charliewattsofficial/', spotify_groupe='https://open.spotify.com/intl-fr/artist/22bE4uQ6baNwSHPVcDxLCe'),
        Groupe(id_groupe=10, nom_groupe='Ronnie Wood', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre guitariste des Rolling Stones', 
            insta_groupe='https://www.instagram.com/ronniewood/', spotify_groupe='https://open.spotify.com/intl-fr/artist/22bE4uQ6baNwSHPVcDxLCe'),
        Groupe(id_groupe=11, nom_groupe='John Lennon', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre chanteur des Beatles', 
            insta_groupe='https://www.instagram.com/johnlennonofficial/', spotify_groupe='https://open.spotify.com/intl-fr/artist/3WrFJ7ztbogyGnTHbHJFl2'),
        Groupe(id_groupe=12, nom_groupe='Paul McCartney', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre bassiste des Beatles', 
            insta_groupe='https://www.instagram.com/paulmccartney/', spotify_groupe='https://open.spotify.com/intl-fr/artist/3WrFJ7ztbogyGnTHbHJFl2'),
        Groupe(id_groupe=13, nom_groupe='George Harrison', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre guitariste des Beatles', 
            insta_groupe='https://www.instagram.com/georgeharrisonofficial/', spotify_groupe='https://open.spotify.com/intl-fr/artist/3WrFJ7ztbogyGnTHbHJFl2'),
        Groupe(id_groupe=14, nom_groupe='Ringo Starr', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre batteur des Beatles', 
            insta_groupe='https://www.instagram.com/ringostarrmusic/', spotify_groupe='https://open.spotify.com/intl-fr/artist/3WrFJ7ztbogyGnTHbHJFl2'),
        Groupe(id_groupe=15, nom_groupe='Freddie Mercury', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre chanteur de Queen', 
            insta_groupe='https://www.instagram.com/freddiemercury/', spotify_groupe='https://open.spotify.com/intl-fr/artist/1dfeR4HaWDbWqFHLkxsg1d'),
        Groupe(id_groupe=16, nom_groupe='Brian May', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre guitariste de Queen', 
            insta_groupe='https://www.instagram.com/brianmayforreal/', spotify_groupe='https://open.spotify.com/intl-fr/artist/1dfeR4HaWDbWqFHLkxsg1d'),
        Groupe(id_groupe=17, nom_groupe='Roger Taylor', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre batteur de Queen', 
            insta_groupe='https://www.instagram.com/rogertaylorofficial/', spotify_groupe='https://open.spotify.com/intl-fr/artist/1dfeR4HaWDbWqFHLkxsg1d'),
        Groupe(id_groupe=18, nom_groupe='John Deacon', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre bassiste de Queen', 
            insta_groupe='https://www.instagram.com/johndeaconofficial/', spotify_groupe='https://open.spotify.com/intl-fr/artist/1dfeR4HaWDbWqFHLkxsg1d'),
        Groupe(id_groupe=19, nom_groupe='Angus Young', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre guitariste de AC/DC', 
            insta_groupe='https://www.instagram.com/acdc/', spotify_groupe='https://open.spotify.com/intl-fr/artist/711MCceyCBcFnzjGY4Q7Un'),
        Groupe(id_groupe=20, nom_groupe='Brian Johnson', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre chanteur de AC/DC', 
            insta_groupe='https://www.instagram.com/acdc/', spotify_groupe='https://open.spotify.com/intl-fr/artist/711MCceyCBcFnzjGY4Q7Un'),
        Groupe(id_groupe=21, nom_groupe='Malcolm Young', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre guitariste de AC/DC', 
            insta_groupe='https://www.instagram.com/acdc/', spotify_groupe='https://open.spotify.com/intl-fr/artist/711MCceyCBcFnzjGY4Q7Un'),
        Groupe(id_groupe=22, nom_groupe='Cliff Williams', id_hebergement=2,
            photo_groupe=open('app/static/img/artiste.png', 'rb').read(), 
            description_groupe='Célèbre bassiste de AC/DC', 
            insta_groupe='https://www.instagram.com/acdc/', spotify_groupe='https://open.spotify.com/intl-fr/artist/711MCceyCBcFnzjGY4Q7Un'),
    ]
    session.add_all(groupes)

    # Insertions pour la table LIEU
    lieux = [
        Lieu(id_lieu=1, nom_lieu='Stade de France', jauge_lieu=50000, coordonne_X = 10, coordonne_Y = 15),
        Lieu(id_lieu=2, nom_lieu='Stade Olympique', jauge_lieu=80000, coordonne_X = 12, coordonne_Y = 13),
        Lieu(id_lieu=3, nom_lieu='Stade de Lyon', jauge_lieu=60000, coordonne_X = 20, coordonne_Y = 23),
        Lieu(id_lieu=4, nom_lieu='Stade de Marseille', jauge_lieu=70000, coordonne_X = 25, coordonne_Y = 20),
    ]
    session.add_all(lieux)

    # Insertions pour la table CONCERT
    concerts = [
        Concert(id_concert=1, nom_concert='Concert d\'ouverture', tps_prepa_concert=30, 
                date_heure_concert=datetime.strptime('2024-01-20 19:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=180, id_lieu=1),
        Concert(id_concert=2, nom_concert='Concert de cloture', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-28 23:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=120, id_lieu=2),
        Concert(id_concert=3, nom_concert='Concert de rock', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-25 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=100, id_lieu=3),
        Concert(id_concert=4, nom_concert='Concert de pop', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-22 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=150, id_lieu=3),
        Concert(id_concert=5, nom_concert='Concert de jazz', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-23 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=120, id_lieu=3),
        Concert(id_concert=6, nom_concert='Concert de metal', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-24 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=100, id_lieu=2),
        Concert(id_concert=7, nom_concert='Concert d\'électro', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-26 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=150, id_lieu=3),
        Concert(id_concert=8, nom_concert='Concert de rap', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-27 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=120, id_lieu=1),
        Concert(id_concert=9, nom_concert='Concert Familiale', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-21 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=100, id_lieu=3),
        Concert(id_concert=10, nom_concert='Concert de classique', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-29 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=150, id_lieu=2),
        Concert(id_concert=11, nom_concert='Concert de rock', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-21 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=100, id_lieu=1),
        Concert(id_concert=12, nom_concert='Concert de pop', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-24 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=150, id_lieu=2),
        Concert(id_concert=13, nom_concert='Concert de jazz', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-25 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=120, id_lieu=1),
        Concert(id_concert=14, nom_concert='Concert de metal', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-22 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=100, id_lieu=3),
        Concert(id_concert=15, nom_concert='Concert d\'électro', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-23 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=150, id_lieu=2),
        Concert(id_concert=16, nom_concert='Concert de rap', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-26 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=120, id_lieu=1),
        Concert(id_concert=17, nom_concert='Concert Familiale', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-26 15:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=100, id_lieu=3),
        Concert(id_concert=18, nom_concert='Concert de classique', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-23 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=150, id_lieu=2),
        Concert(id_concert=19, nom_concert='Concert de rock', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-21 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=100, id_lieu=1),
        Concert(id_concert=20, nom_concert='Concert de pop', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-24 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=150, id_lieu=2),
        Concert(id_concert=21, nom_concert='Concert de jazz', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-25 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=120, id_lieu=1),
        Concert(id_concert=22, nom_concert='Concert de metal', tps_prepa_concert=30,
                date_heure_concert=datetime.strptime('2024-01-22 21:00:00', '%Y-%m-%d %H:%M:%S'), 
                duree_concert=100, id_lieu=3),
        ]
    session.add_all(concerts)

    # Insertions pour la table SPECTATEUR
    spectateurs = [
        Spectateur(id_spectateur=1, nom_spectateur='Valentin', prenom_spectateur='Romanet', 
                    mdp_spectateur='v', email_spectateur='v',
                    anniv_spectateur=datetime.strptime('1973-05-15', '%Y-%m-%d').date(), photo_compte=None, admin=True),
        Spectateur(id_spectateur=2, nom_spectateur='Hugo', prenom_spectateur='Sainson', 
                    mdp_spectateur='h', email_spectateur='h', 
                    anniv_spectateur=datetime.strptime('2001-09-11', '%Y-%m-%d').date(), photo_compte=None, admin=False),
        Spectateur(id_spectateur=3, nom_spectateur='Thibault', prenom_spectateur='Saint-Leger', 
                    mdp_spectateur='t', email_spectateur='t', 
                    anniv_spectateur=datetime.strptime('1918-11-11', '%Y-%m-%d').date(), photo_compte=None, admin=False),
        Spectateur(id_spectateur=4, nom_spectateur='Arthur', prenom_spectateur='Villet', 
                    mdp_spectateur='mdpVillet', email_spectateur='arthur@example.com',
                        anniv_spectateur=datetime.strptime('2004-03-10', '%Y-%m-%d').date(), photo_compte=None, admin=True),
        Spectateur(id_spectateur=5, nom_spectateur='a', prenom_spectateur='a', 
                    mdp_spectateur='a', email_spectateur='a',
                        anniv_spectateur=datetime.strptime('2004-03-10', '%Y-%m-%d').date(), photo_compte=None, admin=True),
        Spectateur(id_spectateur=6, nom_spectateur='b', prenom_spectateur='b', 
                    mdp_spectateur='b', email_spectateur='b',
                        anniv_spectateur=datetime.strptime('2004-03-10', '%Y-%m-%d').date(), photo_compte=None, admin=True),
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
        Instrument(id_instrument=4, nom_instrument='Basse'),
        Instrument(id_instrument=5, nom_instrument='Voix'),
    ]
    session.add_all(instruments)

    # Insertions pour la table JOUER
    jouer = [
        Jouer(id_artiste=1, id_instrument=1),
        Jouer(id_artiste=2, id_instrument=2),
        Jouer(id_artiste=3, id_instrument=5),
        Jouer(id_artiste=4, id_instrument=1),
        Jouer(id_artiste=5, id_instrument=2),
        Jouer(id_artiste=6, id_instrument=4),
        Jouer(id_artiste=7, id_instrument=1),
        Jouer(id_artiste=8, id_instrument=3),
        Jouer(id_artiste=9, id_instrument=4),
        Jouer(id_artiste=10, id_instrument=2),
        Jouer(id_artiste=11, id_instrument=5),
        Jouer(id_artiste=12, id_instrument=1),
        Jouer(id_artiste=13, id_instrument=2),
        Jouer(id_artiste=14, id_instrument=4),
        Jouer(id_artiste=15, id_instrument=1),
        Jouer(id_artiste=16, id_instrument=2),
        Jouer(id_artiste=17, id_instrument=4),
        Jouer(id_artiste=18, id_instrument=3),
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
        Appartenir(id_groupe=5, id_artiste=1),
        Appartenir(id_groupe=6, id_artiste=2),
        Appartenir(id_groupe=1, id_artiste=3),
        Appartenir(id_groupe=1, id_artiste=4),
        Appartenir(id_groupe=1, id_artiste=5),
        Appartenir(id_groupe=1, id_artiste=6),
        Appartenir(id_groupe=2, id_artiste=7),
        Appartenir(id_groupe=2, id_artiste=8),
        Appartenir(id_groupe=2, id_artiste=9),
        Appartenir(id_groupe=2, id_artiste=10),
        Appartenir(id_groupe=3, id_artiste=11),
        Appartenir(id_groupe=3, id_artiste=12),
        Appartenir(id_groupe=3, id_artiste=13),
        Appartenir(id_groupe=3, id_artiste=14),
        Appartenir(id_groupe=4, id_artiste=15),
        Appartenir(id_groupe=4, id_artiste=16),
        Appartenir(id_groupe=4, id_artiste=17),
        Appartenir(id_groupe=4, id_artiste=18),
        Appartenir(id_groupe=7, id_artiste=3),
        Appartenir(id_groupe=8, id_artiste=4),
        Appartenir(id_groupe=9, id_artiste=5),
        Appartenir(id_groupe=10, id_artiste=6),
        Appartenir(id_groupe=11, id_artiste=7),
        Appartenir(id_groupe=12, id_artiste=8),
        Appartenir(id_groupe=13, id_artiste=9),
        Appartenir(id_groupe=14, id_artiste=10),
        Appartenir(id_groupe=15, id_artiste=11),
        Appartenir(id_groupe=16, id_artiste=12),
        Appartenir(id_groupe=17, id_artiste=13),
        Appartenir(id_groupe=18, id_artiste=14),
        Appartenir(id_groupe=19, id_artiste=15),
        Appartenir(id_groupe=20, id_artiste=16),
        Appartenir(id_groupe=21, id_artiste=17),
        Appartenir(id_groupe=22, id_artiste=18),
    ]
    session.add_all(appartenir)

    # Insertions pour la table ETRESTYLE
    etrestyle = [
        EtreStyle(id_groupe=1, id_style=1),
        EtreStyle(id_groupe=2, id_style=2),
        EtreStyle(id_groupe=3, id_style=3),
        EtreStyle(id_groupe=4, id_style=1),
        EtreStyle(id_groupe=5, id_style=2),
        EtreStyle(id_groupe=6, id_style=3),
        EtreStyle(id_groupe=7, id_style=1),
        EtreStyle(id_groupe=8, id_style=2),
        EtreStyle(id_groupe=9, id_style=3),
        EtreStyle(id_groupe=10, id_style=1),
        EtreStyle(id_groupe=11, id_style=2),
        EtreStyle(id_groupe=12, id_style=3),
        EtreStyle(id_groupe=13, id_style=1),
        EtreStyle(id_groupe=14, id_style=2),
        EtreStyle(id_groupe=15, id_style=3),
        EtreStyle(id_groupe=16, id_style=1),
        EtreStyle(id_groupe=17, id_style=2),
        EtreStyle(id_groupe=18, id_style=3),
        EtreStyle(id_groupe=19, id_style=1),
        EtreStyle(id_groupe=20, id_style=2),
        EtreStyle(id_groupe=21, id_style=3),
        EtreStyle(id_groupe=22, id_style=1),
    ]
    session.add_all(etrestyle)

    # Insertions pour la table TYPE
    types = [
        Type(id_type=1, nb_jours=1, nom_type='Pass 1 jour', prix=30.0, age_min=25, age_max=60),
        Type(id_type=2, nb_jours=2, nom_type='Pass 2 jours', prix=60.0, age_min=25, age_max=60),
        Type(id_type=3, nb_jours=5, nom_type='Pass semaine', prix=150.0, age_min=25, age_max=60),
        Type(id_type=4, nb_jours=1, nom_type='Pass 1 jour jeunes', prix=20.0, age_min=18, age_max=25),
        Type(id_type=5, nb_jours=2, nom_type='Pass 2 jours jeunes', prix=40.0, age_min=18, age_max=25),
        Type(id_type=6, nb_jours=5, nom_type='Pass semaine jeunes', prix=100.0, age_min=18, age_max=25),
        Type(id_type=7, nb_jours=1, nom_type='Pass 1 jour enfant', prix=10.0, age_min=0, age_max=18),
        Type(id_type=8, nb_jours=2, nom_type='Pass 2 jours enfant', prix=20.0, age_min=0, age_max=18),
        Type(id_type=9, nb_jours=5, nom_type='Pass semaine enfant', prix=50.0, age_min=0, age_max=18),
        Type(id_type=10, nb_jours=1, nom_type='Pass 1 jour senior', prix=20.0, age_min=60, age_max=100),
        Type(id_type=11, nb_jours=2, nom_type='Pass 2 jours senior', prix=40.0, age_min=60, age_max=100),
        Type(id_type=12, nb_jours=5, nom_type='Pass semaine senior', prix=100.0, age_min=60, age_max=100)
    ]
    session.add_all(types)

    # Insertions pour la table ORGANISERCONCERT
    organiserconcert = [
        OrganiserConcert(id_groupe=1, id_concert=1),
        OrganiserConcert(id_groupe=2, id_concert=2),
        OrganiserConcert(id_groupe=3, id_concert=3),
        OrganiserConcert(id_groupe=4, id_concert=4),
        OrganiserConcert(id_groupe=5, id_concert=5),
        OrganiserConcert(id_groupe=6, id_concert=6),
        OrganiserConcert(id_groupe=7, id_concert=7),
        OrganiserConcert(id_groupe=8, id_concert=8),
        OrganiserConcert(id_groupe=9, id_concert=9),
        OrganiserConcert(id_groupe=10, id_concert=10),
        OrganiserConcert(id_groupe=11, id_concert=11),
        OrganiserConcert(id_groupe=5, id_concert=12),
        OrganiserConcert(id_groupe=5, id_concert=13),
        OrganiserConcert(id_groupe=5, id_concert=14),
        OrganiserConcert(id_groupe=5, id_concert=15),
        OrganiserConcert(id_groupe=5, id_concert=16),
        OrganiserConcert(id_groupe=1, id_concert=17),
        OrganiserConcert(id_groupe=1, id_concert=18),
        OrganiserConcert(id_groupe=1, id_concert=19),
        OrganiserConcert(id_groupe=2, id_concert=20),
        OrganiserConcert(id_groupe=2, id_concert=21),
        OrganiserConcert(id_groupe=22, id_concert=22),

    ]
    session.add_all(organiserconcert)

    # Insertions pour la table FAVORIS
    favoris = [
        Favoris(id_spectateur=1, id_groupe=1),
        Favoris(id_spectateur=2, id_groupe=2),
        Favoris(id_spectateur=3, id_groupe=3),
        Favoris(id_spectateur=4, id_groupe=4),
        Favoris(id_spectateur=5, id_groupe=5),
        Favoris(id_spectateur=6, id_groupe=6),
    ]
    session.add_all(favoris)

    # Insertions pour la table RESERVER
    reserver = [
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

    event= [
        Event(id_event=1, nom_event='Biere pong', date_event=datetime.strptime('2024-01-22', '%Y-%m-%d').date(), id_lieu=1),
        Event(id_event=2, nom_event='Strip poker', date_event=datetime.strptime('2024-01-20', '%Y-%m-%d').date(), id_lieu=2),
        Event(id_event=3, nom_event='Danse bretonne', date_event=datetime.strptime('2024-01-21', '%Y-%m-%d').date(), id_lieu=3),
        Event(id_event=4, nom_event='Concours de mangeur', date_event=datetime.strptime('2024-01-23', '%Y-%m-%d').date(), id_lieu=3),
        Event(id_event=5, nom_event='Distribution de Tshirts', date_event=datetime.strptime('2024-01-23', '%Y-%m-%d').date(), id_lieu=2),
        Event(id_event=6, nom_event='Concours de danse', date_event=datetime.strptime('2024-01-25', '%Y-%m-%d').date(), id_lieu=1),
        Event(id_event=7, nom_event='Concours de chant', date_event=datetime.strptime('2024-01-26', '%Y-%m-%d').date(), id_lieu=1),
        Event(id_event=8, nom_event='Concours de danse', date_event=datetime.strptime('2024-01-22', '%Y-%m-%d').date(), id_lieu=2),
        Event(id_event=9, nom_event='Concours de chant', date_event=datetime.strptime('2024-01-24', '%Y-%m-%d').date(), id_lieu=3),

    ]
    session.add_all(event)

    organiserevent = [
        OrganiserEvent(id_groupe=1, id_event=1),
        OrganiserEvent(id_groupe=2, id_event=2),
        OrganiserEvent(id_groupe=3, id_event=3),
        OrganiserEvent(id_groupe=4, id_event=4),
        OrganiserEvent(id_groupe=5, id_event=5),
        OrganiserEvent(id_groupe=6, id_event=6),
        OrganiserEvent(id_groupe=1, id_event=7),
        OrganiserEvent(id_groupe=2, id_event=8),
        OrganiserEvent(id_groupe=3, id_event=9),
    ]
    session.add_all(organiserevent)

    # Valider les modifications dans la base de données
    session.commit()

    # Décrémentation de la jauge des hébergements
    Hebergement.query.filter_by(id_hebergement=1).first().jauge_hebergement = Hebergement.query.filter_by(id_hebergement=1).first().jauge_hebergement - 2
    Hebergement.query.filter_by(id_hebergement=2).first().jauge_hebergement = Hebergement.query.filter_by(id_hebergement=2).first().jauge_hebergement - 18
    Hebergement.query.filter_by(id_hebergement=3).first().jauge_hebergement = Hebergement.query.filter_by(id_hebergement=3).first().jauge_hebergement - 1
    db.session.commit()
    print('Insertions terminées.')

