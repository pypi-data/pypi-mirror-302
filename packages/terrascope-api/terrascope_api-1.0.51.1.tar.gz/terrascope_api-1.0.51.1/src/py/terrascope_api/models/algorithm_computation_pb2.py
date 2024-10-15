# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: algorithm_computation.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'algorithm_computation.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from terrascope_api.models import common_models_pb2 as common__models__pb2

from terrascope_api.models.common_models_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1b\x61lgorithm_computation.proto\x12\x07oi.papi\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x13\x63ommon_models.proto\"\xf5\x03\n\x14\x41lgorithmComputation\x12\n\n\x02id\x18\x01 \x01(\t\x12\x19\n\x11\x61oi_collection_id\x18\x02 \x01(\t\x12\x16\n\x0e\x61lgo_config_id\x18\x03 \x01(\t\x12\x0e\n\x06toi_id\x18\x04 \x01(\t\x12\x11\n\tinput_ids\x18\x05 \x03(\t\x12\x30\n\x0csubmitted_on\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x05state\x18\x07 \x01(\x0e\x32#.oi.papi.AlgorithmComputation.State\x12\x38\n\x08progress\x18\x08 \x01(\x0b\x32&.oi.papi.AlgorithmComputation.Progress\x12\x32\n\x0elast_execution\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1aO\n\x08Progress\x12\x0f\n\x07running\x18\x01 \x01(\x01\x12\x11\n\tsucceeded\x18\x02 \x01(\x01\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x01\x12\x0f\n\x07no_data\x18\x04 \x01(\x01\"V\n\x05State\x12\x11\n\rUNKNOWN_STATE\x10\x00\x12\x0f\n\x0bNOT_STARTED\x10\x01\x12\x0f\n\x0bIN_PROGRESS\x10\x02\x12\n\n\x06PAUSED\x10\x03\x12\x0c\n\x08\x43OMPLETE\x10\x04\"k\n!AlgorithmComputationCreateRequest\x12\x1b\n\x13\x61lgorithm_config_id\x18\x01 \x01(\t\x12\x19\n\x11\x61oi_collection_id\x18\x02 \x01(\t\x12\x0e\n\x06toi_id\x18\x03 \x01(\t\"w\n\"AlgorithmComputationCreateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12<\n\x15\x61lgorithm_computation\x18\x02 \x01(\x0b\x32\x1d.oi.papi.AlgorithmComputation\"-\n\x1e\x41lgorithmComputationRunRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"6\n\x1f\x41lgorithmComputationRunResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\"V\n\x1e\x41lgorithmComputationGetRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\'\n\npagination\x18\x02 \x01(\x0b\x32\x13.oi.papi.Pagination\"\x9e\x01\n\x1f\x41lgorithmComputationGetResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12=\n\x16\x61lgorithm_computations\x18\x02 \x03(\x0b\x32\x1d.oi.papi.AlgorithmComputation\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\"\xb2\x02\n\x1f\x41lgorithmComputationListRequest\x12\x32\n\x05state\x18\x01 \x01(\x0e\x32#.oi.papi.AlgorithmComputation.State\x12\x34\n\x10min_submitted_on\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x34\n\x10max_submitted_on\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1b\n\x13\x61lgorithm_config_id\x18\x04 \x01(\t\x12\x0e\n\x06toi_id\x18\x05 \x01(\t\x12\x19\n\x11\x61oi_collection_id\x18\x06 \x01(\t\x12\'\n\npagination\x18\x07 \x01(\x0b\x32\x13.oi.papi.Pagination\"\x9f\x01\n AlgorithmComputationListResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12=\n\x16\x61lgorithm_computations\x18\x02 \x03(\x0b\x32\x1d.oi.papi.AlgorithmComputation\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination2\x8d\x03\n\x17\x41lgorithmComputationApi\x12\x61\n\x06\x63reate\x12*.oi.papi.AlgorithmComputationCreateRequest\x1a+.oi.papi.AlgorithmComputationCreateResponse\x12X\n\x03run\x12\'.oi.papi.AlgorithmComputationRunRequest\x1a(.oi.papi.AlgorithmComputationRunResponse\x12X\n\x03get\x12\'.oi.papi.AlgorithmComputationGetRequest\x1a(.oi.papi.AlgorithmComputationGetResponse\x12[\n\x04list\x12(.oi.papi.AlgorithmComputationListRequest\x1a).oi.papi.AlgorithmComputationListResponseP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'algorithm_computation_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ALGORITHMCOMPUTATION']._serialized_start=95
  _globals['_ALGORITHMCOMPUTATION']._serialized_end=596
  _globals['_ALGORITHMCOMPUTATION_PROGRESS']._serialized_start=429
  _globals['_ALGORITHMCOMPUTATION_PROGRESS']._serialized_end=508
  _globals['_ALGORITHMCOMPUTATION_STATE']._serialized_start=510
  _globals['_ALGORITHMCOMPUTATION_STATE']._serialized_end=596
  _globals['_ALGORITHMCOMPUTATIONCREATEREQUEST']._serialized_start=598
  _globals['_ALGORITHMCOMPUTATIONCREATEREQUEST']._serialized_end=705
  _globals['_ALGORITHMCOMPUTATIONCREATERESPONSE']._serialized_start=707
  _globals['_ALGORITHMCOMPUTATIONCREATERESPONSE']._serialized_end=826
  _globals['_ALGORITHMCOMPUTATIONRUNREQUEST']._serialized_start=828
  _globals['_ALGORITHMCOMPUTATIONRUNREQUEST']._serialized_end=873
  _globals['_ALGORITHMCOMPUTATIONRUNRESPONSE']._serialized_start=875
  _globals['_ALGORITHMCOMPUTATIONRUNRESPONSE']._serialized_end=929
  _globals['_ALGORITHMCOMPUTATIONGETREQUEST']._serialized_start=931
  _globals['_ALGORITHMCOMPUTATIONGETREQUEST']._serialized_end=1017
  _globals['_ALGORITHMCOMPUTATIONGETRESPONSE']._serialized_start=1020
  _globals['_ALGORITHMCOMPUTATIONGETRESPONSE']._serialized_end=1178
  _globals['_ALGORITHMCOMPUTATIONLISTREQUEST']._serialized_start=1181
  _globals['_ALGORITHMCOMPUTATIONLISTREQUEST']._serialized_end=1487
  _globals['_ALGORITHMCOMPUTATIONLISTRESPONSE']._serialized_start=1490
  _globals['_ALGORITHMCOMPUTATIONLISTRESPONSE']._serialized_end=1649
  _globals['_ALGORITHMCOMPUTATIONAPI']._serialized_start=1652
  _globals['_ALGORITHMCOMPUTATIONAPI']._serialized_end=2049
# @@protoc_insertion_point(module_scope)
