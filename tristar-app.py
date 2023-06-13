import os
import phonenumbers
from dotenv import load_dotenv
from flask import Flask
from flask import flash, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, EmailField, TelField, RadioField, validators

app = Flask(__name__)

GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tanyushashilina1@gmail.com'
app.config['MAIL_PASSWORD'] = GMAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

class ReservationForm(FlaskForm):
    guest_name = StringField('Guest name:*', validators=[validators.DataRequired(), validators.Length(min=2, max=35)])
    guest_email = EmailField('Email address:*', validators=[validators.DataRequired(), validators.Length(min=3, max=50)])
    guest_phone = TelField('Phone number:*', validators=[validators.DataRequired(), validators.Length(min=10, max=20)])
    arrival = DateField('Select the date of your arrival:*', validators=[validators.InputRequired()])
    departure = DateField('Select the date of your departure:*', validators=[validators.InputRequired()])
    adults = IntegerField('Adults:*', validators=[validators.InputRequired(), validators.NumberRange(min=1, max=30)])
    children = IntegerField('Children:*', validators=[validators.InputRequired(), validators.NumberRange(min=0, max=30)])
    pets = RadioField('Will you have any pets?*', choices=['Yes', 'No'], validators=[validators.InputRequired()])
    room_type = RadioField('What type of room will you need?*', choices=['Single Queen', 'Single King', 'Double Queen'],
                            validators=[validators.InputRequired()])
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hotel')
def hotel():
    return render_template('hotel.html')

@app.route('/bar')
def bar():
    return render_template('bar.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    form = ReservationForm()
    if form.validate_on_submit():
        msg = Message('Reservation request', sender='tanyushashilina1@gmail.com', recipients=['tanyushashilina1@gmail.com'])
        msg.body = (f'You got a new reservation request. Here is the guest data:\n'
                   f'Name: {form.guest_name.data}\nEmail: {form.guest_email.data}\nPhone number: {form.guest_phone.data}\n'
                   f'Arrival: {form.arrival.data}\nDeparture: {form.departure.data}\n'
                   f'Among guests: {form.adults.data} adult(s), {form.children.data} child(ren)\n'
                   f'Pets: {form.pets.data}\nRoom type: {form.room_type.data}\n'
                   f'Please, contact the guest as soon as possible!')
        mail.send(msg)
        return redirect('/success')
    return render_template('reservation.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)