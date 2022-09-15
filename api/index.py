from flask import Flask, request
from sqlfluff.api.simple import fix, lint
import tempfile

app = Flask(__name__)

DIALECT = "ansi"
CONFIG = """
[sqlfluff:rules:L010]
capitalisation_policy = lower
"""


@app.route("/")
def home():
    return "Welcome to sqlfluff-api!"


@app.route("/v1/pretty", methods=["POST"])
def format_sql_post():
    body = request.get_json()

    with tempfile.NamedTemporaryFile("w+t") as conf:
        conf.write(body["conf"])
        conf.seek(0)
        lint_res = lint(body["sql"], config_path=conf.name)
        fixed = fix(body["sql"], config_path=conf.name)

    return {"lint": lint_res, "sql": fixed}
