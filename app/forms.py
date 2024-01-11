from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, FileField
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
