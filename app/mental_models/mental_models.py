from flask import (Blueprint, request, jsonify)
import json
from ..models import Mental_Model, Mental_Model_Schema


mental_models = Blueprint('mental-models', __name__,
                          url_prefix='/mental-models')


@mental_models.route('/', methods=['GET'])
def GET_mental_models():
    models = Mental_Model.query.all()
    if models is not None:
        data = [Mental_Model_Schema().dump(m).data for m in models]
        return jsonify(data)


@mental_models.route('/<int:id>')
def GET_one_mental_model(id):
    model = Mental_Model.query.filter_by(id=id).first()
    print(model)
    if model is not None:
        data = Mental_Model_Schema().dump(model).data
        return jsonify(data)
    else:
        return "Not found"
