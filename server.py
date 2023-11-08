import base64
import json
import os
from typing import Generator

import httpx
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)

NETWORK = os.getenv("NETWORK", "localhost")
SPRING_API_PORT = os.getenv("SPRING_API_PORT", "8080")

CORS(
    app,
    origins=[
        f"http://{NETWORK}:{SPRING_API_PORT}",
    ],
)

count = 0


def iter_filename() -> Generator[str, None, None]:
    global count
    yield f"Code_{os.getpid()}_{count}.kt"
    count += 1


client = httpx.Client(
    base_url=f"http://{NETWORK}:{SPRING_API_PORT}/",
    headers={"Content-Type": "application/json"},
    timeout=3,
    verify=False,
)


def get(url: str) -> dict:
    try:
        response = client.get(url)
    except (httpx.HTTPError, Exception) as e:
        return {"error": str(e)}
    return response.json()


def post(url: str, data: dict = {}) -> dict:
    try:
        response = client.post(url, data=json.dumps(data))
    except (httpx.HTTPError, Exception) as e:
        return {"error": str(e)}
    return response.json()


def create_traceback(error_dict: dict) -> str:
    internal: dict = error_dict.get("interval")
    message = error_dict.get("message")
    severity = error_dict.get("severity")

    start = internal.get("start")
    end = internal.get("end")

    return f"{severity} at line {start.get('line')}, column {start.get('ch')}-{end.get('ch')}: {message}"

def create_exception(exception: dict) -> str:
    full_name = exception.get("fullName")
    method = exception.get("stackTrace")[0].get("methodName")
    line = exception.get("stackTrace")[0].get("lineNumber")
    return f"Exception {full_name} at {method} line {line}"

@app.route("/js/<path:path>", methods=["GET"])
def js(path: str):
    return send_from_directory("public/js", path)


@app.route("/css/<path:path>", methods=["GET"])
def css(path: str):
    return send_from_directory("public/css", path)


@app.route("/fonts/<path:path>", methods=["GET"])
def fonts(path: str):
    return send_from_directory("public/fonts", path)


@app.route("/api/version", methods=["GET"])
def api_version():
    return jsonify(get("versions"))


@app.route("/api/run", methods=["GET"])
def compiler_run():
    code = request.args.get("code", "")
    code = base64.b64decode(code).decode("utf-8")

    filename = next(iter_filename())

    out = post(
        "api/compiler/run",
        data={"args": "", "files": [{"name": filename, "text": code}]},
    )

    if out.get("error"):  # httpx errors
        return jsonify(out)

    print(out)
    
    errors: dict = out.get("errors")
    if (error := list(errors.values())[0]) != []:  # kotlin errors
        error_message = create_traceback(error[0])
        return {"error": error_message}

    if out.get("exception") is not None:  # kotlin exceptions
        error_message = create_exception(out.get("exception"))
        return {"error": error_message}

    return {"message": out.get("text")}


@app.route("/version", methods=["GET"])
def compiler_version():
    return get("versions")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
