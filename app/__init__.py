import os
import flask
from flask_sslify import SSLify
from datetime import timedelta
from flask_session import Session

# create and configure the app
app = flask.Flask(__name__)
app.secret_key = "anyrandomstring123!!!321"
app.permanent_session_lifetime = timedelta(days=365)

sslify = SSLify(app)


@app.before_request
def before_request():
    flask.session.permanent = True
    flask.session.modified = True
    
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)


from . import main
app.register_blueprint(main.eApp)
