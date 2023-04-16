import jwt
import hashlib
import datetime
from functools import wraps
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
app.config.from_object("project.config.Config")
database = SQLAlchemy(app)


class Citizen(database.Model):
    __tablename__ = "citizen"
    id = database.Column(database.Integer, primary_key=True)
    national_id = database.Column(database.String(11), unique=True, nullable=False)
    first_name = database.Column(database.String(16), nullable=False)
    last_name = database.Column(database.String(16), nullable=False)
    hes_code = database.Column(database.String(128), unique=True, nullable=False)
    health_status = database.Column(database.Boolean, nullable=False)

    def __init__(self, national_id, first_name, last_name, health_status):
        self.national_id = national_id
        self.first_name = first_name
        self.last_name = last_name
        self.hes_code = hashlib.sha256(
            "{}-{}-{}".format(self.national_id, self.first_name, self.last_name).encode(
                "utf-8"
            )
        ).hexdigest()
        self.health_status = True if health_status.lower() == "true" else False

    def save(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_hes_code(cls, hes_code):
        return (
            cls.query.with_entities(cls.first_name, cls.last_name, cls.health_status)
            .filter_by(hes_code=hes_code)
            .first()
        )


class CitizenSchema(Schema):
    id = fields.Int(dump_only=True)
    national_id = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    hes_code = fields.Str(required=True)
    health_status = fields.Bool(required=True)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("token")
        if not token:
            return (
                jsonify({"message": "Authentication required. Token is missing."}),
                401,
            )

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
        except Exception as e:
            return jsonify({"message": "Error occurred: {}".format(str(e))}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/get_token", methods=["GET"])
def get_token():
    auth = request.authorization
    if auth and auth.password == "get_token":
        token = jwt.encode(
            {
                "user": auth.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token})
    return make_response(
        "Could not verify.", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )


@app.route("/query", methods=["GET"])
@token_required
def hes_code_query():
    """
    Query the database for a citizen by his/her HES code.
    """
    resp = {"success": False, "message": "", "data": []}
    try:
        hes_code = request.get_json()["hes_code"]
        citizen = Citizen.get_by_hes_code(hes_code)
        
        if not citizen:
            resp["message"] = "Citizen not found."
        else:
            schema = CitizenSchema()
            resp["success"] = True
            resp["data"] = {"citizen": schema.dump(citizen)}
    except Exception as e:
        resp["message"] = "Error occurred: {}".format(str(e))
    finally:
        return resp


@app.route("/", methods=["GET"])
def index():
    return {"success": True, "message": "HES server is up!"}
