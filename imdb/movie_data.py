__author__ = 'Apurva A Kunkulol'


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from imdb.db import get_db
from .authentication import login_required

bp = Blueprint("movie_data", __name__, url_prefix="/movie_data")

@bp.route("/getmoviedata", methods=("GET", "POST"))
@login_required
def getmoviedata():
    lst_mv = []
    db = get_db()
    if request.method == "POST":
        #import pdb
        #pdb.set_trace()
        name = request.form["title"] or None
        director = request.form["director"] or None
        popularity = request.form["popularity"] or None
        genre = request.form["genre"] or None
        imdb_score = request.form["imdb_score"] or None
        error = None

        if error is None:
            try:
                query = """INSERT INTO movie (title, popularity, director, genre, imdb_score) \
                           VALUES (?, ?, ?, ?, ?)"""
                db.execute(query, (name, popularity, director, genre, imdb_score))
                db.commit()
                query = """Select title from Movie"""
                res = db.execute(query)
                #lst_mv = []
                for itm in res:
                    lst_mv.append(itm[0])
            except db.IntegrityError as dberr:
                raise dberr
            except Exception as ex:
                raise ex
            else:
                return redirect(url_for("movie_data.getmoviedata"))
        else:
            flash(error)

    query = """Select title from Movie"""
    res = db.execute(query)
    for itm in res:
        lst_mv.append(itm[0])

    return render_template("movie_data/movie_info.html", movie_list=lst_mv)

