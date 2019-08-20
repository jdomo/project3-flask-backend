# 1
from flask import Flask, g

import models

DEBUG = True
PORT = 5000

#initialize instance of Flask class
app = Flask(__name__)

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
