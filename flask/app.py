import json

from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
app.config["SWAGGER_UI_DOC_EXPANSION"] = "list"
app.config["RESTX_MASK_SWAGGER"] = False
app.config["ERROR_INCLUDE_MESSAGE"] = False

api = Api(
    app, version="0.1.0", title="User Greetings API", 
    description="Flask APIs can access the username and the names of the groups of the current logged "
    "in user by parsing the RStudio-Connect-Credentials request header."
)
ns = api.namespace("user-greeting", description='request header parse test')

def get_credentials(req):
    """
    Returns a dict containing "user" and "groups" information populated by
    the incoming request header "RStudio-Connect-Credentials".
    """
    credential_header = req.headers.get("RStudio-Connect-Credentials")
    if not credential_header:
        return {}
    return json.loads(credential_header)


@ns.route("/hello")
class UserGreeting(Resource):
    """Prints greeting message to RSC named user"""

    def get(self):
        user_metadata = get_credentials(request)
        username = user_metadata.get("user")
        if username is None:
            return {"message": "Howdy, stranger."}
        return {"message": f"So nice to see you, {username}."}

if __name__ == "__main__":
    app.run(debug=True)