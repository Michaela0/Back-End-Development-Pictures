from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for item in data:
        if item['id'] == id:
            return jsonify(item), 200
    return jsonify({"message": f"Picture with id {id} not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    if not picture:
        return jsonify({'message': 'Invalid or missing JSON data'}), 400

    picture_id = picture.get('id')
    if picture_id is None:
        return jsonify({'message': 'Missing picture id'}), 400

    for item in data:
        if item.get('id') == picture_id:
            return jsonify({"Message": f"picture with id {picture_id} already present"}), 302

    data.append(picture)
    return jsonify(picture), 201

    # check if picture with given id already exists
    for item in data:
        if item.get('id') == picture_id:
            return jsonify({"Message": f"picture with id {picture_id} already present"}), 302

    # append the picture
    data.append(picture)

    # return the created picture with 201 created
    return jsonify(picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    if not picture:
        return jsonify({"message": "Invalid or missing JSON data"}), 400

    if picture.get('id') != id:
        return jsonify({"message": "ID in URL and payload do not match"}), 400

    for item in data:
        if item.get('id') == id:
            item.update(picture)
            return jsonify(item), 200

    return jsonify({"message": "picture not found"}), 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # find a match and remove
    for item in data:
        if item.get('id') == id:
            data.remove(item)
            return "", 204
    # if no match
    return jsonify({"message": "picture not found"}), 404