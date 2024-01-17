from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, FileField, ValidationError,TextAreaField,RadioField,DateField
from wtforms.validators import DataRequired
from app.requests import get_all_lieux


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
    submit = SubmitField('Modifier')
    
    
class ConcertForm(FlaskForm):
    id_concert = HiddenField()
    nom_concert= StringField(validators=[DataRequired()], render_kw={"placeholder": "Nom du concert"})
    tps_prepa_concert = StringField(validators=[DataRequired()], render_kw={"placeholder": "Temps de préparation du concert"})
    date_heure_concert = DateField(validators=[DataRequired()], render_kw={"placeholder": "Date du concert"})
    duree_concert = StringField(validators=[DataRequired()], render_kw={"placeholder": "Durée du concert"})
    lieu_concert = RadioField(validators=[DataRequired()], render_kw={"placeholder": "Lieu du concert"})
    submit = SubmitField('Modifier')
    
class EventForm(FlaskForm):
    id_event= HiddenField()
    date_event = DateField(validators=[DataRequired()], render_kw={"placeholder": "Date de l'event"})
    nom_event = StringField(validators=[DataRequired()], render_kw={"placeholder": "Nom de l'event"})
    lieux = get_all_lieux()
    lieux = [(lieu.id_lieu, lieu.nom_lieu) for lieu in lieux]
    lieu_event = RadioField('Lieu de l\'event' ,validators=[DataRequired()], render_kw={"placeholder": "Lieu de l'event"} ,choices=lieux) 
    submit = SubmitField('Modifier')