from flask import Blueprint, render_template, abort, g, request, session
from flask import flash, redirect, url_for
from flask.ext.mail import Mail, Message
from jinja2 import TemplateNotFound  
from flask_login import login_required
from hawkers.models import User, Hawker, CutOffTime, Food, Order, OrderItem, db
from wtforms import form, fields, validators, ValidationError
from wtforms_components import TimeField
import re, os
from werkzeug import secure_filename
from PIL import Image

vendor_page = Blueprint('vendor_page', __name__, template_folder='vendor_templates')

# Manage Configurations
vendor_page.config = {}
@vendor_page.record
def record_app_settings(setup_state) :
    app = setup_state.app
    vendor_page.mail = Mail(app)
    vendor_page.config = dict([(key, value) for (key, value) in app.config.items()])
    
def allowed_file(filename) :
    ret = '.' in filename and filename.rsplit('.', 1)[1] in ('jpg')
    return ret
	
# Forms		
class StallForm(form.Form) :
    name = fields.TextField('Name', [validators.InputRequired(), validators.Length(max=100)])
    address = fields.TextAreaField('Address', [validators.InputRequired(), validators.Length(max=500)])
    pincode = fields.IntegerField('PinCode', [validators.InputRequired()])
    email = fields.TextField('E-Mail', [validators.InputRequired(), validators.Email()])
    contact_number = fields.IntegerField('Contact Number', [validators.InputRequired(), ])
    owner = fields.SelectField('Owner', coerce=int)
    
    def validate_pincode(form, field) :
        if len(str(field.data)) not in (5,6) :
            raise ValidationError('Pincode must be 6 digits.')
            
    def validate_contact_number(form, field) :
        if len(str(field.data)) != 8 :
            raise ValidationError('Contact number must be 8 digits.')
    
class FoodForm(form.Form):
	name = fields.TextField('Name', [validators.InputRequired(), validators.Length(max=50)])
	description = fields.TextAreaField('Description', [validators.InputRequired(), validators.Length(max=200)])
	price = fields.DecimalField('Price', [validators.InputRequired(),])
	is_available = fields.BooleanField('Available?', [])
	image = fields.FileField(u'Image File', [])
	
	def validate_image(form, field) :
	    if field.data:
	        field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
	    
class TimeForm(form.Form) :
    cutofftime = TimeField('Cut Off Time (24 Hr, HH:MM:SS Format)', [validators.InputRequired(),])
    
# Routes
@vendor_page.route('/')
@login_required
def index() :
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

# Manage Owners
@vendor_page.route('/owner')
def manage_owners() :
    if not g.user.is_admin :
        return redirect(url_for('vendor_page.index'))
    users = User.query.all()
    return render_template('owner.html', users=users)

@vendor_page.route('/owner/<int:userid>/edit')
def edit_user(userid, methods=['POST', 'GET']) :
    user_form = UserForm(request.form)
    user = Users.query.get(userid)
    if request.method == 'POST' and user_form.validate() :
        user.login = user_form.login.data
        user.first_name = user_form.first_name.data
        user.last_name = user_form.last_name.data
        user.email = user_form.email.data
        db.session.commit()
        return redirect(url_for('vendor_page.index'))

    return render_template('edituser.html', user=user, form=user_form)

@vendor_page.route('/owner/<int:userid>/delete')
def delete_user(userid,  methods=['POST', 'GET']) :
    user = Users.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('vendor_page.index'))

@vendor_page.route('/owner/<int:userid>/changepass')
def change_user_pass(userid,  methods=['POST', 'GET']) :
    user = Users.query.get(userid)
    user_pass_form = UserPassForm(request.form)

    if request.method == 'POST' and user_pass_form.validate() :
        user.password = user_pass_form.password.data
        db.session.commit()
        return redirect(url_for('vendor_page.index'))

    return render_template('changepassword.html', user=user, form=user_pass_form)

@vendor_page.route('/owner/add')
def add_owner(methods=['POST', 'GET']) :
    user_form = UserForm(request.form)

    if request.method == 'POST' and user_form.validate() :
        user = User()
        user.first_name = user_form.first_name.data
        user.last_name = user_form.last_name.data
        user.login = user_form.login.data
        user.email = user_form.email.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('vendor_page.index'))

    return render_template('addowner.html', form=user_form)
    
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
        h.email = stall_form.email.data
        h.contact_number = stall_form.contact_number.data
        db.session.add(h)
        db.session.commit()
        return redirect(url_for('vendor_page.index'))
        
    return render_template('addstall.html', form=stall_form)
    
@vendor_page.route('/stall/<int:id>/modify', methods=['POST', 'GET'])
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
        stall.email = stall_form.email.data
        db.session.commit()
        return redirect(url_for('vendor_page.index'))
    else :
        stall_form.name.data = stall.name
        stall_form.address.data = stall.address
        stall_form.pincode.data = stall.pincode
        stall_form.email.data = stall.email
        stall_form.contact_number.data = stall.contact_number
        
    return render_template('editstall.html', form=stall_form, stallid=stall.id)
    
@vendor_page.route('/stall/<int:id>/delete')
def delete_stall(id):
    stall = Hawker.query.get(id)
    db.session.delete(stall)
    db.session.commit()
    return redirect(url_for('vendor_page.index'))
    
# Manage Food Items
@vendor_page.route('/food/', methods=['POST', 'GET'])
def manage_food() :
    stalls = None
    foods = None
    stallid = 0
    if g.user.is_admin :
        stalls = Hawker.query.all()
    else :
        stalls = Hawker.query.filter_by(owner=g.user.id).all()
        
    if request.method == 'POST' :
        stallid = request.form['stallId']
        foods = Food.query.filter_by(hawker_id=stallid).all() #pretty bad code?
        for food in foods:
            if food.image in ('', None):
                food.thumb = None
            else :
                name, ext = food.image.rsplit('.', 1)
                food.thumb = '%s_thumb.%s'%(name, ext)
        
    return render_template('food.html', stalls=stalls, foods=foods, id=int(stallid))

@vendor_page.route('/food/<int:stallid>/add', methods=['POST', 'GET'])
def add_food(stallid) :
    food_form = FoodForm(request.form)
    stall = Hawker.query.get(stallid)
     
    if request.method == 'POST' and food_form.validate() :
        food = Food()
        food.name = food_form.name.data
        food.description = food_form.description.data
        food.price = food_form.price.data
        food.is_available = food_form.is_available.data
        food.hawker_id = stallid
        image_file = request.files['image']
        food.image = secure_filename(image_file.filename)

        if image_file and allowed_file(image_file.filename) :
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(vendor_page.config['UPLOADED_FILES_DEST'], filename))            
            thumb = Image.open(os.path.join(vendor_page.config['UPLOADED_FILES_DEST'], filename)).resize((40, 40), Image.ANTIALIAS)
            name,ext = filename.rsplit('.', 1)
            thumb_filename = '%s_thumb.%s'%(name, ext)
            thumb.save(os.path.join(vendor_page.config['UPLOADED_FILES_DEST'], thumb_filename))

        db.session.add(food)
        db.session.commit()
        
        return redirect(url_for('vendor_page.index'))
    return render_template('addfood.html', form=food_form, stall=stall)
    
@vendor_page.route('/food/<int:foodid>/delete')
def delete_food(foodid) :
    food = Food.query.get(foodid)
    db.session.delete(food)
    db.session.commit()
    return redirect(url_for('vendor_page.index'))

@vendor_page.route('/food/<int:foodid>/edit', methods=['POST', 'GET'])
def edit_food(foodid) :
    food_form = FoodForm(request.form)
    food = Food.query.get(foodid)
    food_form.name.data = food.name
    food_form.description.data = food.description
    food_form.price.data = food.price
    food_form.is_available.data = food.is_available
    food_form.image.data = food.image
    food_form.image_present = (food.image not in ('', None))
    stall = Hawker.query.get(food.hawker_id)
    if food_form.image_present:
        name, ext = food.image.rsplit('.', 1)
        food_form.image_thumb = '%s_thumb.%s'%(name, ext)
    if request.method == 'POST' and food_form.validate() :
        food.name = food_form.name.data
        food.description = food_form.description.data
        food.price = food_form.price.data
        food.is_available = food_form.is_available.data
        food.hawker_id = stall.id
        image_file = request.files['image']
        if image_file and allowed_file(image_file.filename) :
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(vendor_page.config['UPLOADED_FILES_DEST'], filename))            
            thumb = Image.open(os.path.join(vendor_page.config['UPLOADED_FILES_DEST'], filename)).resize((40, 40), Image.ANTIALIAS)
            name,ext = filename.rsplit('.', 1)
            thumb_filename = '%s_thumb.%s'%(name, ext)
            thumb.save(os.path.join(vendor_page.config['UPLOADED_FILES_DEST'], thumb_filename))
            food.image = secure_filename(image_file.filename)

        db.session.commit()        

        return redirect(url_for('vendor_page.index'))
        
    return render_template('editfood.html', form=food_form, food=food, stall=stall)
    
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

@vendor_page.route('/order',  methods=['POST', 'GET'])
def manage_orders() :
    stalls = None
    orders = None
    stallid = 0
    foods = None
    if g.user.is_admin :
        stalls = Hawker.query.all()
    else :
        stalls = Hawker.query.filter_by(owner=g.user.id).all()
        
    if request.method == 'POST' :
        stallid = request.form['stallId']
        orders = Order.query.filter_by(hawker_id=stallid).all() #pretty bad code?
        foods = {}
        for order in orders :
            orderitems = OrderItem.query.filter_by(order_id=order.id)
            foods[order.id] = []
            for orderitem in orderitems :
                foods[order.id].append(Food.query.get(orderitem.food_id))

    return render_template('order.html', stalls=stalls, orders=orders, foods=foods, id=int(stallid))

@vendor_page.route('/order/<int:orderid>/accept')
def accept_order(orderid) :
    order = Order.query.get(orderid)
    order.accepted = 1
    db.session.commit()
    msg = Message('Order accepted!', 
                    sender=vendor_page.config['DEFAULT_MAIL_SENDER'], 
                    recipients=[order.hawker.email, order.customer_email])
    msg.html = render_template("accept.html", name=order.customer_name)
    vendor_page.mail.send(msg)

    return redirect(url_for('vendor_page.index'))

@vendor_page.route('/order/<int:orderid>/reject')
def reject_order(orderid) :
    order = Order.query.get(orderid)
    order.accepted = 2
    db.session.commit()
    msg = Message('Order rejected :( ', 
                    sender=vendor_page.config['DEFAULT_MAIL_SENDER'], 
                    recipients=[order.hawker.email, order.customer_email])
    msg.html = render_template("reject.html", name=order.customer_name)
    vendor_page.mail.send(msg)
    return redirect(url_for('vendor_page.index'))
    
@vendor_page.route('/order/<int:orderid>/details')
def order_details(orderid) :
    orderItems = OrderItem.query.filter_by(order_id=orderid)
    foodItems = []
    for orderItem in orderItems :
        food = Food.query.get(id=orderItem.food_id)
        foodItems.append(food)
    return render_template('orderdetail.html', foods=foodItems)
    
@vendor_page.before_request
@login_required
def validate_user():
    if not session['user'] :
        abort(401)
    user = User.query.filter_by(login=session['user']).first()
    g.user = user

