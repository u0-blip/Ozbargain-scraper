from wtforms import form, StringField, fields, FormField, SubmitField, BooleanField
from flask_admin import BaseView, expose, AdminIndexView
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from models import User, roles_users, Role, db, user_datastore, pref_descriptions
from flask import Flask, url_for, redirect, render_template, request, abort, Response, Blueprint
from communication_preferene_view import Pref_list_form, add_pref

class query_data(db.Model):
    __tablename__ = 'query_data'
    id = db.Column(db.Integer(), primary_key=True)
    query = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    user = db.relationship('User', back_populates="queries")

    def __str__(self):
        return self.query

class query_form(form.Form):
    query = StringField(label='Query')

class Query_list_form(form.Form):
    queries = fields.FieldList(
        FormField(query_form, default=lambda: query_data()), min_entries=0)
    query1 = StringField(label='Query')
    submit_query = SubmitField(label='Save')

class index_view(AdminIndexView):
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        if current_user.is_authenticated:
            user = db.session.query(User).filter(User.id == current_user.id).first()
            query_list_form = Query_list_form(formdata=request.form)
            print('req form', request.form)
            pref_list_form = Pref_list_form(formdata=request.form)

            user = db.session.query(User).filter(User.id == current_user.id).first()

            if len(user.pref) == 0:
                add_pref(user, pref_descriptions)
                pref_list_form = Pref_list_form(obj=user)
                print('0 pref list form: ', pref_list_form.pref)


            print('pref list form: ', user.pref[0].description)

            # for i, p in enumerate(pref_list_form.pref):
            #     p.description = user.pref[i].description
            #     print('pref list form: ', p.description)

            # print(query_list_form)
            if query_list_form.submit_query.data and query_list_form.validate() and request.method == 'POST':
                # get_spider_output.apply_async(kwargs={'user_id': current_user.id})
                query_list_form.populate_obj(user)
                db.session.commit()
                print('another yeah')
                if len(query_list_form.query1._value()) > 0:
                    qd = query_data()
                    qd.query = query_list_form.query1._value()
                    qd.user_id = current_user.id
                    qd.user = user
                    db.session.commit()

            if pref_list_form.submit_pref.data and pref_list_form.validate() and request.method == 'POST':
                # get_spider_output.apply_async(kwargs={'user_id': current_user.id})
                # pref_list_form.populate_obj(user)
                checked = []
                for p in pref_list_form:
                    print(type(p))
                    try:
                        for p1 in p:
                            index = p1.name.split('-')[-1]
                            index = int(index)
                            checked.append(index)
                    except:
                        pass 

                for i, p in enumerate(user.pref):
                    if i in checked:
                        p.value = True
                    else:
                        p.value = False

                db.session.commit()

            user = db.session.query(User).filter(User.id == current_user.id).first()
            user.query1 = ''

            query_list_form = Query_list_form(obj=user)
            pref_list_form = Pref_list_form(obj=user)

            return self.render('admin/index.html', query_list_form = query_list_form, pref_list_form=pref_list_form)
        else:
            return redirect(url_for('security.login', next=request.url))

