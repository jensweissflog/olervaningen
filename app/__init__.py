from flask import Flask, make_response
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
CORS(app)

# Default settings
app.config.from_object("config")
try:
    # Optional secrets
    app.config.from_object("secrets")
except:
    pass

api = Api(app)



