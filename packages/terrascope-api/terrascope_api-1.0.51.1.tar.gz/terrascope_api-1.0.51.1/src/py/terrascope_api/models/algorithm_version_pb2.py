# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: algorithm_version.proto
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
    'algorithm_version.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from terrascope_api.models import common_models_pb2 as common__models__pb2
from terrascope_api.models import algorithm_pb2 as algorithm__pb2
try:
  common__models__pb2 = algorithm__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = algorithm__pb2.common_models_pb2

from terrascope_api.models.common_models_pb2 import *
from terrascope_api.models.algorithm_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x61lgorithm_version.proto\x12\x07oi.papi\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x13\x63ommon_models.proto\x1a\x0f\x61lgorithm.proto\"\xa4\x08\n\x08Manifest\x12,\n\x08metadata\x18\x01 \x01(\x0b\x32\x1a.oi.papi.Manifest.Metadata\x12\x31\n\x06inputs\x18\x02 \x03(\x0b\x32!.oi.papi.Manifest.AlgorithmInputs\x12\x33\n\x07outputs\x18\x03 \x03(\x0b\x32\".oi.papi.Manifest.AlgorithmOutputs\x12\x43\n\x14\x63ontainer_parameters\x18\x04 \x01(\x0b\x32%.oi.papi.Manifest.ContainerParameters\x12.\n\tinterface\x18\x05 \x01(\x0b\x32\x1b.oi.papi.Manifest.Interface\x12;\n\x10resource_request\x18\x06 \x01(\x0b\x32!.oi.papi.Manifest.ResourceRequest\x12/\n\nparameters\x18\x07 \x03(\x0b\x32\x1b.oi.papi.Manifest.Parameter\x12\x18\n\x10manifest_version\x18\x08 \x01(\t\x1a\x44\n\x08Metadata\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0f\n\x07version\x18\x04 \x01(\t\x12\x0c\n\x04tags\x18\x02 \x03(\tJ\x04\x08\x01\x10\x02\x1a\x34\n\tInterface\x12\x16\n\x0einterface_type\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x61pter\x18\x02 \x01(\t\x1aO\n\x0f\x41lgorithmInputs\x12\x16\n\x0e\x64\x61ta_type_name\x18\x01 \x01(\t\x12\x11\n\tmin_count\x18\x02 \x01(\r\x12\x11\n\tmax_count\x18\x03 \x01(\r\x1aS\n\x10\x41lgorithmOutputs\x12!\n\x19observation_value_columns\x18\x02 \x03(\t\x12\x16\n\x0e\x64\x61ta_type_name\x18\x03 \x01(\tJ\x04\x08\x01\x10\x02\x1ar\n\x13\x43ontainerParameters\x12\r\n\x05image\x18\x01 \x01(\t\x12;\n\x10resource_request\x18\x02 \x01(\x0b\x32!.oi.papi.Manifest.ResourceRequest\x12\x0f\n\x07\x63ommand\x18\x03 \x03(\t\x1a^\n\x0fResourceRequest\x12\x0b\n\x03gpu\x18\x01 \x01(\r\x12\x11\n\tmemory_gb\x18\x02 \x01(\r\x12\x15\n\rcpu_millicore\x18\x03 \x01(\r\x12\x14\n\x0cmax_input_gb\x18\x04 \x01(\x01\x1a\x8e\x01\n\tParameter\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\r\x12\r\n\x05units\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x0b\n\x03min\x18\x05 \x01(\r\x12\x0b\n\x03max\x18\x06 \x01(\r\x12\x16\n\x0e\x61llowed_values\x18\x07 \x03(\t\x12\x0f\n\x07\x64\x65\x66\x61ult\x18\x08 \x01(\r\"\xe0\x01\n\x10\x41lgorithmVersion\x12\n\n\x02id\x18\x01 \x01(\t\x12%\n\talgorithm\x18\x02 \x01(\x0b\x32\x12.oi.papi.Algorithm\x12\x0f\n\x07version\x18\x03 \x01(\t\x12)\n\x08manifest\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12.\n\ncreated_on\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x0eis_deactivated\x18\x06 \x01(\x08\x12\x15\n\ris_deprecated\x18\x07 \x01(\x08\"\xae\x01\n\x1d\x41lgorithmVersionCreateRequest\x12\x14\n\x0c\x61lgorithm_id\x18\x01 \x01(\t\x12\x32\n\x0fmanifest_struct\x18\x02 \x01(\x0b\x32\x17.google.protobuf.StructH\x00\x12-\n\x10manifest_message\x18\x03 \x01(\x0b\x32\x11.oi.papi.ManifestH\x00\x42\x14\n\x12\x61lgorithm_manifest\"k\n\x1e\x41lgorithmVersionCreateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x34\n\x11\x61lgorithm_version\x18\x02 \x01(\x0b\x32\x19.oi.papi.AlgorithmVersion\"R\n\x1a\x41lgorithmVersionGetRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\'\n\npagination\x18\x02 \x01(\x0b\x32\x13.oi.papi.Pagination\"\x92\x01\n\x1b\x41lgorithmVersionGetResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x35\n\x12\x61lgorithm_versions\x18\x02 \x03(\x0b\x32\x19.oi.papi.AlgorithmVersion\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\"\x84\x02\n\x1b\x41lgorithmVersionListRequest\x12\x14\n\x0c\x61lgorithm_id\x18\x01 \x01(\t\x12\x13\n\x0bsearch_text\x18\x02 \x01(\t\x12\x0b\n\x03tag\x18\x03 \x01(\t\x12\x32\n\x0emin_created_on\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0emax_created_on\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1c\n\x14include_all_versions\x18\x06 \x01(\x08\x12\'\n\npagination\x18\x07 \x01(\x0b\x32\x13.oi.papi.Pagination\"\x93\x01\n\x1c\x41lgorithmVersionListResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x35\n\x12\x61lgorithm_versions\x18\x02 \x03(\x0b\x32\x19.oi.papi.AlgorithmVersion\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\"/\n AlgorithmVersionDeprecateRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"8\n!AlgorithmVersionDeprecateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\"0\n!AlgorithmVersionDeactivateRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"9\n\"AlgorithmVersionDeactivateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\".\n\x1f\x41lgorithmVersionActivateRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"7\n AlgorithmVersionActivateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r2\xc3\x04\n\x13\x41lgorithmVersionApi\x12Y\n\x06\x63reate\x12&.oi.papi.AlgorithmVersionCreateRequest\x1a\'.oi.papi.AlgorithmVersionCreateResponse\x12P\n\x03get\x12#.oi.papi.AlgorithmVersionGetRequest\x1a$.oi.papi.AlgorithmVersionGetResponse\x12S\n\x04list\x12$.oi.papi.AlgorithmVersionListRequest\x1a%.oi.papi.AlgorithmVersionListResponse\x12\x62\n\tdeprecate\x12).oi.papi.AlgorithmVersionDeprecateRequest\x1a*.oi.papi.AlgorithmVersionDeprecateResponse\x12\x65\n\ndeactivate\x12*.oi.papi.AlgorithmVersionDeactivateRequest\x1a+.oi.papi.AlgorithmVersionDeactivateResponse\x12_\n\x08\x61\x63tivate\x12(.oi.papi.AlgorithmVersionActivateRequest\x1a).oi.papi.AlgorithmVersionActivateResponseP\x02P\x03\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'algorithm_version_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MANIFEST']._serialized_start=138
  _globals['_MANIFEST']._serialized_end=1198
  _globals['_MANIFEST_METADATA']._serialized_start=553
  _globals['_MANIFEST_METADATA']._serialized_end=621
  _globals['_MANIFEST_INTERFACE']._serialized_start=623
  _globals['_MANIFEST_INTERFACE']._serialized_end=675
  _globals['_MANIFEST_ALGORITHMINPUTS']._serialized_start=677
  _globals['_MANIFEST_ALGORITHMINPUTS']._serialized_end=756
  _globals['_MANIFEST_ALGORITHMOUTPUTS']._serialized_start=758
  _globals['_MANIFEST_ALGORITHMOUTPUTS']._serialized_end=841
  _globals['_MANIFEST_CONTAINERPARAMETERS']._serialized_start=843
  _globals['_MANIFEST_CONTAINERPARAMETERS']._serialized_end=957
  _globals['_MANIFEST_RESOURCEREQUEST']._serialized_start=959
  _globals['_MANIFEST_RESOURCEREQUEST']._serialized_end=1053
  _globals['_MANIFEST_PARAMETER']._serialized_start=1056
  _globals['_MANIFEST_PARAMETER']._serialized_end=1198
  _globals['_ALGORITHMVERSION']._serialized_start=1201
  _globals['_ALGORITHMVERSION']._serialized_end=1425
  _globals['_ALGORITHMVERSIONCREATEREQUEST']._serialized_start=1428
  _globals['_ALGORITHMVERSIONCREATEREQUEST']._serialized_end=1602
  _globals['_ALGORITHMVERSIONCREATERESPONSE']._serialized_start=1604
  _globals['_ALGORITHMVERSIONCREATERESPONSE']._serialized_end=1711
  _globals['_ALGORITHMVERSIONGETREQUEST']._serialized_start=1713
  _globals['_ALGORITHMVERSIONGETREQUEST']._serialized_end=1795
  _globals['_ALGORITHMVERSIONGETRESPONSE']._serialized_start=1798
  _globals['_ALGORITHMVERSIONGETRESPONSE']._serialized_end=1944
  _globals['_ALGORITHMVERSIONLISTREQUEST']._serialized_start=1947
  _globals['_ALGORITHMVERSIONLISTREQUEST']._serialized_end=2207
  _globals['_ALGORITHMVERSIONLISTRESPONSE']._serialized_start=2210
  _globals['_ALGORITHMVERSIONLISTRESPONSE']._serialized_end=2357
  _globals['_ALGORITHMVERSIONDEPRECATEREQUEST']._serialized_start=2359
  _globals['_ALGORITHMVERSIONDEPRECATEREQUEST']._serialized_end=2406
  _globals['_ALGORITHMVERSIONDEPRECATERESPONSE']._serialized_start=2408
  _globals['_ALGORITHMVERSIONDEPRECATERESPONSE']._serialized_end=2464
  _globals['_ALGORITHMVERSIONDEACTIVATEREQUEST']._serialized_start=2466
  _globals['_ALGORITHMVERSIONDEACTIVATEREQUEST']._serialized_end=2514
  _globals['_ALGORITHMVERSIONDEACTIVATERESPONSE']._serialized_start=2516
  _globals['_ALGORITHMVERSIONDEACTIVATERESPONSE']._serialized_end=2573
  _globals['_ALGORITHMVERSIONACTIVATEREQUEST']._serialized_start=2575
  _globals['_ALGORITHMVERSIONACTIVATEREQUEST']._serialized_end=2621
  _globals['_ALGORITHMVERSIONACTIVATERESPONSE']._serialized_start=2623
  _globals['_ALGORITHMVERSIONACTIVATERESPONSE']._serialized_end=2678
  _globals['_ALGORITHMVERSIONAPI']._serialized_start=2681
  _globals['_ALGORITHMVERSIONAPI']._serialized_end=3260
# @@protoc_insertion_point(module_scope)
