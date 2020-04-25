import os
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from application import app, db
from application.forms import LoginForm, RegistrationForm, AddBookForm
from application.models import User, Book

@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return render_template('landing.html')
    form = AddBookForm()
    if form.validate_on_submit():
        image = form.image.data
        book = Book(title=form.title.data, author=form.author.data,
                image=image, user_id=current_user.id)
        db.session.add(book)
        db.session.commit()
    books = Book.query.filter_by(owner=current_user)
    return render_template("index.html", books=books, form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration complete!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
