# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import post_service_pb2 as post__service__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in post_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class PostServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreatePost = channel.unary_unary(
                '/post_service.PostService/CreatePost',
                request_serializer=post__service__pb2.CreatePostRequest.SerializeToString,
                response_deserializer=post__service__pb2.CreatePostResponse.FromString,
                _registered_method=True)
        self.UpdatePost = channel.unary_unary(
                '/post_service.PostService/UpdatePost',
                request_serializer=post__service__pb2.UpdatePostRequest.SerializeToString,
                response_deserializer=post__service__pb2.UpdatePostResponse.FromString,
                _registered_method=True)
        self.DeletePost = channel.unary_unary(
                '/post_service.PostService/DeletePost',
                request_serializer=post__service__pb2.DeletePostRequest.SerializeToString,
                response_deserializer=post__service__pb2.DeletePostResponse.FromString,
                _registered_method=True)
        self.GetPost = channel.unary_unary(
                '/post_service.PostService/GetPost',
                request_serializer=post__service__pb2.GetPostRequest.SerializeToString,
                response_deserializer=post__service__pb2.GetPostResponse.FromString,
                _registered_method=True)
        self.ListPosts = channel.unary_unary(
                '/post_service.PostService/ListPosts',
                request_serializer=post__service__pb2.ListPostsRequest.SerializeToString,
                response_deserializer=post__service__pb2.ListPostsResponse.FromString,
                _registered_method=True)


class PostServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreatePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListPosts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PostServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreatePost': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePost,
                    request_deserializer=post__service__pb2.CreatePostRequest.FromString,
                    response_serializer=post__service__pb2.CreatePostResponse.SerializeToString,
            ),
            'UpdatePost': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePost,
                    request_deserializer=post__service__pb2.UpdatePostRequest.FromString,
                    response_serializer=post__service__pb2.UpdatePostResponse.SerializeToString,
            ),
            'DeletePost': grpc.unary_unary_rpc_method_handler(
                    servicer.DeletePost,
                    request_deserializer=post__service__pb2.DeletePostRequest.FromString,
                    response_serializer=post__service__pb2.DeletePostResponse.SerializeToString,
            ),
            'GetPost': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPost,
                    request_deserializer=post__service__pb2.GetPostRequest.FromString,
                    response_serializer=post__service__pb2.GetPostResponse.SerializeToString,
            ),
            'ListPosts': grpc.unary_unary_rpc_method_handler(
                    servicer.ListPosts,
                    request_deserializer=post__service__pb2.ListPostsRequest.FromString,
                    response_serializer=post__service__pb2.ListPostsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'post_service.PostService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('post_service.PostService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class PostService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreatePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/post_service.PostService/CreatePost',
            post__service__pb2.CreatePostRequest.SerializeToString,
            post__service__pb2.CreatePostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdatePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/post_service.PostService/UpdatePost',
            post__service__pb2.UpdatePostRequest.SerializeToString,
            post__service__pb2.UpdatePostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeletePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/post_service.PostService/DeletePost',
            post__service__pb2.DeletePostRequest.SerializeToString,
            post__service__pb2.DeletePostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetPost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/post_service.PostService/GetPost',
            post__service__pb2.GetPostRequest.SerializeToString,
            post__service__pb2.GetPostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListPosts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/post_service.PostService/ListPosts',
            post__service__pb2.ListPostsRequest.SerializeToString,
            post__service__pb2.ListPostsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
