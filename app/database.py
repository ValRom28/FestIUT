from app import app, db
from sqlalchemy.orm import sessionmaker
from .models import (Appartenir, Artiste, Billet, Concert, EtreStyle,
                     EtreType, Favoris, Groupe, Hebergement, Instrument,
                     Jouer, Lieu, OrganiserConcert, Possede, Reserver,
                     Style, SousStyle, Spectateur, Type)

@app.cli.command('initdb')
def initdb():
    db.create_all()
    print('Initialized the database.')