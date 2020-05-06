import os
import requests as req
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from application import app, db
from application.forms import LoginForm, RegistrationForm
from application.forms import AddBookForm, ISBNAddForm, EditDeleteForm
from application.models import User, Book
from application.helpers import get_book_by_isbn, validate_cover

@app.route("/", methods=['GET', 'POST'])
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
        image = validate_cover(form.image.data)
        book = Book(title=form.title.data, author=form.author.data,
                image=image, user_id=current_user.id, description=form.description.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html", form=form)

@app.route("/book/<int:id>", methods=["GET", "POST"])
@login_required
def book(id):
    form = EditDeleteForm()
    book = Book.query.filter_by(id=id).first()
    if book.user_id != current_user.id:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        if form.delete.data:
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            return redirect(url_for("edit", id=book.id))
    return render_template("book.html", book=book, form=form)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    book = Book.query.filter_by(id=id).first()
    form = AddBookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.image = validate_cover(form.image.data)
        book.description = form.description.data
        db.session.commit()
        return redirect(url_for("book", id=book.id))
    return render_template("add.html", form=form)
