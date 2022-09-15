from flask import Flask, request
from sqlfluff.api.simple import fix, lint
import json

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to sqlfluff-api!'


@app.route('/v1/pretty', methods=['POST'])
def format_sql_post():
    body = json.loads(request.body)
    return f"Here's your formatted SQL: {body['sql']}"


@app.route('/v1/pretty', methods=['GET'])
def format_sql_get():
    sql = f"{request.args.get('code')}\n"
    result = lint(sql=sql)
    return f"You gave me: {sql}. I give you: {fix(sql=sql)}. Lint result: {result}"
