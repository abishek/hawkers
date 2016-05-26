# https://github.com/flask-admin/flask-admin/blob/master/examples/auth-flask-login
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, helpers
from flask import redirect, url_for, request
from flask_admin import form as admin_form
from jinja2 import Markup
from flask_sqlalchemy import SQLAlchemy

    
file_path = 'hawkers/images'
try:
    import os
    os.mkdir(file_path)
except OSError:
    pass

# Create customized model view class
class HawkerAdminModelView(ModelView):

    def is_accessible(self):
        # accessible if the user is authenticated and he is called admin
        return login.current_user.is_authenticated and login.current_user.is_admin


#https://github.com/flask-admin/flask-admin/blob/master/examples/forms/app.py
class ImageAdminView(HawkerAdminModelView):

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=admin_form.thumbgen_filename(model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': admin_form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }
		
        
