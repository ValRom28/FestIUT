-- Insertions pour la table ARTISTE
INSERT INTO ARTISTE (idArtiste, nomArtiste) VALUES (1, 'DJ Snake');
INSERT INTO ARTISTE (idArtiste, nomArtiste) VALUES (2, 'Louane');
INSERT INTO ARTISTE (idArtiste, nomArtiste) VALUES (3, 'Liam Sottier');

-- Insertions pour la table HEBERGEMENT
INSERT INTO HEBERGEMENT (idHebergement, nomHebergement, addresseHebergement) VALUES (1, 'Hôtel Luxe', '123 Rue Principale');
INSERT INTO HEBERGEMENT (idHebergement, nomHebergement, addresseHebergement) VALUES (2, 'Auberge Charme', '456 Avenue Centrale');
INSERT INTO HEBERGEMENT (idHebergement, nomHebergement, addresseHebergement) VALUES (3, 'Motel Repos', '789 Boulevard Tranquille');

-- Insertions pour la table GROUPE
INSERT INTO GROUPE (idGroupe, nomGroupe, idHebergement) VALUES (1, 'Les Artistes Brillants', 1);
INSERT INTO GROUPE (idGroupe, nomGroupe, idHebergement) VALUES (2, 'Ensemble Harmonie', 2);
INSERT INTO GROUPE (idGroupe, nomGroupe, idHebergement) VALUES (3, 'Les Mélodies Divines', 3);

-- Insertions pour la table LIEU
INSERT INTO LIEU (idLieu, nomLieu, jaugeLieu) VALUES (1, 'Stade Olympique', 50000);
INSERT INTO LIEU (idLieu, nomLieu, jaugeLieu) VALUES (2, 'Arena Music', 10000);
INSERT INTO LIEU (idLieu, nomLieu, jaugeLieu) VALUES (3, 'Théâtre Royal', 1500);

-- Insertions pour la table CONCERT
INSERT INTO CONCERT (idConcert, nomConcert, tpsPrepaConcert, dateHeureConcert, dureeConcert, idLieu) VALUES (1, 'Concert d ouverture', 30, '2023-10-25 19:00:00', 120, 1);
INSERT INTO CONCERT (idConcert, nomConcert, tpsPrepaConcert, dateHeureConcert, dureeConcert, idLieu) VALUES (2, 'Soirée Musicale', 40, '2023-11-05 20:00:00', 90, 2);
INSERT INTO CONCERT (idConcert, nomConcert, tpsPrepaConcert, dateHeureConcert, dureeConcert, idLieu) VALUES (3, 'Symphonie en Soirée', 25, '2023-11-15 18:30:00', 150, 3);

-- Insertions pour la table SPECTATEUR
INSERT INTO SPECTATEUR (idSpectateur, nomSpectateur, prenomSpectateur, motPasseSpectateur, emailSpectateur, anniversaireSpectateur) VALUES (1, 'Valentin', 'Romanet', 'mdpRomanet', 'valentin@example.com', '2004-05-15');
INSERT INTO SPECTATEUR (idSpectateur, nomSpectateur, prenomSpectateur, motPasseSpectateur, emailSpectateur, anniversaireSpectateur) VALUES (2, 'Hugo', 'Sainson', 'mdpSainson', 'hugo@example.com', '2004-12-20');
INSERT INTO SPECTATEUR (idSpectateur, nomSpectateur, prenomSpectateur, motPasseSpectateur, emailSpectateur, anniversaireSpectateur) VALUES (3, 'Thibault', 'Saint-Leger', 'mdpSaint', 'thibault@example.com', '2004-17-06');
INSERT INTO SPECTATEUR (idSpectateur, nomSpectateur, prenomSpectateur, motPasseSpectateur, emailSpectateur, anniversaireSpectateur) VALUES (3, 'Arthur', 'Villet', 'mdpVillet', 'arthur@example.com', '2004-03-10');

-- Insertions pour la table STYLE
INSERT INTO STYLE (idStyle, nomStyle) VALUES (1, 'Rock');
INSERT INTO STYLE (idStyle, nomStyle) VALUES (2, 'Pop');
INSERT INTO STYLE (idStyle, nomStyle) VALUES (3, 'Jazz');

-- Insertions pour la table SOUSSTYLE
INSERT INTO SOUSSTYLE (idSousStyle, idStyle, nomSousStyle) VALUES (1, 1, 'Rock alternatif');
INSERT INTO SOUSSTYLE (idSousStyle, idStyle, nomSousStyle) VALUES (2, 1, 'Hard rock');
INSERT INTO SOUSSTYLE (idSousStyle, idStyle, nomSousStyle) VALUES (3, 2, 'Pop-rock');

-- Insertions pour la table INSTRUMENT
INSERT INTO INSTRUMENT (idInstrument, nomInstrument) VALUES (1, 'Guitare');
INSERT INTO INSTRUMENT (idInstrument, nomInstrument) VALUES (2, 'Batterie');
INSERT INTO INSTRUMENT (idInstrument, nomInstrument) VALUES (3, 'Piano');

-- Insertions pour la table JOUER
INSERT INTO JOUER (idArtiste, idInstrument) VALUES (1, 1);
INSERT INTO JOUER (idArtiste, idInstrument) VALUES (2, 2);
INSERT INTO JOUER (idArtiste, idInstrument) VALUES (3, 3);

-- Insertions pour la table ETRESTYLE
INSERT INTO ETRESTYLE (idStyle, idGroupe) VALUES (1, 1);
INSERT INTO ETRESTYLE (idStyle, idGroupe) VALUES (2, 2);
INSERT INTO ETRESTYLE (idStyle, idGroupe) VALUES (3, 3);

-- Insertions pour la table TYPE
INSERT INTO TYPE (idType, nbJours, prix, ageMin, ageMax) VALUES (1, 3, 50.0, 18, 60);
INSERT INTO TYPE (idType, nbJours, prix, ageMin, ageMax) VALUES (2, 1, 25.0, 16, 45);
INSERT INTO TYPE (idType, nbJours, prix, ageMin, ageMax) VALUES (3, 2, 35.0, 21, 70);

-- Insertions pour la table BILLET
INSERT INTO BILLET (idBillet, dateBillet, idType, idSpectateur) VALUES (1, '2023-10-15', 1, 1);
INSERT INTO BILLET (idBillet, dateBillet, idType, idSpectateur) VALUES (2, '2023-11-02', 2, 2);
INSERT INTO BILLET (idBillet, dateBillet, idType, idSpectateur) VALUES (3, '2023-11-20', 3, 3); 

-- Insertions pour la table ETRETYPE
INSERT INTO ETRETYPE (idBillet, idType) VALUES (1, 1);
INSERT INTO ETRETYPE (idBillet, idType) VALUES (2, 2);
INSERT INTO ETRETYPE (idBillet, idType) VALUES (3, 3);

-- Insertions pour la table POSSEDE
INSERT INTO POSSEDE (idStyle, idSousStyle) VALUES (1, 1);
INSERT INTO POSSEDE (idStyle, idSousStyle) VALUES (1, 2);
INSERT INTO POSSEDE (idStyle, idSousStyle) VALUES (2, 3);

-- Insertions pour la table APPARTENIR
INSERT INTO APPARTENIR (idArtiste, idGroupe) VALUES (1, 1);
INSERT INTO APPARTENIR (idArtiste, idGroupe) VALUES (2, 2);
INSERT INTO APPARTENIR (idArtiste, idGroupe) VALUES (3, 3);

-- Insertions pour la table ORGANISERCONCERT
INSERT INTO ORGANISERCONCERT (idGroupe, idConcert) VALUES (1, 1);
INSERT INTO ORGANISERCONCERT (idGroupe, idConcert) VALUES (2, 2);
INSERT INTO ORGANISERCONCERT (idGroupe, idConcert) VALUES (3, 3);

-- Insertions pour la table FAVORIS
INSERT INTO FAVORIS (idGroupe, idSpectateur) VALUES (1, 1);
INSERT INTO FAVORIS (idGroupe, idSpectateur) VALUES (2, 2);
INSERT INTO FAVORIS (idGroupe, idSpectateur) VALUES (3, 3);

-- Insertions pour la table RESERVER
INSERT INTO RESERVER (idConcert, idSpectateur) VALUES (1, 1);
INSERT INTO RESERVER (idConcert, idSpectateur) VALUES (2, 2);
INSERT INTO RESERVER (idConcert, idSpectateur) VALUES (3, 3);
