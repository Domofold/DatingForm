import os

import threading
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from factories.MysqlConnectionFactory import MysqlConnectionFactory
import requests
import xml.etree.ElementTree as ET
from utils.email import Email
from utils.xml import Xml


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = MysqlConnectionFactory().connection().connect()
auth = HTTPBasicAuth()
db = SQLAlchemy(app)


@auth.verify_password
def verify_password(username, password):
    if (username == os.getenv("SENT_FORMS_LOGIN") and
            password == os.getenv("SENT_FORMS_PASS")):
        return True


class Form(db.Model):
    idForm = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(45))
    dwelling_place = db.Column(db.String(45))
    hobbies = db.Column(db.String(45))
    diet = db.Column(
        db.Enum('wszystkożerna', 'wegańska', 'wegetariańska',
                'fleksitariańska', 'owocowa', 'ketogeniczna'),
                default='wszystkożerna')
    email = db.Column(db.String(45))


@app.route('/', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        dwelling_place = request.form['dwelling_place']
        hobbies = request.form['hobbies']
        diet = request.form['diet']
        email = request.form['email']

        datingform = Form(name=name, age=age, gender=gender, dwelling_place=dwelling_place,
                          hobbies=hobbies, diet=diet, email=email)

        db.session.add(datingform)
        db.session.commit()

        xml_data = Xml.formToXmlBytes(datingform)
        requests.post(os.getenv("SEND_EMAIL_URL"), data=xml_data)

    return render_template('index.html')


@app.route('/sent-forms', methods=["GET", "POST"])
@auth.login_required
def sentForms():
    forms = Form.query.all()
    if request.method == "POST":
        diet = request.form['diet']
        forms = Form.query.filter_by(diet=diet)
    return render_template('sentForms.html', forms=forms)


@app.route('/api/send/email', methods=["GET", "POST"])
def sendEmail():
    try:
        xml_bytes = request.data
        root = ET.fromstring(xml_bytes)

        name = root.find('form/name').attrib['text']
        age = root.find('form/age').attrib['text']
        gender = root.find('form/gender').attrib['text']
        dwelling_place = root.find('form/dwelling_place').attrib['text']
        hobbies = root.find('form/hobbies').attrib['text']
        diet = root.find('form/diet').attrib['text']
        email = root.find('form/email').attrib['text']

        thread = threading.Thread(target=Email.sendEmailNotification,
                                  args=(name, age, gender, dwelling_place, hobbies, diet, email))
        thread.start()
        return "Email has been sent"
    except Exception as e:
        return f"An error has occurred: {str(e)}"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
