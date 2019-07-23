from flask import (Blueprint, request, jsonify, abort)
import json
from ..models import Mental_Model, Mental_Model_Schema
from app import db
from app.response import InvalidUsage


mental_models = Blueprint('mental-models', __name__,
                          url_prefix='/mental-models')

mm_schema = Mental_Model_Schema()
mms_schema = Mental_Model_Schema(many=True)


@mental_models.route('/', methods=['GET'])
def GET_mental_models():
  models = Mental_Model.query.all()
  all_models = mms_schema.dump(models).data
  return {'results': len(all_models), 'data': mms_schema.dump(models).data}


@mental_models.route('/<id>', methods=['GET'])
def GET_one_mental_model(id):
  # Get from DB
  model = Mental_Model.query.filter_by(id=id).first()

  # Not found
  if model is None:
    abort(404)

  # Return to client
  else:
    return mm_schema.dump(model).data


@mental_models.route('/', methods=['POST'])
def POST_mental_models():
  # Get JSON from request
  json_data = request.get_json()
  if not json_data:
    raise InvalidUsage('No data provided.')

  if not 'title' in json_data:
    raise InvalidUsage('Title is a required field.')

  # De-serialize
  data, errors = mm_schema.load(json_data, session=db.session)
  if errors:
    return errors, 422

  # Check if a mental model with that title already exists
  model = Mental_Model.query.filter_by(title=data.title).first()
  if model:
    raise InvalidUsage(
        'A MentalModel with that title already exists.', 400)

  # Add to DB
  db.session.add(data)
  db.session.commit()

  # Return to client
  return mm_schema.dump(data).data


@mental_models.route('/<id>', methods=['PUT'])
def PUT_mental_model(id):
  # Get request JSON
  json_data = request.get_json()
  if not json_data:
    return 'No data provided.'

  updated, errors = mm_schema.load(
      json_data, session=db.session, partial=True)
  if errors:
    return jsonify(errors), 422

  # Get from DB
  existing_model = Mental_Model.query.filter_by(id=id).first()
  if existing_model is None:
    raise InvalidUsage('MentalModel not found', 404)

  # 'title' is a special case since it needs to be unique
  if json_data['title']:
    existing_title = Mental_Model.query.filter_by(
        title=json_data['title']).first()
    if existing_title is not None:
      raise InvalidUsage(
          'A MentalModel with that title already exists', 400)
    existing_model.title = json_data['title']

  existing_model.update(**json_data)

  # Update DB
  db.session.commit()

  # Return to client
  return mm_schema.dump(existing_model).data
