from flask import request, Response, json, Blueprint, g, jsonify
from sklearn import svm
from sklearn import datasets
from sklearn.externals import joblib

from ..models.DatasetModel import DatasetModel, DatasetSchema

train_api = Blueprint('train', __name__)
train_schema = DatasetSchema()


@train_api.route('/train', methods=['POST'])
def train():
    # get params from request
    params = request.get_json()

    # read dataset
    # iris = datasets.load_iris()
    # X, y = iris.data, iris.target

    x = DatasetModel.get_x_dataset()
    y = DatasetModel.get_y_dataset()
    data_x = train_schema.dump(x, many=True).data
    data_y = train_schema.dump(y, many=True).data
    # x_list = list(data_x.values())
    # y_list = list(data_y.values())

    # fit model
    # clf = svm.SVC(
    #     C=1.0,
    #     probability=True
    # )
    # clf.fit(data_x, data_y)

    # persist model
    # joblib.dump(clf, 'model.pkl')
    # b = clf.score(data_x, data_y)
    return jsonify(200, data_x[0], None)
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