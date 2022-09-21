__author__ = 'Apurva A Kunkulol'

import os
import json
from pprint import pprint
import uuid

import sqlite3
import click
from flask import current_app, g
from werkzeug.local import Local
from werkzeug.security import check_password_hash, generate_password_hash



def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


def insert_movie_records():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'imdb.json')
    #print(path)
    data = None
    with open(path, "r") as f:
        data = json.load(f)
        db = get_db()
        popularity, director, genre, imdb_score, name = None, None, None, None, None
        for d in data:
            for key, val in d.items():
                if key == "99popularity":
                    popularity = val
                    #print("\nPopularity: {}\n".format(popularity))
                elif key == "director":
                    director = val
                    #print("\nDirector: {}\n".format(director))
                elif key == "genre":
                    genre = json.dumps(val)
                    #print("\nGenre: {}\n".format(json.dumps(val)))
                elif key == "imdb_score":
                    imdb_score = val
                    #print("\nimdb_score: {}\n".format(imdb_score))
                elif key == "name":
                    name = val
            query = """INSERT INTO MOVIE (title, popularity, director, genre, imdb_score) VALUES
                       (?, ?, ?, ?, ?)"""
            print("Query: {}".format(query))
            db.execute(query, (name, popularity, director, json.dumps(genre), imdb_score))
            db.commit()


    pprint("JSON data: {}\nType: {}".format(data[0], type(data)))


def insert_roles():
    db = get_db()
    cur = db.cursor()
    try:
       query = """INSERT INTO ROLE (role_name) VALUES (?)"""
       cur.executemany(query, [("admin", ), ("viewer", )])
       #db.execute(query, )
       for itm in cur.execute("Select * from Role"):
           print("Role: {}\t{}".format(itm[0], itm[1]))
    except Exception as ex:
        raise ex


def insert_users():
    db = get_db()
    try:
        query = """INSERT INTO imdb_user (user_name, password, role_id) VALUES (?, ?, ?)"""

        res = db.execute(query, ("admin", generate_password_hash("admin"), 1))
        #query = """Select * from imdb_user where user_name = ?"""
        #res = db.execute(query, ("admin", ))
        #for itm in res:
        #    print(itm[0], "\t", itm[1], "\t", itm[2])

    except Exception as ex:
        raise ex

@click.command("init-db")
def init_db_command():
    init_db()
    insert_movie_records()
    insert_roles()
    insert_users()
    click.echo("Initialized database.")




def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)



