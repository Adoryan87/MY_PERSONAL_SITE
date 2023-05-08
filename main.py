from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
import smtplib
import os
from dotenv.main import load_dotenv

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
load_dotenv()

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about_me():
    return render_template("about.html", change=True)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=os.environ.get("TO_ADRESS"),
                                msg=f"Subject:{form.subject.data}\n\nMy name is {form.name.data} and email is {form.email.data}\n{form.message.data}")
            return redirect(url_for('home'))
    return render_template("contact.html", change=True, form=form)


if __name__ == "__main__":
    app.run()
