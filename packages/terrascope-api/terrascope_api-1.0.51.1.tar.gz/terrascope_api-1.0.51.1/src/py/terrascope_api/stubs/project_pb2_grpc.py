# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from terrascope_api.models import project_pb2 as project__pb2

GRPC_GENERATED_VERSION = '1.66.2'
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
        + f' but the generated code in project_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ProjectApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.list = channel.unary_unary(
                '/oi.papi.ProjectApi/list',
                request_serializer=project__pb2.ProjectListRequest.SerializeToString,
                response_deserializer=project__pb2.ProjectListResponse.FromString,
                _registered_method=True)
        self.get = channel.unary_unary(
                '/oi.papi.ProjectApi/get',
                request_serializer=project__pb2.ProjectGetRequest.SerializeToString,
                response_deserializer=project__pb2.ProjectGetResponse.FromString,
                _registered_method=True)
        self.create = channel.unary_unary(
                '/oi.papi.ProjectApi/create',
                request_serializer=project__pb2.ProjectCreateRequest.SerializeToString,
                response_deserializer=project__pb2.ProjectCreateResponse.FromString,
                _registered_method=True)
        self.update = channel.unary_unary(
                '/oi.papi.ProjectApi/update',
                request_serializer=project__pb2.ProjectUpdateRequest.SerializeToString,
                response_deserializer=project__pb2.ProjectUpdateResponse.FromString,
                _registered_method=True)
        self.delete = channel.unary_unary(
                '/oi.papi.ProjectApi/delete',
                request_serializer=project__pb2.ProjectDeleteRequest.SerializeToString,
                response_deserializer=project__pb2.ProjectDeleteResponse.FromString,
                _registered_method=True)
        self.run = channel.unary_unary(
                '/oi.papi.ProjectApi/run',
                request_serializer=project__pb2.ProjectRunRequest.SerializeToString,
                response_deserializer=project__pb2.ProjectRunResponse.FromString,
                _registered_method=True)
        self.clone = channel.unary_unary(
                '/oi.papi.ProjectApi/clone',
                request_serializer=project__pb2.ProjectCloneRequest.SerializeToString,
                response_deserializer=project__pb2.ProjectCloneResponse.FromString,
                _registered_method=True)
        self.credit_estimate = channel.unary_unary(
                '/oi.papi.ProjectApi/credit_estimate',
                request_serializer=project__pb2.ProjectCreditEstimateRequest.SerializeToString,
                response_deserializer=project__pb2.ProjectCreditEstimateResponse.FromString,
                _registered_method=True)
        self.request_access = channel.unary_unary(
                '/oi.papi.ProjectApi/request_access',
                request_serializer=project__pb2.ProjectRequestAccessRequest.SerializeToString,
                response_deserializer=project__pb2.ProjectRequestAccessResponse.FromString,
                _registered_method=True)


class ProjectApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def list(self, request, context):
        """
        List the Projects available to the user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """
        Get a specified Project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def create(self, request, context):
        """
        Create a Project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """
        Update a Project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """
        Delete a Project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def run(self, request, context):
        """
        Run a Project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def clone(self, request, context):
        """
        Clone a Project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def credit_estimate(self, request, context):
        """
        Estimate credits for a Project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def request_access(self, request, context):
        """
        Request Access for a Project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProjectApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=project__pb2.ProjectListRequest.FromString,
                    response_serializer=project__pb2.ProjectListResponse.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=project__pb2.ProjectGetRequest.FromString,
                    response_serializer=project__pb2.ProjectGetResponse.SerializeToString,
            ),
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=project__pb2.ProjectCreateRequest.FromString,
                    response_serializer=project__pb2.ProjectCreateResponse.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=project__pb2.ProjectUpdateRequest.FromString,
                    response_serializer=project__pb2.ProjectUpdateResponse.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=project__pb2.ProjectDeleteRequest.FromString,
                    response_serializer=project__pb2.ProjectDeleteResponse.SerializeToString,
            ),
            'run': grpc.unary_unary_rpc_method_handler(
                    servicer.run,
                    request_deserializer=project__pb2.ProjectRunRequest.FromString,
                    response_serializer=project__pb2.ProjectRunResponse.SerializeToString,
            ),
            'clone': grpc.unary_unary_rpc_method_handler(
                    servicer.clone,
                    request_deserializer=project__pb2.ProjectCloneRequest.FromString,
                    response_serializer=project__pb2.ProjectCloneResponse.SerializeToString,
            ),
            'credit_estimate': grpc.unary_unary_rpc_method_handler(
                    servicer.credit_estimate,
                    request_deserializer=project__pb2.ProjectCreditEstimateRequest.FromString,
                    response_serializer=project__pb2.ProjectCreditEstimateResponse.SerializeToString,
            ),
            'request_access': grpc.unary_unary_rpc_method_handler(
                    servicer.request_access,
                    request_deserializer=project__pb2.ProjectRequestAccessRequest.FromString,
                    response_serializer=project__pb2.ProjectRequestAccessResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'oi.papi.ProjectApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('oi.papi.ProjectApi', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ProjectApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def list(request,
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
            '/oi.papi.ProjectApi/list',
            project__pb2.ProjectListRequest.SerializeToString,
            project__pb2.ProjectListResponse.FromString,
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
    def get(request,
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
            '/oi.papi.ProjectApi/get',
            project__pb2.ProjectGetRequest.SerializeToString,
            project__pb2.ProjectGetResponse.FromString,
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
    def create(request,
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
            '/oi.papi.ProjectApi/create',
            project__pb2.ProjectCreateRequest.SerializeToString,
            project__pb2.ProjectCreateResponse.FromString,
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
    def update(request,
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
            '/oi.papi.ProjectApi/update',
            project__pb2.ProjectUpdateRequest.SerializeToString,
            project__pb2.ProjectUpdateResponse.FromString,
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
    def delete(request,
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
            '/oi.papi.ProjectApi/delete',
            project__pb2.ProjectDeleteRequest.SerializeToString,
            project__pb2.ProjectDeleteResponse.FromString,
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
    def run(request,
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
            '/oi.papi.ProjectApi/run',
            project__pb2.ProjectRunRequest.SerializeToString,
            project__pb2.ProjectRunResponse.FromString,
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
    def clone(request,
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
            '/oi.papi.ProjectApi/clone',
            project__pb2.ProjectCloneRequest.SerializeToString,
            project__pb2.ProjectCloneResponse.FromString,
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
    def credit_estimate(request,
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
            '/oi.papi.ProjectApi/credit_estimate',
            project__pb2.ProjectCreditEstimateRequest.SerializeToString,
            project__pb2.ProjectCreditEstimateResponse.FromString,
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
    def request_access(request,
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
            '/oi.papi.ProjectApi/request_access',
            project__pb2.ProjectRequestAccessRequest.SerializeToString,
            project__pb2.ProjectRequestAccessResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
