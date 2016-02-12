# https://github.com/flask-admin/flask-admin/blob/master/examples/auth-flask-login/app.py
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, helpers
import flask_login as login
from flask import redirect, url_for, request
from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()



# Initialize flask-login
def init_login(app):
	login_manager = login.LoginManager()
	login_manager.init_app(app)
    
	# Create user loader function
	@login_manager.user_loader
	def load_user(user_id):
		return db.session.query(User).get(user_id)


# Create customized model view class
class HawkerAdminModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated
        
class HawkerAdminIndexView(AdminIndexView) :

	@expose('/')
	def index(self):
		if not login.current_user.is_authenticated:
			return redirect(url_for('.login_view'))
		return super(HawkerAdminIndexView, self).index()
	
	@expose('/login/', methods=('GET', 'POST'))
	def login_view(self):
		# handle user login
		form = LoginForm(request.form)
		if helpers.validate_form_on_submit(form):
			user = form.get_user()
			login.login_user(user)

		if login.current_user.is_authenticated:
			return redirect(url_for('.index'))
		
		self._template_args['form'] = form
		return super(HawkerAdminIndexView, self).index()

	@expose('/logout/')
	def logout_view(self):
		login.logout_user()
		return redirect(url_for('.index'))
        

