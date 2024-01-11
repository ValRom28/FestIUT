-- TABLES --

CREATE TABLE APPARTENIR (
  PRIMARY KEY (idArtiste, idGroupe),
  idArtiste INT NOT NULL,
  idGroupe INT NOT NULL
);

CREATE TABLE ARTISTE (
  PRIMARY KEY (idArtiste),
  idArtiste INT NOT NULL,
  nomArtiste VARCHAR(42)
);

CREATE TABLE BILLET (
  PRIMARY KEY (idBillet),
  idBillet INT NOT NULL,
  dateBillet DATE,
  idType INT NOT NULL,
  idSpectateur INT NOT NULL
);

CREATE TABLE CONCERT (
  PRIMARY KEY (idConcert),
  idConcert INT NOT NULL,
  nomConcert VARCHAR(42),
  tpsPrepaConcert INT,
  dateHeureConcert DATE,
  dureeConcert INT,
  idLieu INT NOT NULL
);

CREATE TABLE ETRESTYLE (
  PRIMARY KEY (idStyle, idGroupe),
  idStyle INT NOT NULL,
  idGroupe INT NOT NULL
);

CREATE TABLE ETRETYPE (
  PRIMARY KEY (idBillet, idType),
  idBillet INT NOT NULL,
  idType INT NOT NULL
);

CREATE TABLE FAVORIS (
  PRIMARY KEY (idGroupe, idSpectateur),
  idGroupe INT NOT NULL,
  idSpectateur INT NOT NULL
);

CREATE TABLE GROUPE (
  PRIMARY KEY (idGroupe),
  idGroupe INT NOT NULL,
  nomGroupe VARCHAR(42),
  photoGroupe BLOB,
  descriptionGroupe VARCHAR(42),
  lienInstaGroupe VARCHAR(42),
  lienSpotifyGroupe VARCHAR(42),
  idHebergement INT NOT NULL
);

CREATE TABLE HEBERGEMENT (
  PRIMARY KEY (idHebergement),
  idHebergement INT NOT NULL,
  nomHebergement VARCHAR(42),
  addresseHebergement VARCHAR(42)
);

CREATE TABLE INSTRUMENT (
  PRIMARY KEY (idInstrument),
  idInstrument INT NOT NULL,
  nomInstrument VARCHAR(42)
);

CREATE TABLE JOUER (
  PRIMARY KEY (idArtiste, idInstrument),
  idArtiste INT NOT NULL,
  idInstrument INT NOT NULL
);

CREATE TABLE LIEU (
  PRIMARY KEY (idLieu),
  idLieu INT NOT NULL,
  nomLieu VARCHAR(42),
  jaugeLieu INT,
  coordonneX float,
  coordonneY float
);

CREATE TABLE ORGANISERCONCERT (
  PRIMARY KEY (idGroupe, idConcert),
  idGroupe INT NOT NULL,
  idConcert INT NOT NULL
);

CREATE TABLE POSSEDE (
  PRIMARY KEY (idStyle, idSousStyle),
  idStyle INT NOT NULL,
  idSousStyle INT NOT NULL
);

CREATE TABLE RESERVER (
  PRIMARY KEY (idConcert, idSpectateur),
  idConcert INT NOT NULL,
  idSpectateur INT NOT NULL
);

CREATE TABLE STYLE (
  PRIMARY KEY (idStyle),
  idStyle INT NOT NULL,
  nomStyle VARCHAR(42)
);

CREATE TABLE SOUSSTYLE (
  PRIMARY KEY (idSousStyle),
  idSousStyle INT NOT NULL,
  idStyle INT,
  nomSousStyle VARCHAR(42)
);

CREATE TABLE SPECTATEUR (
  PRIMARY KEY (idSpectateur),
  idSpectateur INT NOT NULL,
  nomSpectateur VARCHAR(42),
  prenomSpectateur VARCHAR(42),
  motPasseSpectateur VARCHAR(42),
  emailSpectateur VARCHAR(42) UNIQUE,
  anniversaireSpectateur DATE,
  photoCompte BLOB
);

CREATE TABLE TYPE (
  PRIMARY KEY (idType),
  idType INT NOT NULL,
  nbJours INT,
  prix FLOAT,
  ageMin INT,
  ageMax INT
);


-- FOREIGN KEYS --

ALTER TABLE APPARTENIR ADD FOREIGN KEY (idGroupe) REFERENCES GROUPE (idGroupe);
ALTER TABLE APPARTENIR ADD FOREIGN KEY (idArtiste) REFERENCES ARTISTE (idArtiste);

ALTER TABLE BILLET ADD FOREIGN KEY (idSpectateur) REFERENCES SPECTATEUR (idSpectateur);

ALTER TABLE CONCERT ADD FOREIGN KEY (idLieu) REFERENCES LIEU (idLieu);

ALTER TABLE ETRESTYLE ADD FOREIGN KEY (idGroupe) REFERENCES GROUPE (idGroupe);
ALTER TABLE ETRESTYLE ADD FOREIGN KEY (idStyle) REFERENCES STYLE (idStyle);

ALTER TABLE ETRETYPE ADD FOREIGN KEY (idBillet) REFERENCES BILLET (idBillet);
ALTER TABLE ETRETYPE ADD FOREIGN KEY (idType) REFERENCES TYPE (idType);

ALTER TABLE FAVORIS ADD FOREIGN KEY (idSpectateur) REFERENCES SPECTATEUR (idSpectateur);
ALTER TABLE FAVORIS ADD FOREIGN KEY (idGroupe) REFERENCES GROUPE (idGroupe);

ALTER TABLE GROUPE ADD FOREIGN KEY (idHebergement) REFERENCES HEBERGEMENT (idHebergement);

ALTER TABLE JOUER ADD FOREIGN KEY (idInstrument) REFERENCES INSTRUMENT (idInstrument);
ALTER TABLE JOUER ADD FOREIGN KEY (idArtiste) REFERENCES ARTISTE (idArtiste);

ALTER TABLE ORGANISERCONCERT ADD FOREIGN KEY (idConcert) REFERENCES CONCERT (idConcert);
ALTER TABLE ORGANISERCONCERT ADD FOREIGN KEY (idGroupe) REFERENCES GROUPE (idGroupe);

ALTER TABLE POSSEDE ADD FOREIGN KEY (idSousStyle) REFERENCES SOUSSTYLE (idSousStyle);
ALTER TABLE POSSEDE ADD FOREIGN KEY (idStyle) REFERENCES STYLE (idStyle);

ALTER TABLE RESERVER ADD FOREIGN KEY (idSpectateur) REFERENCES SPECTATEUR (idSpectateur);
ALTER TABLE RESERVER ADD FOREIGN KEY (idConcert) REFERENCES CONCERT (idConcert);


-- TRIGGERS -- 

DELIMITER |
-- Trigger pour vérifier l'âge du spectateur par rapport au type de billet
CREATE TRIGGER gestionAge BEFORE INSERT ON BILLET
FOR EACH ROW
BEGIN
    DECLARE annivSpec DATE;
    DECLARE ageSpec INT;
    DECLARE ageMinBillet INT;
    DECLARE ageMaxBillet INT;

    SELECT anniversaireSpectateur INTO annivSpec FROM SPECTATEUR WHERE idSpectateur = NEW.idSpectateur;

    SET ageSpec = DATEDIFF(NOW(), annivSpec) / 365;

    SELECT ageMin, ageMax INTO ageMinBillet, ageMaxBillet FROM TYPE WHERE idType = NEW.idType;

    IF ageSpec < ageMinBillet OR ageSpec > ageMaxBillet THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Âge du spectateur en dehors des limites du type de billet';
    END IF;
END |

-- Trigger pour vérifier que l'âge minimum n'est pas supérieur à l'âge maximum dans le type de billet
CREATE TRIGGER gestionAgeMinMax BEFORE INSERT ON TYPE
FOR EACH ROW
BEGIN
    IF NEW.ageMin > NEW.ageMax THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Âge minimum supérieur à l'âge maximum";
    END IF;
END |

-- Trigger pour vérifier la capacité de réservation par rapport à la jauge du lieu
CREATE TRIGGER gestionPlaces BEFORE INSERT ON RESERVER
FOR EACH ROW
BEGIN
    DECLARE nbPlacesReservees INT;
    DECLARE jaugeConcert INT;

    SELECT COUNT(*) INTO nbPlacesReservees FROM RESERVER WHERE idConcert = NEW.idConcert;

    SELECT jaugeLieu INTO jaugeConcert FROM LIEU WHERE idLieu = (SELECT idLieu FROM CONCERT WHERE idConcert = NEW.idConcert);

    IF nbPlacesReservees >= jaugeConcert THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Concert complet, plus de réservations possibles";
    END IF;
END |

DELIMITER ;
