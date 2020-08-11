#!venv/bin/python
from flask import Flask, url_for, redirect, render_template, request, abort, Response, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin import BaseView, expose, AdminIndexView
from wtforms import form, StringField, fields, FormField

import redis
import os
import datetime
import json
import numpy as np

# from bokeh.plotting import figure, show, output_file
# from bokeh.embed import components
# from bokeh.resources import CDN

from basic_app import app
from models import User, roles_users, Role, db, user_datastore,build_sample_db
from celery_worker import get_spider_output
from utilities import get_posts, rdb
from admin_views import admin

# Setup Flask-Security
security = Security(app, user_datastore)


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
