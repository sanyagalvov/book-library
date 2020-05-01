import os
import requests as req
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from application import app, db
from application.forms import LoginForm, RegistrationForm
from application.forms import AddBookForm, ISBNAddForm, EditDeleteForm
from application.models import User, Book
from application.isbn import get_book_by_isbn

@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return render_template('landing.html')
    form = ISBNAddForm()
    if form.validate_on_submit():
        if form.isbn.data == "" or form.manual.data:
            return redirect(url_for("add"))
        return redirect(url_for("add", isbn=form.isbn.data))
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

@app.route("/add", defaults={"isbn": None}, methods=['GET', 'POST'])
@app.route("/add/<string:isbn>", methods=['GET', 'POST'])
def add(isbn):
    if isbn:
        book = get_book_by_isbn(isbn)
        if book:
            form = AddBookForm(obj=book)
        else:
            flash("Book was not found! :( Please add this book manually.", "danger")
            form = AddBookForm()
    else:
        form = AddBookForm()
    if form.validate_on_submit():
        image = form.image.data
        book = Book(title=form.title.data, author=form.author.data,
                image=image, user_id=current_user.id)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html", form=form)

@app.route("/book/<int:id>", methods=["GET", "POST"])
def book(id):
    form = EditDeleteForm()
    book = Book.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if form.delete.data:
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for("index"))
    return render_template("book.html", book=book, form=form)
