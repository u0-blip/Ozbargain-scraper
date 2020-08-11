from wtforms import form, StringField, fields, FormField, SubmitField, BooleanField, TextField
from models import db


def add_pref(user, pref_descriptions):
    prefs = []
    for p in pref_descriptions:
        prefs.append(pref_data(description = p, user=user, user_id = user.id))
    db.session.commit()

class pref_data(db.Model):
    __tablename__ = 'pref_data'
    id = db.Column(db.Integer(), primary_key=True)

    description = db.Column(db.String(255))
    value = db.Column(db.Boolean())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    user = db.relationship('User', back_populates="pref")

    def __str__(self):
        return str(self.id)

class pref_form(form.Form):
    description = StringField()
    value = BooleanField()

class Pref_list_form(form.Form):
    pref = fields.FieldList(FormField(pref_form, default=lambda: pref_data()), min_entries=0)
    submit_pref = SubmitField(label='Save')
