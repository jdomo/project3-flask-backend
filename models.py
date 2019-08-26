# 2
import os
from playhouse.db_url import connect
from peewee import *
from flask_login import UserMixin
import datetime

# DATABASE = SqliteDatabase('albums.sqlite') #pre-deploy
DATABASE = connect(os.environ.get('DATABASE_URL'))

class User(UserMixin, Model):
  username = CharField(unique=True)
  email = CharField(unique=True)
  password = CharField()
  image = CharField()

  class Meta:
    database = DATABASE

class Album(Model):
  artist = CharField()
  title = CharField()
  created_at = DateTimeField(default=datetime.datetime.now)
  image= CharField()
  created_by = ForeignKeyField(User, backref='albums')

  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  # DATABASE.drop_tables([User, Album])
  DATABASE.create_tables([User, Album], safe=True)
  print("TABLES CREATED!!")
  DATABASE.close()