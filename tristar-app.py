import os
from dotenv import load_dotenv
from flask import Flask
from flask import flash, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, BooleanField, EmailField, TelField, RadioField, validators

app = Flask(__name__)

GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class ReservationForm(FlaskForm):
    guest_name = StringField('Guest name:', validators=[validators.DataRequired(), validators.Length(min=2, max=35)])
    guest_email = EmailField('Email:', validators=[validators.DataRequired(), validators.Length(min=3, max=50)])
    guest_phone = TelField('Phone number:', validators=[validators.DataRequired(), validators.Length(min=10, max=15)])
    arrival = DateField('Select the date of your arrival:', validators=[validators.InputRequired()])
    departure = DateField('Select the date of your departure:', validators=[validators.InputRequired()])
    adults = IntegerField('Adults:', validators=[validators.InputRequired(), validators.NumberRange(min=1, max=10)])
    children = IntegerField('Children:', validators=[validators.InputRequired(), validators.NumberRange(min=0, max=10)])
    pets = RadioField('Will you have any pets?', choices=['Yes', 'No'], validators=[validators.InputRequired()])
    is_smoking = RadioField('Will you need smoking or non-smoking room?', choices=['Smoking', 'Non-smoking'],
                            validators=[validators.InputRequired()])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hotel')
def hotel():
    return 'This is the HOTEL page'

@app.route('/bar')
def bar():
    return 'This is the BAR page'

@app.route('/contacts')
def contacts():
    return 'This is the CONTACTS page'

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    form = ReservationForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('reservation.html', form=form)

@app.route('/success')
def success():
    return 'Thank you! We will contact you ASAP!'

if __name__ == '__main__':
    app.run(port=5000, debug=True)