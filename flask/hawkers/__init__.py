from flask import Flask
from os import environ
from flask_admin import Admin

environ['THDP_SETTINGS'] = 'settings.cfg'

app = Flask(__name__)
app.config.from_envvar('THDP_SETTINGS')
admin = Admin(app, name='hawkers', template_mode='bootstrap3')

from hawkers import views
