from flask import Flask

app = Flask(__name__)
from hawkers import views

