from flask import Blueprint, render_template, abort, g
from flask import request, redirect, url_for, session
from jinja2 import TemplateNotFound  
from wtforms import form, fields, validators
from werkzeug.security import check_password_hash
import flask_login as login
from hawkers.models import db, User

auth = Blueprint('auth', __name__, template_folder='templates')
login_manager = login.LoginManager()

# Initialize flask-login
def init_login(app, db):
    login_manager.init_app(app)
	
# Create user loader function
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.loginaction', next=request.path))
    		
# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
	username = fields.TextField(validators=[validators.required()])
	password = fields.PasswordField(validators=[validators.required()])

	def validate_login(self, field) :
		user = self.get_user()
		
		if user is None:
			raise validators.ValidationError('Invalid user')
			
		if not check_password_hash(user.password, self.password.data):
			raise validators.ValidationError('Invalid password')
			
	def get_user(self):
		# super ugly hack. learn some python first.
		return db.session.query(User).filter_by(login=self.username.data).first()
		
@auth.route('/login', methods=["GET", "POST"])
def loginaction() :
	# handle user login
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate() :
	    user = form.get_user()
	    if login.login_user(user) :
	        session['user'] = user.login
	        print("User %s logged in successfully."%user.login)
	        return redirect(request.args.get('next') or url_for('vendor_page.index'))
	        
	return render_template('login.html', form=form)

@auth.route('/logout')
def logoutaction() :
	login.logout_user()
	session.pop('user', None)
	return redirect(url_for('auth.loginaction'))

