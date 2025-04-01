from unittest.mock import patch, MagicMock
import pytest
from api_service import app
from post_service_pb2 import (
    CreatePostResponse,
    GetPostResponse,
    Post,
    ListPostsResponse
)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_post_success(client):
    with patch('requests.get') as mock_get, \
         patch('grpc.insecure_channel') as mock_channel:
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = ["jleb"]
        
        mock_stub = MagicMock()
        mock_stub.CreatePost.return_value = CreatePostResponse(id="meme")
        mock_channel.return_value = MagicMock()
        
        with patch('api.post.get_grpc_stub', return_value=mock_stub):
            response = client.post(
                '/api/v1/posts',
                json={
                    "title": "Test Post",
                    "content": "Test Content",
                    "is_private": False,
                    "tags": ["memas", "funny"]
                },
                headers={"X-Auth-Token": "valid-token"}
            )
            
            assert response.status_code == 200
            assert response.json == {
                "id": "meme",
                "message": "Post created successfully"
            }

def test_get_post_success(client):
    with patch('requests.get') as mock_get, \
         patch('grpc.insecure_channel') as mock_channel:
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = ["jleb"]
        
        created_at = "2024-12-31T11:11:11"
        updated_at = "2025-01-02T11:11:11"
        
        post = Post(
            id="meme",
            title="Test Post",
            content="Test Content",
            user_id="jleb",
            created_at=created_at,
            updated_at=updated_at,
            is_private=False,
            tags=["memas", "funny"]
        )
        mock_stub = MagicMock()
        mock_stub.GetPost.return_value = GetPostResponse(post=post)
        
        with patch('api.post.get_grpc_stub', return_value=mock_stub):
            response = client.get(
                '/api/v1/posts/meme',
                headers={"X-Auth-Token": "valid-token"}
            )
            
            assert response.status_code == 200
            assert response.json == {
                "id": "meme",
                "title": "Test Post",
                "content": "Test Content",
                "user_id": "jleb",
                "created_at": created_at,
                "updated_at": updated_at,
                "is_private": False,
                "tags": ["memas", "funny"]
            }

def test_list_posts_success(client):
    with patch('requests.get') as mock_get, \
         patch('grpc.insecure_channel') as mock_channel:
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = ["jleb"]
        
        posts = [
            Post(
                id=f"post{i}",
                title=f"Post {i}",
                content=f"Content {i}",
                user_id="jleb",
                created_at="2020-02-02T20:20:20",
                updated_at="2021-02-02T20:20:20",
                is_private=False,
                tags=[f"tag{i}"]
            ) for i in range(1, 4)
        ]
        
        mock_stub = MagicMock()
        mock_stub.ListPosts.return_value = ListPostsResponse(
            posts=posts,
            total=3
        )
        
        with patch('api.post.get_grpc_stub', return_value=mock_stub):
            response = client.get(
                '/api/v1/posts?page=1&per_page=10',
                headers={"X-Auth-Token": "valid-token"}
            )
            
            assert response.status_code == 200
            data = response.json
            assert len(data["posts"]) == 3
            assert data["total"] == 3
            assert data["posts"][0]["title"] == "Post 1"

def test_update_post_success(client):
    with patch('requests.get') as mock_get, \
         patch('grpc.insecure_channel') as mock_channel:
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = ["jleb"]
        
        mock_stub = MagicMock()
        
        with patch('api.post.get_grpc_stub', return_value=mock_stub):
            response = client.put(
                '/api/v1/posts/meme',
                json={
                    "title": "Updated Title",
                    "content": "Updated Content",
                    "is_private": True,
                    "tags": ["updated"]
                },
                headers={"X-Auth-Token": "valid-token"}
            )
            
            assert response.status_code == 200
            assert response.json == {"message": "Post updated successfully"}
            mock_stub.UpdatePost.assert_called_once()

def test_delete_post_success(client):
    with patch('requests.get') as mock_get, \
         patch('grpc.insecure_channel') as mock_channel:
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = ["jleb"]
        
        mock_stub = MagicMock()
        
        with patch('api.post.get_grpc_stub', return_value=mock_stub):
            response = client.delete(
                '/api/v1/posts/meme',
                headers={"X-Auth-Token": "valid-token"}
            )
            
            assert response.status_code == 200
            assert response.json == {"message": "Post deleted successfully"}
            mock_stub.DeletePost.assert_called_once()
