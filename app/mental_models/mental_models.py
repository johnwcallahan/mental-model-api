from flask import ( Blueprint, request, jsonify )
import json
from ..models import Mental_Model

mental_models = Blueprint('mental-models', __name__, url_prefix='/mental-models')

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

@mental_models.route('/', methods=['GET'])
def GET_mental_models():
  models = Mental_Model.query.all()
  return jsonify([m.serialize for m in models])

  return "hello"
  # return jsonify(json_list=[m.serialize for m in models])