from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired

class aanpassen_eten_form(FlaskForm):
    id_field = HiddenField()
    naam = StringField('naam van het eten', validators=[DataRequired()])
    categorie = StringField('categorie', validators=[DataRequired()])
    submit = SubmitField('Voeg toe')

class aanpassen_mo_form(FlaskForm):
    id_field = HiddenField()
    naam = StringField('naam micro-organisme', validators=[DataRequired()])
    herkenning = StringField("herkenning", validators=[DataRequired()])
    risiconiveau = StringField('risiconiveau', validators=[DataRequired()])
    actie = StringField('actie', validators=[DataRequired()])
    symptomen = StringField('symptomen', validators=[DataRequired()])
    beschrijving = StringField('beschrijving')
    submit = SubmitField('Voeg toe')

