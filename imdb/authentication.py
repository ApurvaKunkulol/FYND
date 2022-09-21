__author__ = 'Apurva A Kunkulol'

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from imdb.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        import pdb
        #pdb.set_trace()
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is a required field."

        if not password:
            error = "Password is a required field."

        if error is None:
            try:
                query = """INSERT INTO imdb_user (user_name, password, role_id) \
                           VALUES (?, ?, ?)"""
                db.execute(query, (username, generate_password_hash(password), 2))
                db.commit()
            except db.IntegrityError as dberr:
                raise dberr
            except Exception as ex:
                raise ex
            else:
                return redirect(url_for("index"))
        flash(error)

    return render_template("authentication/register.html")


@bp.route("/registerasadmin", methods=("GET", "POST"))
def registerasadmin():
    if request.method == "POST":
        import pdb
        #pdb.set_trace()
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is a required field."

        if not password:
            error = "Password is a required field."

        if error is None:
            try:
                query = """INSERT INTO imdb_user (user_name, password, role_id) \
                           VALUES (?, ?, ?)"""
                db.execute(query, (username, generate_password_hash(password), 1))
                db.commit()
            except db.IntegrityError as dberr:
                raise dberr
            except Exception as ex:
                raise ex
            else:
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template("authentication/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        #import pdb
        #pdb.set_trace()
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None
        query = """Select * from imdb_user where user_name = ?"""
        user = db.execute(query, (username,)).fetchall()
        #query = """Select * from imdb_user"""
        #user = db.execute(query)

        if user is None:
            error = "Incorrect Username."
        elif not check_password_hash(user[0][2], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user[0]
            print(url_for("movie_data.getmoviedata"))
            return redirect(url_for("movie_data.getmoviedata"))

        flash(error)

    return render_template("authentication/login.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        query = """Select * from imdb_user where id = {}""".format(user_id)
        g.user = get_db().execute(query).fetchone()

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
