from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (f"mysql://"
                                         f"{os.getenv('DB_USER')}:"
                                         f"{os.getenv('DB_USER_PASS')}"
                                         f"@{os.getenv('DB_URL')}")
db = SQLAlchemy(app)


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
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
