import json

from flask import Flask, request

app = Flask(__name__)


def get_credentials(req):
    """
    Returns a dict containing "user" and "groups" information populated by
    the incoming request header "RStudio-Connect-Credentials".
    """
    credential_header = req.headers.get("RStudio-Connect-Credentials")
    if not credential_header:
        return {}
    return json.loads(credential_header)


@app.route("/hello")
def hello():
    user_metadata = get_credentials(request)
    username = user_metadata.get("user")
    if username is None:
        return {"message": "Howdy, stranger."}
    return {"message": f"So nice to see you, {username}."}