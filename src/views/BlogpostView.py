from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.BlogpostModel import BlogpostModel, BlogpostSchemas

blogpost_api = Blueprint('blogpost_api', __name__)
blogpost_schema = BlogpostSchemas()


@blogpost_api.route('/add', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    req_data['owner_id'] = g.user.get('id')
    data, error = blogpost_schema.load(req_data)
    if error:
        return custom_response(json_data(400, None, error), 400)
    post = BlogpostModel(data)
    post.save()
    data = blogpost_schema.dump(post).data
    return custom_response(json_data(200, data, None), 200)


@blogpost_api.route('/all')
def get_all():
    posts = BlogpostModel.get_all_blogposts()
    data = blogpost_schema.dump(posts, many=True).data
    return custom_response(json_data(200, data, None), 200)


@blogpost_api.route('/<int:blogpost_id>', methods=['GET'])
def get_one(blogpost_id):
    post = BlogpostModel.get_one_blogposts(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post).data
    return custom_response(json_data(200, data, None), 200)


@blogpost_api.route('/<int:blogpost_id>', methods=['PUT'])
@Auth.auth_required
def update(blogpost_id):
    req_data = request.get_json()
    post = BlogpostModel.get_one_blogposts(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post).data
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'persmission denied'}, 400)

    data, error = blogpost_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    post.update(data)

    data = blogpost_schema.dump(post).data
    return custom_response(json_data(200, data, None), 200)


@blogpost_api.route('/<int:blogpost_id>', methods=['DELETE'])
@Auth.auth_required
def delete(blogpost_id):
    post = BlogpostModel.get_one_blogposts(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post).data
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    post.delete()
    return custom_response(json_data(200, 'Data has been deleted', None), 200)


def json_data(status, data, error):
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
