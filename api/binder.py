import flask
import httpx
import json

import base64

import os

app = flask.Flask(__name__)

NETWORK = os.getenv("NETWORK", "localhost")
SPRING_API_PORT = os.getenv("SPRING_API_PORT", "8080")

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "8002")

client = httpx.Client(
    base_url=f"http://{NETWORK}:{SPRING_API_PORT}/",
    headers={
        "Content-Type": "application/json"
    },
    timeout=30,
    verify=False
)

def get(url: str) -> dict:
    response = client.get(url)
    print(response.text)
    return response.json()

def post(url: str, data: dict = {}) -> dict:    
    response = client.post(url, data=json.dumps(data))
    return response.json()

@app.route("/run", methods=["GET"])
def compiler_run():
    code = flask.request.args.get("code", "")
    code = base64.b64decode(code).decode("utf-8")
    
    filename = flask.request.args.get("filename", "Code.kt")
    
    out = post("api/compiler/run", data={
        "args": "",
        "files": [
            {
                "name": filename,
                "text": code
            }
        ]
    })
    
    return out
@app.route("/version", methods=["GET"])
def compiler_version():
    return get("versions")

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)