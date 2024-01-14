from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, FileField, ValidationError
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
    description_groupe = StringField(validators=[DataRequired()], render_kw={"placeholder": "Description du groupe"})
    photo_groupe = FileField(validators=[DataRequired()], render_kw={"placeholder": "Photo du groupe"})
    insta_groupe = StringField(validators=[DataRequired()], render_kw={"placeholder": "Lien Instagram"})
    spotify_groupe = StringField(validators=[DataRequired()], render_kw={"placeholder": "Lien Spotify"})
    id_hebergement = HiddenField()
    modif = SubmitField('modifier')
