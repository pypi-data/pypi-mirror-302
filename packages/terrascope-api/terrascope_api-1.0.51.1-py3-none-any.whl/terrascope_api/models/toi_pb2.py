# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: toi.proto
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
    'toi.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from terrascope_api.models import common_models_pb2 as common__models__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

from terrascope_api.models.common_models_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ttoi.proto\x12\x07oi.papi\x1a\x13\x63ommon_models.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xb5\x01\n\x07\x43\x61\x64\x65nce\x12-\n\tfrequency\x18\x01 \x01(\x0e\x32\x1a.oi.papi.Cadence.Frequency\x12\r\n\x05value\x18\x02 \x01(\r\"l\n\tFrequency\x12\x15\n\x11UNKNOWN_FREQUENCY\x10\x00\x12\x0c\n\x08MINUTELY\x10\x01\x12\n\n\x06HOURLY\x10\x02\x12\t\n\x05\x44\x41ILY\x10\x03\x12\n\n\x06WEEKLY\x10\x04\x12\x0b\n\x07MONTHLY\x10\x05\x12\n\n\x06YEARLY\x10\x06\"J\n\nRecurrence\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04rule\x18\x02 \x01(\t\x12\"\n\x08\x64uration\x18\x03 \x01(\x0b\x32\x10.oi.papi.Cadence\"\xe6\x01\n\x03TOI\x12\n\n\x02id\x18\x01 \x01(\t\x12/\n\x0bstart_local\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0c\x66inish_local\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x0brecurrences\x18\x04 \x03(\x0b\x32\x13.oi.papi.Recurrence\x12\x31\n\rexclude_dates\x18\x05 \x03(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0b\x64\x65scription\x18\x06 \x01(\t\"\xe7\x01\n\x10TOICreateRequest\x12/\n\x0bstart_local\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0c\x66inish_local\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x0brecurrences\x18\x03 \x03(\x0b\x32\x13.oi.papi.Recurrence\x12\x31\n\rexclude_dates\x18\x04 \x03(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\"C\n\x11TOICreateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x19\n\x03toi\x18\x02 \x01(\x0b\x32\x0c.oi.papi.TOI\"\x1f\n\x10TOIDeleteRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"(\n\x11TOIDeleteResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\"E\n\rTOIGetRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\'\n\npagination\x18\x02 \x01(\x0b\x32\x13.oi.papi.Pagination\"q\n\x0eTOIGetResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12!\n\x0btoi_objects\x18\x02 \x03(\x0b\x32\x0c.oi.papi.TOI\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\"N\n\x0eTOIListRequest\x12\x13\n\x0bsearch_text\x18\x01 \x01(\t\x12\'\n\npagination\x18\x02 \x01(\x0b\x32\x13.oi.papi.Pagination\"r\n\x0fTOIListResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12!\n\x0btoi_objects\x18\x02 \x03(\x0b\x32\x0c.oi.papi.TOI\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination2\xfd\x01\n\x06TOIApi\x12?\n\x06\x63reate\x12\x19.oi.papi.TOICreateRequest\x1a\x1a.oi.papi.TOICreateResponse\x12?\n\x06\x64\x65lete\x12\x19.oi.papi.TOIDeleteRequest\x1a\x1a.oi.papi.TOIDeleteResponse\x12\x36\n\x03get\x12\x16.oi.papi.TOIGetRequest\x1a\x17.oi.papi.TOIGetResponse\x12\x39\n\x04list\x12\x17.oi.papi.TOIListRequest\x1a\x18.oi.papi.TOIListResponseP\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'toi_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CADENCE']._serialized_start=77
  _globals['_CADENCE']._serialized_end=258
  _globals['_CADENCE_FREQUENCY']._serialized_start=150
  _globals['_CADENCE_FREQUENCY']._serialized_end=258
  _globals['_RECURRENCE']._serialized_start=260
  _globals['_RECURRENCE']._serialized_end=334
  _globals['_TOI']._serialized_start=337
  _globals['_TOI']._serialized_end=567
  _globals['_TOICREATEREQUEST']._serialized_start=570
  _globals['_TOICREATEREQUEST']._serialized_end=801
  _globals['_TOICREATERESPONSE']._serialized_start=803
  _globals['_TOICREATERESPONSE']._serialized_end=870
  _globals['_TOIDELETEREQUEST']._serialized_start=872
  _globals['_TOIDELETEREQUEST']._serialized_end=903
  _globals['_TOIDELETERESPONSE']._serialized_start=905
  _globals['_TOIDELETERESPONSE']._serialized_end=945
  _globals['_TOIGETREQUEST']._serialized_start=947
  _globals['_TOIGETREQUEST']._serialized_end=1016
  _globals['_TOIGETRESPONSE']._serialized_start=1018
  _globals['_TOIGETRESPONSE']._serialized_end=1131
  _globals['_TOILISTREQUEST']._serialized_start=1133
  _globals['_TOILISTREQUEST']._serialized_end=1211
  _globals['_TOILISTRESPONSE']._serialized_start=1213
  _globals['_TOILISTRESPONSE']._serialized_end=1327
  _globals['_TOIAPI']._serialized_start=1330
  _globals['_TOIAPI']._serialized_end=1583
# @@protoc_insertion_point(module_scope)
