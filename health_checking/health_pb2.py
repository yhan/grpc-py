# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: health.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0chealth.proto\x12\x0egrpc_health.v1\"%\n\x12HealthCheckRequest\x12\x0f\n\x07service\x18\x01 \x01(\t\"\x94\x01\n\x13HealthCheckResponse\x12\x41\n\x06status\x18\x01 \x01(\x0e\x32\x31.grpc_health.v1.HealthCheckResponse.ServingStatus\":\n\rServingStatus\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x07SERVING\x10\x01\x12\x0f\n\x0bNOT_SERVING\x10\x02\x32Z\n\x06Health\x12P\n\x05\x43heck\x12\".grpc_health.v1.HealthCheckRequest\x1a#.grpc_health.v1.HealthCheckResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'health_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_HEALTHCHECKREQUEST']._serialized_start=32
  _globals['_HEALTHCHECKREQUEST']._serialized_end=69
  _globals['_HEALTHCHECKRESPONSE']._serialized_start=72
  _globals['_HEALTHCHECKRESPONSE']._serialized_end=220
  _globals['_HEALTHCHECKRESPONSE_SERVINGSTATUS']._serialized_start=162
  _globals['_HEALTHCHECKRESPONSE_SERVINGSTATUS']._serialized_end=220
  _globals['_HEALTH']._serialized_start=222
  _globals['_HEALTH']._serialized_end=312
# @@protoc_insertion_point(module_scope)
