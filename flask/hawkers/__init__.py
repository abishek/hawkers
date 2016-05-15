from os import environ
from flask import Flask
from flask_admin import Admin
from hawkers import admin_views
from hawkers.vendors import vendor_page
from hawkers.auth import login, init_login

environ['THDP_SETTINGS'] = 'settings.cfg'

app = Flask(__name__, static_folder='static_files', static_url_path='/static')
app.config.from_envvar('THDP_SETTINGS')
#admin = Admin(app, name='hawkers', index_view=admin_views.HawkerAdminIndexView(), template_mode='bootstrap3')

# Register the modules
app.register_blueprint(login)
app.register_blueprint(vendor_page, url_prefix='/vendors')

from hawkers import views
from hawkers.models import db

init_login(app, db)
db.init_app(app)