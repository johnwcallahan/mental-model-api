from flask import (Blueprint, request, jsonify, abort)
import json
from ..models import Mental_Model, Mental_Model_Schema
from app import db


mental_models = Blueprint('mental-models', __name__,
                          url_prefix='/mental-models')

mm_schema = Mental_Model_Schema()
mms_schema = Mental_Model_Schema(many=True)


@mental_models.route('/', methods=['GET'])
def GET_mental_models():
    models = Mental_Model.query.all()
    return mms_schema.dumps(models)


@mental_models.route('/', methods=['POST'])
def POST_mental_models():
    # Get JSON from request
    json_data = request.get_json()
    if not json_data:
        return 'No data provided.'

    # Load as model
    model, errors = mm_schema.load(json_data, db)
    if errors:
        return errors, 422

    # Add to DB
    db.session.add(model)
    db.session.flush()
    db.session.commit()

    # Return to client
    return mm_schema.dumps(model)


@mental_models.route('/<id>', methods=['GET'])
def GET_one_mental_model(id):
    # Get from DB
    model = Mental_Model.query.filter_by(id=id).first()

    # Not found
    if model is None:
        abort(404)

    # Return to client
    else:
        return mm_schema.dumps(model)


@mental_models.route('/<id>', methods=['PUT'])
def PUT_mental_model(id):
    # Get request JSON
    json_data = request.get_json()
    if not json_data:
        return 'No data provided.'

    # Get from DB
    existingModel = Mental_Model.query.filter_by(id=id).first()

    # Not found
    if existingModel is None:
        abort(404)

    updatedModel = mm_schema.load(json_data, partial)

    # Update DB
    db.session.add(model)
    db.session.flush()
    db.session.commit()

    # Return to client
    return mm_schema.dump(model).data
