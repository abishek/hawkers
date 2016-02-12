from flask import Flask
from os import environ
from flask_admin import Admin
from hawkers import admin_views

environ['THDP_SETTINGS'] = 'settings.cfg'

app = Flask(__name__)
app.config.from_envvar('THDP_SETTINGS')
admin = Admin(app, name='hawkers', index_view=admin_views.HawkerAdminIndexView(), template_mode='bootstrap3')

from hawkers import views
