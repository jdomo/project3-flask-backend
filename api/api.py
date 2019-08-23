import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

import os
import sys
import secrets

from PIL import Image

album = Blueprint('album', 'albums', url_prefix="/api")

def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  f_name, f_ext = os.path.splitext(form_picture.filename)
  picture_name = random_hex + f_ext
  file_path_for_avatar = os.path.join(os.getcwd(), 'static/album_pics/' + picture_name)
  output_size = (125, 175)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(file_path_for_avatar)

  return picture_name

@album.route('/', methods=["GET"])
def get_all_albums():
  try:
    albums = [model_to_dict(album) for album in models.Album.select()]
    return jsonify(data=albums, status={"code": 200, "message": "Success"}) 
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "Error getting the resource"})

@album.route('/', methods=["POST"])
def create_album():

    payload = request.get_json()
    print(payload)
    print(current_user.get_id(), '<---current user id')
    payload['created_by'] = current_user.get_id()
    album = models.Album.create(**payload)
    album_dict = model_to_dict(album)

    return jsonify(data=album_dict, status={"code":201, "message": "Success"})

@album.route('/<id>', methods=["GET"])
def get_album(id):
    album = models.Album.get_by_id(id)

    return jsonify(data=model_to_dict(album), status={"code": 200, "message": "Success"})

@album.route('/<id>', methods=["PUT"])
def update_album(id):
    payload = request.get_json()
    query = models.Album.update(**payload).where(models.Album.id == id)
    query.execute()

    updated_album = models.Album.get_by_id(id)
    return jsonify(data=model_to_dict(updated_album), status={"code": 200, "message": "Album successfully updated"})

@album.route('/<id>', methods=["DELETE"])
def delete_album(id):
  deleted_album = models.Album.get_by_id(id)
  delete_album = models.Album.delete().where(models.Album.id == id)
  delete_album.execute()

  return jsonify(data=model_to_dict(deleted_album), status={"code": 200, "message": "Album successfully deleted"})
