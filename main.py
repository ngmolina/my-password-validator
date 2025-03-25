import flask
import re

# TODO: change this to your academic email
AUTHOR = "ngmolina@seas.upenn.edu"


app = flask.Flask(__name__)


# This is a simple route to test your server


@app.route("/")
def hello():
    return f"Hello from my Password Validator! Please test your passwords! &mdash; <tt>{AUTHOR}</tt>"


@app.route("/v1/checkPassword", methods=["POST"])
def check_password():
    data = flask.request.get_json() or {}
    pw = data.get("password", "")
    
    # Initialize reason as empty string (for valid passwords)
    reason = ""
    valid = True
    
    # Check length >= 8
    if len(pw) < 8:
        reason = "Password must be at least 8 characters long"
        valid = False
    
    # Check for at least 2 uppercase letters
    elif len(re.findall(r'[A-Z]', pw)) < 2:
        reason = "Password must contain at least 2 uppercase letters"
        valid = False
    
    # Check for at least 2 digits
    elif len(re.findall(r'\d', pw)) < 2:
        reason = "Password must contain at least 2 digits"
        valid = False
    
    # Check for at least 1 special character from !@#$%^&*
    elif len(re.findall(r'[!@#$%^&*]', pw)) < 1:
        reason = "Password must contain at least 1 special character (!@#$%^&*)"
        valid = False
    
    # Return the result with HTTP 200 status code
    return flask.jsonify({"valid": valid, "reason": reason}), 200