from flask import request, Response, json, Blueprint, g, jsonify
from sklearn import svm
from sklearn.externals import joblib

from ..models.DatasetModel import DatasetModel, DatasetSchema

train_api = Blueprint('train', __name__)
train_schema = DatasetSchema()


@train_api.route('/train', methods=['GET'])
def train():

    x = DatasetModel.get_x_dataset()
    y = DatasetModel.get_y_dataset()
    data_x = train_schema.dump(x, many=True).data
    data_y = train_schema.dump(y, many=True).data
    value = [[] for _ in range(len(data_x))]
    value_y = [[] for _ in range(len(data_y))]
    for data in range(len(data_x)):
        value[data].append(data_x[data].get("age", ""))
        value[data].append(data_x[data].get("bmi", ""))
        value[data].append(data_x[data].get("diabetes_pedigree_function", ""))
        value[data].append(data_x[data].get("diastolic_blood_pressure", ""))
        value[data].append(data_x[data].get("number_of_pregnancy", ""))
        value[data].append(data_x[data].get("plasma_glucose_concentration", ""))
        value[data].append(data_x[data].get("triceps_skin_thickness", ""))
        value_y[data].append(data_y[data].get("test_result", ""))

    # fit model
    clf = svm.SVC(
        C=1.0,
        probability=True
    )
    clf.fit(value, value_y)

    # persist model
    joblib.dump(clf, 'model.pkl')
    b = clf.score(value, value_y)
    return jsonify({'hasil': b})
    # return jsonify({'hasil': y})


def __json_data(status, data, error):
    json_res = {
        'status': status,
        'result': data,
        'error': error
    }
    return json_res


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )