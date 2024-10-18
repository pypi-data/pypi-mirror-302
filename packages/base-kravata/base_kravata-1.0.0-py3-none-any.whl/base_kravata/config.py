
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api


app = Flask(__name__)

# loading environment variables
load_dotenv()

# declaring flask application
api = Api(app)