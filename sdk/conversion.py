from google.protobuf import any_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2
from google.protobuf import timestamp_pb2
from google.protobuf import wrappers_pb2
import datetime
import warnings


def convert_to_bytes(value, type_str):
    """Convert a Python value to protobuf encoded bytes based on the specified type."""
    try:
        if type_str == "google.protobuf.Timestamp":
            proto = timestamp_pb2.Timestamp()
            if isinstance(value, datetime.datetime):
                proto.FromDatetime(value)
            elif isinstance(value, dict):
                proto.seconds = value.get("seconds", 0)
                proto.nanos = value.get("nanos", 0)
            return proto.SerializeToString()

        elif type_str == "google.protobuf.Duration":
            proto = duration_pb2.Duration()
            if isinstance(value, datetime.timedelta):
                seconds = value.seconds + value.days * 86400
                nanos = value.microseconds * 1000
                proto.seconds = seconds
                proto.nanos = nanos
            elif isinstance(value, dict):
                proto.seconds = value.get("seconds", 0)
                proto.nanos = value.get("nanos", 0)
            return proto.SerializeToString()

        elif type_str == "google.protobuf.Struct":
            proto = struct_pb2.Struct()
            proto.update(value)
            return proto.SerializeToString()

        elif type_str == "google.protobuf.Any":
            proto = any_pb2.Any()
            if isinstance(value, dict):
                if "type_url" in value and "value" in value:
                    proto.type_url = value["type_url"]
                    proto.value = (
                        value["value"]
                        if isinstance(value["value"], bytes)
                        else bytes(value["value"])
                    )
            return proto.SerializeToString()

        elif type_str == "google.protobuf.Empty":
            proto = empty_pb2.Empty()
            return proto.SerializeToString()

        elif type_str == "google.protobuf.BoolValue":
            proto = wrappers_pb2.BoolValue(value=bool(value))
            return proto.SerializeToString()

        elif type_str == "google.protobuf.StringValue":
            proto = wrappers_pb2.StringValue(value=str(value))
            return proto.SerializeToString()

        elif type_str == "google.protobuf.BytesValue":
            proto = wrappers_pb2.BytesValue(
                value=value if isinstance(value, bytes) else bytes(value)
            )
            return proto.SerializeToString()

        elif type_str == "google.protobuf.Int32Value":
            proto = wrappers_pb2.Int32Value(value=int(value))
            return proto.SerializeToString()

        elif type_str == "google.protobuf.Int64Value":
            proto = wrappers_pb2.Int64Value(value=int(value))
            return proto.SerializeToString()

        elif type_str == "google.protobuf.UInt32Value":
            proto = wrappers_pb2.UInt32Value(value=int(value))
            return proto.SerializeToString()

        elif type_str == "google.protobuf.UInt64Value":
            proto = wrappers_pb2.UInt64Value(value=int(value))
            return proto.SerializeToString()

        elif type_str == "google.protobuf.DoubleValue":
            proto = wrappers_pb2.DoubleValue(value=float(value))
            return proto.SerializeToString()

        elif type_str == "google.protobuf.FloatValue":
            proto = wrappers_pb2.FloatValue(value=float(value))
            return proto.SerializeToString()

        elif type_str == "google.protobuf.FieldMask":
            proto = field_mask_pb2.FieldMask()
            if isinstance(value, dict) and "paths" in value:
                proto.paths.extend(value["paths"])
            elif isinstance(value, list):
                proto.paths.extend(value)
            return proto.SerializeToString()

        else:
            warnings.warn(f"Unknown type: {type_str}")
            return bytes()

    except Exception as e:
        warnings.warn(f"Error converting to bytes for type {type_str}: {str(e)}")
        return bytes()


def convert_from_bytes(bytes_data, type_str):
    """Convert protobuf encoded bytes to native Python values based on the specified type."""
    try:
        if type_str == "google.protobuf.Timestamp":
            proto = timestamp_pb2.Timestamp()
            proto.ParseFromString(bytes_data)
            return proto.ToDatetime()

        elif type_str == "google.protobuf.Duration":
            proto = duration_pb2.Duration()
            proto.ParseFromString(bytes_data)
            return datetime.timedelta(
                seconds=proto.seconds, microseconds=proto.nanos // 1000
            )

        elif type_str == "google.protobuf.Struct":
            proto = struct_pb2.Struct()
            proto.ParseFromString(bytes_data)
            return dict(proto)

        elif type_str == "google.protobuf.Any":
            proto = any_pb2.Any()
            proto.ParseFromString(bytes_data)
            return {"type_url": proto.type_url, "value": proto.value}

        elif type_str == "google.protobuf.Empty":
            proto = empty_pb2.Empty()
            proto.ParseFromString(bytes_data)
            return {}

        elif type_str == "google.protobuf.BoolValue":
            proto = wrappers_pb2.BoolValue()
            proto.ParseFromString(bytes_data)
            return proto.value

        elif type_str == "google.protobuf.StringValue":
            proto = wrappers_pb2.StringValue()
            proto.ParseFromString(bytes_data)
            return proto.value

        elif type_str == "google.protobuf.BytesValue":
            proto = wrappers_pb2.BytesValue()
            proto.ParseFromString(bytes_data)
            return proto.value

        elif type_str == "google.protobuf.Int32Value":
            proto = wrappers_pb2.Int32Value()
            proto.ParseFromString(bytes_data)
            return proto.value

        elif type_str == "google.protobuf.Int64Value":
            proto = wrappers_pb2.Int64Value()
            proto.ParseFromString(bytes_data)
            return proto.value

        elif type_str == "google.protobuf.UInt32Value":
            proto = wrappers_pb2.UInt32Value()
            proto.ParseFromString(bytes_data)
            return proto.value

        elif type_str == "google.protobuf.UInt64Value":
            proto = wrappers_pb2.UInt64Value()
            proto.ParseFromString(bytes_data)
            return proto.value

        elif type_str == "google.protobuf.DoubleValue":
            proto = wrappers_pb2.DoubleValue()
            proto.ParseFromString(bytes_data)
            return proto.value

        elif type_str == "google.protobuf.FloatValue":
            proto = wrappers_pb2.FloatValue()
            proto.ParseFromString(bytes_data)
            return proto.value

        elif type_str == "google.protobuf.FieldMask":
            proto = field_mask_pb2.FieldMask()
            proto.ParseFromString(bytes_data)
            return proto.paths

        else:
            warnings.warn(f"Unknown type: {type_str}")
            return None

    except Exception as e:
        warnings.warn(f"Error converting from bytes for type {type_str}: {str(e)}")
        return None
