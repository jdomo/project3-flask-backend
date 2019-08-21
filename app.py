# 1
from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

import models

from api.user import user

DEBUG = True
PORT = 5000

login_manager = LoginManager()

#initialize instance of Flask class
app = Flask(__name__, static_url_path="", static_folder="static")

app.secret_key = 'RANDOM STRING'
login_manager.init_app(app)
@login_manager.user_loader

def load_user(userid):
  try:
    return models.user.get(models.User.id == userid)
  except models.DoesNotExist:
    return None

CORS(api, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(api)
app.register_blueprint(user)


@app.route('/')
def index():
  return 'CRAPPY ALBUM COVERS'

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
  

# 1
if __name__ == '__main__':
  # app.run(host='0.0.0.0', debug=DEBUG, port=PORT)
  models.initialize()
  app.run(debug=DEBUG, port=PORT)
