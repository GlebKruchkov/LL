import os
from flask import Blueprint, jsonify, request
import grpc
import requests

import post_service_pb2
import post_service_pb2_grpc
from functools import wraps

post_blueprint = Blueprint('post', __name__)

POST_SERVICE_GRPC_URL = os.getenv('POST_SERVICE_GRPC_URL', 'post_and_comments_service:50051')
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user_service:5000')

def get_grpc_stub():
    channel = grpc.insecure_channel(POST_SERVICE_GRPC_URL)
    return post_service_pb2_grpc.PostServiceStub(channel)

def get_current_user_id(auth_token):
    if not auth_token:
        return None
        
    try:
        response = requests.get(
            f"{USER_SERVICE_URL}/api/v1/users/verify",
            headers={"X-Auth-Token": auth_token}
        )
        
        if response.status_code == 200:
            return response.json()[0]
    except requests.exceptions.RequestException:
        return None
        
    return None

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('X-Auth-Token')
        if not auth_token:
            return jsonify({"error": "Authorization token is missing"}), 401
            
        user_id = get_current_user_id(auth_token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.user_id = str(user_id)
        return f(*args, **kwargs)
        
    return decorated_function

@post_blueprint.route('/api/v1/posts', methods=['POST'])
@auth_required
def create_post():
    data = request.json
    stub = get_grpc_stub()
    
    try:
        response = stub.CreatePost(
            post_service_pb2.CreatePostRequest(
                title=str(data.get('title', '')),
                content=str(data.get('content', '')),
                user_id=str(request.user_id),
                is_private=bool(data.get('is_private', False)),
                tags=[str(tag) for tag in data.get('tags', [])]
            )
        )
        return jsonify({
            "id": str(response.id),
            "message": "Post created successfully"
        }), 200
    except grpc.RpcError as e:
        grpc_code = e.code().value[0]
        http_code = {
            0: 500,   # OK (но это ошибка, так как мы в except)
            1: 499,   # CANCELLED
            2: 500,   # UNKNOWN
            3: 400,   # INVALID_ARGUMENT
            4: 504,   # DEADLINE_EXCEEDED
            5: 404,   # NOT_FOUND
            6: 409,   # ALREADY_EXISTS
            7: 403,   # PERMISSION_DENIED
            16: 401,  # UNAUTHENTICATED
        }.get(grpc_code, 500)
        return jsonify({"error": e.details()}), http_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_blueprint.route('/api/v1/posts/<post_id>', methods=['PUT'])
@auth_required
def update_post(post_id):
    data = request.json
    stub = get_grpc_stub()
    
    try:
        stub.UpdatePost(
            post_service_pb2.UpdatePostRequest(
                id=post_id,
                title=data.get('title'),
                content=data.get('content'),
                user_id=request.user_id,
                is_private=data.get('is_private'),
                tags=data.get('tags', [])
            )
        )
        return jsonify({"message": "Post updated successfully"}), 200
    except grpc.RpcError as e:
        return jsonify({"error": e.details()}), e.code()

@post_blueprint.route('/api/v1/posts/<post_id>', methods=['DELETE'])
@auth_required
def delete_post(post_id):
    stub = get_grpc_stub()
    
    try:
        stub.DeletePost(
            post_service_pb2.DeletePostRequest(
                id=post_id,
                user_id=request.user_id
            )
        )
        return jsonify({"message": "Post deleted successfully"}), 200
    except grpc.RpcError as e:
        return jsonify({"error": e.details()}), e.code()

@post_blueprint.route('/api/v1/posts/<post_id>', methods=['GET'])
@auth_required
def get_post(post_id):
    stub = get_grpc_stub()
    
    try:
        response = stub.GetPost(
            post_service_pb2.GetPostRequest(
                id=post_id,
                user_id=request.user_id
            )
        )
        
        post = response.post
        return jsonify({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "is_private": post.is_private,
            "tags": list(post.tags)
        }), 200
    except grpc.RpcError as e:
        return jsonify({"error": e.details()}), e.code()

@post_blueprint.route('/api/v1/posts', methods=['GET'])
@auth_required
def list_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    stub = get_grpc_stub()
    
    try:
        response = stub.ListPosts(
            post_service_pb2.ListPostsRequest(
                user_id=request.user_id,
                page=page,
                per_page=per_page
            )
        )
        
        posts = [{
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "is_private": post.is_private,
            "tags": list(post.tags)
        } for post in response.posts]
        
        return jsonify({
            "posts": posts,
            "total": response.total,
            "page": page,
            "per_page": per_page
        }), 200
    except grpc.RpcError as e:
        return jsonify({"error": e.details()}), e.code()
