from flask import Flask, abort, jsonify, request
from contextlib import contextmanager
import datetime

# from flask_api import status
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

# from sqlalchemy.orm import Session
import simplejson as json


# Initiate the flask app
def create_app():
    app = Flask(__name__)
    # Set the location of env variables config
    app.config.from_pyfile("settings.py")

    # Get the env variables
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    engine = create_engine(app.config.get("SQLALCHEMY_DATABASE_URI"))
    # engine = create_engine("mongo")

    db = SQLAlchemy(app)

    # Declarative new tables
    base_decla = declarative_base()

    # Reflection on automap
    base_refcl = automap_base()
    base_refcl.prepare(db.engine, reflect=True)

    factory = sessionmaker(bind=engine)
    session = factory()

    # Index , first entry point
    @app.route("/")
    def _index():
        return "hello GAC-V2"

    # Print some ENV's
    @app.route("/env/<string:id>")
    def _print_env(id):
        return f"{id} = { app.config.get(id) }"

    # Bookings resource
    @app.route("/bookings")
    def _bookings():
        gac_table = db.Table(
            "booking_main", db.metadata, autoload=True, autoload_with=db.engine
        )
        instance = session.query(gac_table).all()
        return jsonify(instance), 200

    # One bookings resource
    @app.route("/bookings/<int:id>")
    def _booking(id):
        gac_table = db.Table(
            "booking_main", db.metadata, autoload=True, autoload_with=db.engine
        )
        for instance in session.query(gac_table).filter_by(booking_id=id):
            print(f"fetched: {id}")
        return jsonify(instance), 200

    # Update a given booking PUT
    # .update({BankAccount.money: BankAccount.money + 50})

    @app.route("/bookings/<int:id>", methods=["PUT"])
    def _booking_update(id):
        randomString = hash(datetime.datetime.now())
        gac_table = db.Table(
            "booking_main", db.metadata, autoload=True, autoload_with=db.engine
        )
        # Success updating
        instance = (
            session.query(gac_table)
            .filter_by(booking_id=id)
            .update(
                {
                    "special_notes": randomString,
                    "last_update": datetime.datetime.now(),
                },
                synchronize_session=False,
            )
        )
        print(f"fetched: {id} and {randomString}")
        session.commit()
        return (
            jsonify(special_notes=randomString, last_update=datetime.datetime.now()),
            200,
        )

    # **Return some table**
    @app.route("/<string:tname>")
    def some_table(tname):

        gac_table = db.Table(tname, db.metadata, autoload=True, autoload_with=db.engine)

        instance = session.query(gac_table).all()
        return jsonify(instance), 200

    # **Filter by query string params**
    @app.route("/qs/<string:tname>")
    def _qs(tname):

        gac_table = db.Table(tname, db.metadata, autoload=True, autoload_with=db.engine)

        instance = session.query(gac_table).filter_by(**request.args.to_dict()).all()
        print(f"success: {request.args.to_dict()}")
        if not instance:
            return jsonify({"message": "No records match"}), 200
        elif instance:
            return jsonify(instance), 200
        else:
            return jsonify({"message": "Other error"})

    return app
