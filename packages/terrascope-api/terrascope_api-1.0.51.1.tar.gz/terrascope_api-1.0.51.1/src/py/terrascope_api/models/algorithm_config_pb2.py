# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: algorithm_config.proto
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
    'algorithm_config.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from terrascope_api.models import common_models_pb2 as common__models__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from terrascope_api.models import algorithm_pb2 as algorithm__pb2
try:
  common__models__pb2 = algorithm__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = algorithm__pb2.common_models_pb2
from terrascope_api.models import algorithm_version_pb2 as algorithm__version__pb2
try:
  common__models__pb2 = algorithm__version__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = algorithm__version__pb2.common_models_pb2
try:
  algorithm__pb2 = algorithm__version__pb2.algorithm__pb2
except AttributeError:
  algorithm__pb2 = algorithm__version__pb2.algorithm_pb2
try:
  common__models__pb2 = algorithm__version__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = algorithm__version__pb2.common_models_pb2

from terrascope_api.models.common_models_pb2 import *
from terrascope_api.models.algorithm_pb2 import *
from terrascope_api.models.algorithm_version_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16\x61lgorithm_config.proto\x12\x07oi.papi\x1a\x1cgoogle/protobuf/struct.proto\x1a\x13\x63ommon_models.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x0f\x61lgorithm.proto\x1a\x17\x61lgorithm_version.proto\"\xbf\x02\n\x0f\x41lgorithmConfig\x12\n\n\x02id\x18\x01 \x01(\t\x12\x34\n\x11\x61lgorithm_version\x18\x02 \x01(\x0b\x32\x19.oi.papi.AlgorithmVersion\x12\'\n\x06\x63onfig\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\talgorithm\x18\x04 \x01(\x0b\x32\x12.oi.papi.Algorithm\x12.\n\ncreated_on\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x0eis_deactivated\x18\x06 \x01(\x08\x12\x15\n\ris_deprecated\x18\x07 \x01(\x08\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\t \x01(\t\x12\x18\n\x10resources_locked\x18\n \x01(\x08\"\x88\x01\n\x1c\x41lgorithmConfigCreateRequest\x12\x1c\n\x14\x61lgorithm_version_id\x18\x01 \x01(\t\x12\'\n\x06params\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\"h\n\x1d\x41lgorithmConfigCreateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x32\n\x10\x61lgorithm_config\x18\x02 \x01(\x0b\x32\x18.oi.papi.AlgorithmConfig\"]\n\x1c\x41lgorithmConfigUpdateRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x31\n\x10\x61lgorithm_config\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\"4\n\x1d\x41lgorithmConfigUpdateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\"\x85\x01\n\x19\x41lgorithmConfigGetRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\x14\n\x0c\x61lgorithm_id\x18\x02 \x01(\t\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\x12\x1c\n\x14\x61lgorithm_version_id\x18\x04 \x01(\t\"\x8f\x01\n\x1a\x41lgorithmConfigGetResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x33\n\x11\x61lgorithm_configs\x18\x02 \x03(\x0b\x32\x18.oi.papi.AlgorithmConfig\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\"\x93\x02\n\x1a\x41lgorithmConfigListRequest\x12\x14\n\x0c\x61lgorithm_id\x18\x01 \x01(\t\x12\x1c\n\x14\x61lgorithm_version_id\x18\x02 \x01(\t\x12\x13\n\x0bsearch_text\x18\x03 \x01(\t\x12\x32\n\x0emin_created_on\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0emax_created_on\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1b\n\x13include_deactivated\x18\x06 \x01(\x08\x12\'\n\npagination\x18\x07 \x01(\x0b\x32\x13.oi.papi.Pagination\"\x90\x01\n\x1b\x41lgorithmConfigListResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x33\n\x11\x61lgorithm_configs\x18\x02 \x03(\x0b\x32\x18.oi.papi.AlgorithmConfig\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\"+\n\x1c\x41lgorithmConfigDeleteRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"4\n\x1d\x41lgorithmConfigDeleteResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\".\n\x1f\x41lgorithmConfigDeprecateRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"7\n AlgorithmConfigDeprecateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\"/\n AlgorithmConfigDeactivateRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"8\n!AlgorithmConfigDeactivateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r2\x89\x05\n\x12\x41lgorithmConfigApi\x12W\n\x06\x63reate\x12%.oi.papi.AlgorithmConfigCreateRequest\x1a&.oi.papi.AlgorithmConfigCreateResponse\x12N\n\x03get\x12\".oi.papi.AlgorithmConfigGetRequest\x1a#.oi.papi.AlgorithmConfigGetResponse\x12Q\n\x04list\x12#.oi.papi.AlgorithmConfigListRequest\x1a$.oi.papi.AlgorithmConfigListResponse\x12W\n\x06update\x12%.oi.papi.AlgorithmConfigUpdateRequest\x1a&.oi.papi.AlgorithmConfigUpdateResponse\x12`\n\tdeprecate\x12(.oi.papi.AlgorithmConfigDeprecateRequest\x1a).oi.papi.AlgorithmConfigDeprecateResponse\x12\x63\n\ndeactivate\x12).oi.papi.AlgorithmConfigDeactivateRequest\x1a*.oi.papi.AlgorithmConfigDeactivateResponse\x12W\n\x06\x64\x65lete\x12%.oi.papi.AlgorithmConfigDeleteRequest\x1a&.oi.papi.AlgorithmConfigDeleteResponseP\x01P\x03P\x04\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'algorithm_config_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ALGORITHMCONFIG']._serialized_start=162
  _globals['_ALGORITHMCONFIG']._serialized_end=481
  _globals['_ALGORITHMCONFIGCREATEREQUEST']._serialized_start=484
  _globals['_ALGORITHMCONFIGCREATEREQUEST']._serialized_end=620
  _globals['_ALGORITHMCONFIGCREATERESPONSE']._serialized_start=622
  _globals['_ALGORITHMCONFIGCREATERESPONSE']._serialized_end=726
  _globals['_ALGORITHMCONFIGUPDATEREQUEST']._serialized_start=728
  _globals['_ALGORITHMCONFIGUPDATEREQUEST']._serialized_end=821
  _globals['_ALGORITHMCONFIGUPDATERESPONSE']._serialized_start=823
  _globals['_ALGORITHMCONFIGUPDATERESPONSE']._serialized_end=875
  _globals['_ALGORITHMCONFIGGETREQUEST']._serialized_start=878
  _globals['_ALGORITHMCONFIGGETREQUEST']._serialized_end=1011
  _globals['_ALGORITHMCONFIGGETRESPONSE']._serialized_start=1014
  _globals['_ALGORITHMCONFIGGETRESPONSE']._serialized_end=1157
  _globals['_ALGORITHMCONFIGLISTREQUEST']._serialized_start=1160
  _globals['_ALGORITHMCONFIGLISTREQUEST']._serialized_end=1435
  _globals['_ALGORITHMCONFIGLISTRESPONSE']._serialized_start=1438
  _globals['_ALGORITHMCONFIGLISTRESPONSE']._serialized_end=1582
  _globals['_ALGORITHMCONFIGDELETEREQUEST']._serialized_start=1584
  _globals['_ALGORITHMCONFIGDELETEREQUEST']._serialized_end=1627
  _globals['_ALGORITHMCONFIGDELETERESPONSE']._serialized_start=1629
  _globals['_ALGORITHMCONFIGDELETERESPONSE']._serialized_end=1681
  _globals['_ALGORITHMCONFIGDEPRECATEREQUEST']._serialized_start=1683
  _globals['_ALGORITHMCONFIGDEPRECATEREQUEST']._serialized_end=1729
  _globals['_ALGORITHMCONFIGDEPRECATERESPONSE']._serialized_start=1731
  _globals['_ALGORITHMCONFIGDEPRECATERESPONSE']._serialized_end=1786
  _globals['_ALGORITHMCONFIGDEACTIVATEREQUEST']._serialized_start=1788
  _globals['_ALGORITHMCONFIGDEACTIVATEREQUEST']._serialized_end=1835
  _globals['_ALGORITHMCONFIGDEACTIVATERESPONSE']._serialized_start=1837
  _globals['_ALGORITHMCONFIGDEACTIVATERESPONSE']._serialized_end=1893
  _globals['_ALGORITHMCONFIGAPI']._serialized_start=1896
  _globals['_ALGORITHMCONFIGAPI']._serialized_end=2545
# @@protoc_insertion_point(module_scope)
