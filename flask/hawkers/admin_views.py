# https://github.com/flask-admin/flask-admin/blob/master/examples/auth-flask-login/app.py
from hawkers import admin
from flask_admin.contrib.sqla import ModelView
from hawkers.models import *


# Create customized model view class
class HawkerAdminModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated
        
class HawkerAdminIndexView(admin.AdminIndexView) :

	@expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()
	
	@expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
        
        
# Initialize flask-login
init_login()

admin.add_view(HawkerAdminModelView(Hawker, db.session))
admin.add_view(HawkerAdminModelView(Menu, db.session))
admin.add_view(HawkerAdminModelView(MenuType, db.session))
admin.add_view(HawkerAdminModelView(Food, db.session))
