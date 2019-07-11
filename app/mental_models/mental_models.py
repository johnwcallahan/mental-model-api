from flask import (Blueprint, request, jsonify, abort)
import json
from ..models import Mental_Model, Mental_Model_Schema
from app import db


mental_models = Blueprint('mental-models', __name__,
                          url_prefix='/mental-models')


@mental_models.route('/', methods=['GET'])
def GET_mental_models():
    print('HERE1')
    mms = Mental_Model.query.all()
    mm_schema = Mental_Model_Schema(many=True)
    data = mm_schema.dump(mms).data
    return jsonify(data)


@mental_models.route('/', methods=['POST'])
def POST_mental_models():
    json_data = request.get_json()
    if not json_data:
        return 'No data provided.'
    mm_schema = Mental_Model_Schema()
    model, errors = mm_schema.load(json_data, db)
    if errors:
        return errors, 422
    # model = Mental_Model(title=json_data.title, description=json_data.description,
    #                      url=json_data.url, category=json_data.category)
    db.session.add(model)
    db.session.flush()
    db.session.commit()
    return mm_schema.dump(model).data


@mental_models.route('/<id>', methods=['GET'])
def GET_one_mental_model(id):
    model = Mental_Model.query.filter_by(id=id).first()
    if model is not None:
        data = Mental_Model_Schema().dump(model).data
        return jsonify(data)
    else:
        abort(404)
