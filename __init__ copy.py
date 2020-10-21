from flask import Flask, abort, jsonify, request

# from flask_api import status
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import simplejson as json


# Initiate the flask app
app = Flask(__name__)

# App config
# engine = create_engine("mongodb///?Server=MyServer&Port=27017&Database=test&User=test&Password=Password")
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:zA5o<>2y$.,*aI=-ma97#wQ3!ll8iY0z@167.172.216.105/airport_booking"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

engine = create_engine(
    "mysql+pymysql://root:zA5o<>2y$.,*aI=-ma97#wQ3!ll8iY0z@167.172.216.105/airport_booking"
)
db = SQLAlchemy(app)

# Declare new tables
base_decla = declarative_base()

# Reflection on automap
base_refcl = automap_base()
base_refcl.prepare(db.engine, reflect=True)

factory = sessionmaker(bind=engine)
session = factory()


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


# Return some table
@app.route("/<string:sid>")
def some_table(sid):

    gac_table = db.Table(sid, db.metadata, autoload=True, autoload_with=db.engine)

    instance = session.query(gac_table).all()
    return jsonify(instance), 200


# Return some table record
@app.route("/qs/<string:sid>")
def some_table_record(sid):

    gac_table = db.Table(sid, db.metadata, autoload=True, autoload_with=db.engine)

    instance = session.query(gac_table).filter_by(**request.args.to_dict()).all()
    print(f"success: {request.args.to_dict()}")
    if not instance:
        return jsonify({"message": "No records match"}), 200
    elif instance:
        return jsonify(instance), 200
    else:
        return jsonify({"message": "Other error"})


if __name__ == "__main__":
    app.run(debug=True)