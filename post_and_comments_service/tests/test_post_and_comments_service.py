import pytest
import grpc
from unittest import mock
from datetime import datetime

import post_service_pb2
import post_service_pb2_grpc
from post_and_comments_service import PostService

@pytest.fixture(scope="module")
def grpc_add_to_server():
    return post_service_pb2_grpc.add_PostServiceServicer_to_server

@pytest.fixture(scope="module")
def grpc_servicer():
    return PostService()

@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    return post_service_pb2_grpc.PostServiceStub(grpc_channel)

@pytest.fixture(autouse=True)
def mock_db_functions():
    with mock.patch('post_and_comments_service.create_posts_table'), \
         mock.patch('post_and_comments_service.create_post') as mock_create, \
         mock.patch('post_and_comments_service.update_post') as mock_update, \
         mock.patch('post_and_comments_service.delete_post') as mock_delete, \
         mock.patch('post_and_comments_service.get_post') as mock_get, \
         mock.patch('post_and_comments_service.list_posts') as mock_list:
        
        mock_create.return_value = "test-id"
        mock_update.return_value = True
        mock_delete.return_value = True
        mock_get.return_value = {
            "id": "test-id",
            "title": "Funny Moments Post",
            "content": "content18",
            "user_id": "jleb",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_private": False,
            "tags": ["meme", "funny"]
        }
        mock_list.return_value = ([{
            "id": f"post-{i}",
            "title": f"Post {i}",
            "content": f"Content {i}",
            "user_id": "jleb",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_private": False,
            "tags": [f"tag{i}"]
        } for i in range(1, 4)], 3)
        
        yield {
            "create": mock_create,
            "update": mock_update,
            "delete": mock_delete,
            "get": mock_get,
            "list": mock_list
        }

def test_create_post_success(grpc_stub, mock_db_functions):
    request = post_service_pb2.CreatePostRequest(
        title="Funny Moments Post",
        content="content18",
        user_id="jleb",
        is_private=False,
        tags=["meme", "funny"]
    )
    response = grpc_stub.CreatePost(request)
    assert response.id == "test-id"
    mock_db_functions["create"].assert_called_once_with(
        title="Funny Moments Post",
        content="content18",
        user_id="jleb",
        is_private=False,
        tags=["meme", "funny"]
    )

def test_create_post_error(grpc_stub, mock_db_functions):
    mock_db_functions["create"].side_effect = Exception("DB error")
    request = post_service_pb2.CreatePostRequest(
        title="Funny Moments Post",
        content="content18",
        user_id="jleb"
    )
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.CreatePost(request)
    assert exc_info.value.code() == grpc.StatusCode.INTERNAL

def test_update_post_success(grpc_stub, mock_db_functions):
    request = post_service_pb2.UpdatePostRequest(
        id="test-id",
        title="Updated Title",
        content="Updated Content",
        user_id="jleb",
        is_private=True,
        tags=["updated"]
    )
    response = grpc_stub.UpdatePost(request)
    assert isinstance(response, post_service_pb2.UpdatePostResponse)
    mock_db_functions["update"].assert_called_once_with(
        post_id="test-id",
        title="Updated Title",
        content="Updated Content",
        user_id="jleb",
        is_private=True,
        tags=["updated"]
    )

def test_update_post_not_found(grpc_stub, mock_db_functions):
    mock_db_functions["update"].return_value = False
    request = post_service_pb2.UpdatePostRequest(
        id="non-existent-id",
        user_id="jleb"
    )
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.UpdatePost(request)
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND

def test_delete_post_success(grpc_stub, mock_db_functions):
    request = post_service_pb2.DeletePostRequest(
        id="test-id",
        user_id="jleb"
    )
    response = grpc_stub.DeletePost(request)
    assert isinstance(response, post_service_pb2.DeletePostResponse)
    mock_db_functions["delete"].assert_called_once_with(
        post_id="test-id",
        user_id="jleb"
    )

def test_get_post_success(grpc_stub, mock_db_functions):
    request = post_service_pb2.GetPostRequest(
        id="test-id",
        user_id="jleb"
    )
    response = grpc_stub.GetPost(request)
    assert response.post.id == "test-id"
    assert response.post.title == "Funny Moments Post"
    assert response.post.tags == ["meme", "funny"]
    mock_db_functions["get"].assert_called_once_with(
        post_id="test-id",
        user_id="jleb"
    )

def test_get_post_not_found(grpc_stub, mock_db_functions):
    mock_db_functions["get"].return_value = None
    request = post_service_pb2.GetPostRequest(
        id="non-existent-id",
        user_id="jleb"
    )
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GetPost(request)
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND

def test_list_posts_success(grpc_stub, mock_db_functions):
    request = post_service_pb2.ListPostsRequest(
        user_id="jleb",
        page=1,
        per_page=10
    )
    response = grpc_stub.ListPosts(request)
    assert len(response.posts) == 3
    assert response.total == 3
    assert response.posts[0].title == "Post 1"
    mock_db_functions["list"].assert_called_once_with(
        user_id="jleb",
        page=1,
        per_page=10
    )

def test_list_posts_error(grpc_stub, mock_db_functions):
    mock_db_functions["list"].side_effect = Exception("DB error")
    request = post_service_pb2.ListPostsRequest(
        user_id="jleb"
    )
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.ListPosts(request)
    assert exc_info.value.code() == grpc.StatusCode.INTERNAL

def test_private_post_access(grpc_stub, mock_db_functions):
    mock_db_functions["get"].return_value = {
        "id": "private-post",
        "title": "Private",
        "content": "Secret",
        "user_id": "jleb",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_private": True,
        "tags": []
    }
    
    request_owner = post_service_pb2.GetPostRequest(
        id="private-post",
        user_id="jleb"
    )
    response_owner = grpc_stub.GetPost(request_owner)
    assert response_owner.post.title == "Private"
    
    mock_db_functions["get"].return_value = None
    request_other = post_service_pb2.GetPostRequest(
        id="private-post",
        user_id="anna"
    )
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GetPost(request_other)
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND
