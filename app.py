# 1
import os
from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

import models

from api.user import user
from api.api import album

DEBUG = True
PORT = 8000

login_manager = LoginManager()

#initialize instance of Flask class
app = Flask(__name__, static_url_path="", static_folder="static")

app.secret_key = '123'
login_manager.init_app(app)
@login_manager.user_loader

def load_user(userid):
  try:
    print(models.User.id, '<-- models.User.id in load_user')
    print(userid, '<-- userid in load_user')
    return models.User.get(models.User.id == userid)
  except models.DoesNotExist:
    return None

CORS(album, origins=['http://localhost:3000', 'https://wwac.herokuapp.com'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000', 'https://wwac.herokuapp.com'], supports_credentials=True)

app.register_blueprint(album)
app.register_blueprint(user)

# 3
@app.before_request
def before_request():
  """OPEN CONNECTION BEFORE REQUEST"""
  g.db = models.DATABASE
  g.db.connect()

@app.after_request
def after_request(response):
  """CLOSE CONNECTION AFTER REQUEST COMPLETE"""
  g.db.close()
  return response

@app.route('/')
def index():
  return 'CRAPPY ALBUM COVERS'

if 'ON_HEROKU' in os.environ:
  print('hitting')
  models.initialize()

# 1
if __name__ == '__main__':
  # app.run(host='0.0.0.0', debug=DEBUG, port=PORT)
  models.initialize()
  app.run(debug=DEBUG, port=PORT)
