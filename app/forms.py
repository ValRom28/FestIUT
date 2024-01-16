from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, FileField, ValidationError,TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    mail = StringField(validators=[DataRequired()], render_kw={"placeholder": "Email"})
    mdp = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Mot de passe"})
    submit = SubmitField('Se connecter')
    
class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Nom d'utilisateur"})
    email = StringField(validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Mot de passe"})
    confirm_password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Confirmer le mot de passe"})
    submit = SubmitField('S\'inscrire')
    
    def validate_password(self, password):
        if password.data != self.confirm_password.data:
            raise ValidationError('Les mots de passe doivent correspondre.')
        
class GroupeForm(FlaskForm):
    description_groupe = TextAreaField(validators=[DataRequired()], render_kw={"placeholder": "Description du groupe"})
    photo_groupe = FileField(validators=[DataRequired()], render_kw={"placeholder": "Photo du groupe"})
    insta_groupe = StringField(validators=[DataRequired()], render_kw={"placeholder": "Lien Instagram"})
    spotify_groupe = StringField(validators=[DataRequired()], render_kw={"placeholder": "Lien Spotify"})
    id_hebergement = HiddenField()
    modif = SubmitField('modifier')
    
    
class ConcertForm(FlaskForm):
    id_concert = HiddenField()
    nom_concert= StringField(validators=[DataRequired()], render_kw={"placeholder": "Nom du concert"})
    tps_prepa_concert = StringField(validators=[DataRequired()], render_kw={"placeholder": "Temps de préparation du concert"})
    date_heure_concert = StringField(validators=[DataRequired()], render_kw={"placeholder": "Date du concert"})
    duree_concert = StringField(validators=[DataRequired()], render_kw={"placeholder": "Durée du concert"})
    modif = SubmitField('modifier')
    
class EventForm(FlaskForm):
    id_event= HiddenField()
    date_event = StringField(validators=[DataRequired()], render_kw={"placeholder": "Date de l'event"})
    nom_event = StringField(validators=[DataRequired()], render_kw={"placeholder": "Nom de l'event"})
    
    modif = SubmitField('modifier')
    
class LieuForm(FlaskForm):
    nom_lieu= StringField(validators=[DataRequired()], render_kw={"placeholder": "Nom du lieu"})
    jauge_lieu = StringField(validators=[DataRequired()], render_kw={"placeholder": "Jauge du lieu"})
    coordonne_X = StringField(validators=[DataRequired()], render_kw={"placeholder": "Coordonnée X du lieu"})
    coordonne_Y = StringField(validators=[DataRequired()], render_kw={"placeholder": "Coordonnée Y du lieu"})