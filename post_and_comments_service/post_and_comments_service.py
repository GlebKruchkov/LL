from concurrent import futures
import grpc
import post_service_pb2
import post_service_pb2_grpc
from db_functions import (
    create_posts_table,
    create_post,
    update_post,
    delete_post,
    get_post,
    list_posts
)

class PostService(post_service_pb2_grpc.PostServiceServicer):
    def CreatePost(self, request, context):
        try:
            post_id = create_post(
                title=request.title,
                content=request.content,
                user_id=request.user_id,
                is_private=request.is_private,
                tags=list(request.tags)
            )
            return post_service_pb2.CreatePostResponse(id=post_id)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return post_service_pb2.CreatePostResponse()

    def UpdatePost(self, request, context):
        try:
            success = update_post(
                post_id=request.id,
                title=request.title,
                content=request.content,
                user_id=request.user_id,
                is_private=request.is_private,
                tags=list(request.tags)
            )
            if not success:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Post not found or you don't have permission")
            return post_service_pb2.UpdatePostResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return post_service_pb2.UpdatePostResponse()

    def DeletePost(self, request, context):
        try:
            success = delete_post(
                post_id=request.id,
                user_id=request.user_id
            )
            if not success:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Post not found or you don't have permission")
            return post_service_pb2.DeletePostResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return post_service_pb2.DeletePostResponse()

    def GetPost(self, request, context):
        try:
            post = get_post(
                post_id=request.id,
                user_id=request.user_id
            )
            if not post:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Post not found or you don't have permission")
                return post_service_pb2.GetPostResponse()
            
            return post_service_pb2.GetPostResponse(
                post=post_service_pb2.Post(
                    id=post["id"],
                    title=post["title"],
                    content=post["content"],
                    user_id=post["user_id"],
                    created_at=post["created_at"].isoformat(),
                    updated_at=post["updated_at"].isoformat(),
                    is_private=post["is_private"],
                    tags=post["tags"]
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return post_service_pb2.GetPostResponse()

    def ListPosts(self, request, context):
        try:
            posts, total = list_posts(
                user_id=request.user_id,
                page=request.page,
                per_page=request.per_page
            )
            
            response_posts = []
            for post in posts:
                response_posts.append(post_service_pb2.Post(
                    id=post["id"],
                    title=post["title"],
                    content=post["content"],
                    user_id=post["user_id"],
                    created_at=post["created_at"].isoformat(),
                    updated_at=post["updated_at"].isoformat(),
                    is_private=post["is_private"],
                    tags=post["tags"]
                ))
            
            return post_service_pb2.ListPostsResponse(
                posts=response_posts,
                total=total
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return post_service_pb2.ListPostsResponse()

def serve():
    create_posts_table()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    post_service_pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
