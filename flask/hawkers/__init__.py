from flask import Flask
from os import environ

environ['THDP_SETTINGS'] = 'settings.cfg'

app = Flask(__name__)
app.config.from_envvar('THDP_SETTINGS')
from hawkers import views

