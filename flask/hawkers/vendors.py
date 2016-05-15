from flask import Blueprint, render_template, abort, g, request, session
from flask import flash, redirect, url_for
from jinja2 import TemplateNotFound  
from flask_login import login_required
from hawkers.models import User, Hawker, CutOffTime, db
from wtforms import form, fields, validators, ValidationError
from wtforms_components import TimeField

vendor_page = Blueprint('vendor_page', __name__, template_folder='vendor_templates')

# Forms
class StallForm(form.Form) :
    name = fields.TextField('Name', [validators.InputRequired(), validators.Length(max=100)])
    address = fields.TextAreaField('Address', [validators.InputRequired(), validators.Length(max=500)])
    pincode = fields.IntegerField('PinCode', [validators.InputRequired()])
    contact_number = fields.IntegerField('Contact Number', [validators.InputRequired(), ])
    owner = fields.SelectField('Owner', coerce=int)
    
    def validate_pincode(form, field) :
        if len(str(field.data)) != 6 :
            raise ValidationError('Pincode must be 6 digits.')
            
    def validate_contact_number(form, field) :
        if len(str(field.data)) != 8 :
            raise ValidationError('Contact number must be 8 digits.')
    
class ManageFoodForm(form.Form):
	name = fields.TextField('Name', [validators.InputRequired(), validators.Length(max=50)])
	description = fields.TextAreaField('Address', [validators.InputRequired(), validators.Length(max=200)])
	price = fields.DecimalField('Price', [validators.InputRequired(),])
	is_available = fields.BooleanField('Available?', [])
	image = fields.FileField(u'Image File', [validators.InputRequired(), ])
	
	def validate_image(form, field) :
	    print field.data
	    
class TimeForm(form.Form) :
    cutofftime = TimeField('Cut Off Time', [validators.InputRequired(),])
    
class ManageOrderForm(form.Form) :
    pass

# Routes
@vendor_page.route('/')
@login_required
def index() :
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

# Manage Stalls
@vendor_page.route('/stall')
def manage_stall() :
    stalls = None
    if g.user.is_admin :
        stalls = Hawker.query.all()
        for stall in stalls :
            owner = User.query.get(stall.owner)
            stall.user = owner
    else :
        stalls = Hawker.query.filter_by(owner=g.user.id).all()
        for stall in stalls :
            stall.user = g.user
    return render_template('stall.html', stalls=stalls)

@vendor_page.route('/stall/add', methods=['POST', 'GET'])
def add_stall() :
    stall_form = StallForm(request.form)
    # get a list of hawkers for this user. If admin, get all hawkers
    stalls = None
    users = None
    if g.user.is_admin :
        stalls = Hawker.query.all()
        for stall in stalls :
            owner = User.query.get(stall.owner)
            stall.user = owner
        users = User.query.all()
        stall_form.owner.choices = [(user.id, user.login) for user in users]
    else :
        stalls = Hawker.query.filter_by(owner=g.user.id).all()
        stall_form.owner.choices = [(g.user.id, g.user.login)]
        
    if request.method == 'POST' and stall_form.validate() :
        # add a stall for this hawker
        h = Hawker()
        h.owner = stall_form.owner.data
        h.name = stall_form.name.data
        h.address = stall_form.address.data
        h.pincode = stall_form.pincode.data
        h.contact_number = stall_form.contact_number.data
        db.session.add(h)
        db.session.commit()
        return redirect(url_for('vendor_page.index'))
        
    return render_template('addstall.html', form=stall_form)
    
@vendor_page.route('/stall/<int:id>/modify')
def modify_stall(id) :
    stall_form = StallForm(request.form)
    users = None
    if g.user.is_admin :
        users = User.query.all()
        stall_form.owner.choices = [(user.id, user.login) for user in users]
    else :
        stall_form.owner.choices = [(g.user.id, g.user.login)]    
    
    stall = Hawker.query.get(id)
    if request.method == 'POST' and stall_form.validate() :
        # add a stall for this hawker
        stall.owner = stall_form.owner.data
        stall.name = stall_form.name.data
        stall.address = stall_form.address.data
        stall.pincode = stall_form.pincode.data
        stall.contact_number = stall_form.contact_number.data
        db.session.commit()
        return redirect(url_for('vendor_page.index'))
    else :
        stall_form.name.data = stall.name
        stall_form.address.data = stall.address
        stall_form.pincode.data = stall.pincode
        stall_form.contact_number.data = stall.contact_number
        
    return render_template('editstall.html', form=stall_form)
    
@vendor_page.route('/stall/<int:id>/delete')
def delete_stall(id):
    stall = Hawker.query.get(id)
    db.session.delete(stall)
    db.session.commit()
    return redirect(url_for('vendor_page.index'))
    
@vendor_page.route('/food')
def manage_food() :
    return render_template('food.html')

# Manage Cut Off Times
@vendor_page.route('/time')
def manage_timings() :
    # get a list of hawkers for this user. If admin, get all hawkers
    stalls = None
    users = None
    if g.user.is_admin :
        stalls = Hawker.query.all()
    else :
        stalls = Hawker.query.filter_by(owner=g.user.id).all()
    for stall in stalls :
        stall.user = g.user
        cot = CutOffTime.query.filter_by(hawker_id=stall.id).first()
        if cot :
            stall.cut_off_time = cot.cut_off_time
        else :
            stall.cut_off_time = '-'
                      
    return render_template('time.html', stalls=stalls)
    
@vendor_page.route('/time/<int:stall_id>/modify', methods=['POST', 'GET'])
def modify_time(stall_id):
    time_form = TimeForm(request.form)
    cot = CutOffTime.query.filter_by(hawker_id=stall_id).first()

    if request.method == 'POST' and time_form.validate() :
        if not cot :
            cot = CutOffTime()
            cot.cut_off_time = time_form.cutofftime.data
            cot.hawker_id = stall_id
            db.session.add(cot)
        else :
            cot.cut_off_time = time_form.cutofftime.data
        db.session.commit()
        return redirect(url_for('vendor_page.index'))

    if cot :
        time_form.cutofftime.data = cot.cut_off_time
    return render_template('edittime.html', form=time_form, id=stall_id)

@vendor_page.route('/order')
def manage_orders() :
    return render_template('order.html')

@vendor_page.before_request
@login_required
def validate_user():
    if not session['user'] :
        abort(401)
    user = User.query.filter_by(login=session['user']).first()
    g.user = user

