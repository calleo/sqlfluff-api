from flask import Flask, request, abort, jsonify, make_response
from sqlfluff.api.simple import fix, lint
import tempfile
from sqlfluff.core import (
    SQLFluffUserError,
)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Welcome to SQL Formatter API!"


@app.route("/v1/format", methods=["POST"])
def format_sql_post():
    body = request.get_json()

    with tempfile.NamedTemporaryFile("w+t") as conf:
        conf.write(body["conf"])
        conf.seek(0)
        try:
            lint_res = lint(body["sql"], config_path=conf.name, dialect=body["dialect"])
            fixed = fix(body["sql"], config_path=conf.name, dialect=body["dialect"])
        except SQLFluffUserError as e:
            abort(make_response(jsonify(message=str(e)), 400))

    return {"lint": lint_res, "sql": fixed}
