import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

album = Blueprint('album', 'albums', url_prefix="/api")

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
  delete_album = models.Album.delete().where(models.Album.id == id)
  delete_album.execute()

  return jsonify(data="resource successfully deleted", status={"code": 200, "message": "Album successfully deleted"})
