from flask import Flask, request, abort, jsonify, make_response
from sqlfluff.api.simple import fix, lint
import tempfile
from sqlfluff.core import (
    SQLBaseError,
    SQLFluffUserError,
)
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

from flask import json


@app.errorhandler(SQLFluffUserError)
def handle_exception(exception):
    response = exception.get_response()
    response.data = json.dumps(
        {
            "code": 400,
            "name": exception.name,
            "description": str(exception),
        }
    )
    response.content_type = "application/json"
    return response


@app.route("/")
def home():
    return "Welcome to sqlfluff-api!"


@app.route("/v1/pretty", methods=["POST"])
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
