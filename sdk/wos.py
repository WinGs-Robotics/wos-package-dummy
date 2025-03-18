# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: wos.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import List

import betterproto


class WOSAPIOperation(betterproto.Enum):
    """Enum representing the possible WOSAPI operations"""

    # Used for unknown operations (shouldn't happen)
    OP_UNKNOWN = 0
    # Used for publishing messages No response
    OP_PUBLISH = 1
    # Used for subscribing to topics Response will be OP_ACK or OP_ERROR
    OP_SUBSCRIBE = 2
    # Used for unsubscribing from topics Response will be OP_ACK or OP_ERROR
    OP_UNSUBSCRIBE = 3
    # Used for making requests Response will be OP_RESULT or OP_ERROR
    OP_REQUEST = 4
    # Used for getting the result of a request or action
    OP_RESULT = 5
    # Used for performing actions Response will be OP_RESULT or OP_ERROR In
    # between, there may be multiple OP_FEEDBACK messages
    OP_ACTION = 6
    # Used for sending feedback
    OP_FEEDBACK = 7
    # Used for cancelling a request or action Response will be OP_ACK or OP_ERROR
    OP_CANCEL = 8
    # Used for registering a service Response will be OP_ACK or OP_ERROR
    OP_REGISTER_SERVICE = 9
    # Used for removing a service Response will be OP_ACK or OP_ERROR
    OP_REMOVE_SERVICE = 10
    # Used for sending an error message
    OP_ERROR = 11
    # Used for acknowledging a message This is used in response to OP_PUBLISH,
    # OP_SUBSCRIBE, OP_UNSUBSCRIBE, OP_REGISTER_SERVICE and OP_REMOVE_SERVICE
    OP_ACK = 12


class WOSDataFieldCollection(betterproto.Enum):
    COLLECTION_SINGLE = 0
    COLLECTION_LIST = 1
    COLLECTION_MAP = 2


class WOSNodeState(betterproto.Enum):
    SCHEDULED = 0
    PENDING = 1
    STARTED = 2
    RUNNING = 3
    COMPLETED = 4
    FAILED = 5
    STACKED = 6


class WOSNodePolicy(betterproto.Enum):
    IGNORE = 0
    RESTART = 1
    EMERGENCY = 2


@dataclass
class WOSPackageRegistration(betterproto.Message):
    name: str = betterproto.string_field(1)
    path: str = betterproto.string_field(2)
    info: "WOSPackageInfo" = betterproto.message_field(3)


@dataclass
class WOSPackageDefinition(betterproto.Message):
    # path-regex or path-regex array wos will scan all files under this regex
    # that is a valid proto file
    proto: List[str] = betterproto.string_field(1)
    # path/to/www, we will host the webservice for you [endpoint]:port, we will
    # iframe the webapp
    ui: str = betterproto.string_field(2)
    # The node to run when start the wos
    main: List["WOSStartNodeRequest"] = betterproto.message_field(3)
    # These parameters will be reported to user local config where end user can
    # change the value
    parameters: str = betterproto.string_field(4)
    # You can also choose to specify the type of the parameters which in turn
    # will be validated And provide approprate UI for the user to change the
    # value
    parameters_type: str = betterproto.string_field(5)
    # Map of the node definitions where key is the node key
    nodes: "WOSNodeDefinition" = betterproto.message_field(6)
    # Map of the services where key is the service name
    services: "WOSServiceDefinition" = betterproto.message_field(7)
    # Map of the dependencies where key is the package name and value is the
    # version constraint Or the path to get the package. Suporrted values are: -
    # git://<url>#<branch> - file://<path> - http[s]://<url> (to download the
    # entire package in zip, tar.gz, or tar.xz. And it should have a wos.yml file
    # in its root folder)
    dependencies: str = betterproto.string_field(8)


@dataclass
class WOSNodeInfo(betterproto.Message):
    id: str = betterproto.string_field(1)
    definition: "WOSNodeDefinition" = betterproto.message_field(2)
    request: "WOSStartNodeRequest" = betterproto.message_field(3)
    parameters: str = betterproto.string_field(4)
    state: "WOSNodeState" = betterproto.enum_field(5)
    status: str = betterproto.string_field(6)
    parent: str = betterproto.string_field(7)


@dataclass
class WOSAPIFeedback(betterproto.Message):
    """Use for Op = OP_FEEDBACK"""

    # from zero to one
    progress: float = betterproto.float_field(1)
    # a status message provided by service handler
    status: str = betterproto.string_field(2)


@dataclass
class WOSTopicDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    type: str = betterproto.string_field(2)
    description: str = betterproto.string_field(3)


@dataclass
class WOSServiceInfo(betterproto.Message):
    resource: str = betterproto.string_field(1)
    instance: str = betterproto.string_field(2)


@dataclass
class WOSAPIMessage(betterproto.Message):
    """
    WOSAPI message definition This is the only payload that is sent over the
    wire
    """

    # Unique ID for the message within same connection A request and its response
    # will have the same ID Maybe empty for some transports
    id: int = betterproto.uint64_field(1)
    timestamp: datetime = betterproto.message_field(2)
    # Operation to be performed
    op: "WOSAPIOperation" = betterproto.enum_field(3)
    # The resource to be operated on
    resource: str = betterproto.string_field(4)
    # The topic in this resource
    topic: str = betterproto.string_field(5)
    # The payload of the message In WOS, this can be either bytes of string Or
    # another protobuf message
    payload: bytes = betterproto.bytes_field(6)
    # The instance of the resource, if there are multiple services
    instance: str = betterproto.string_field(7)
    # Machine ID for the route (reserved and unused right now)
    machine: str = betterproto.string_field(8)


@dataclass
class WOSActionDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    input: str = betterproto.string_field(2)
    output: str = betterproto.string_field(3)
    singleton: bool = betterproto.bool_field(4)
    description: str = betterproto.string_field(5)


@dataclass
class WOSNodeInfoList(betterproto.Message):
    nodes: "WOSNodeInfo" = betterproto.message_field(1)


@dataclass
class WOSSetting(betterproto.Message):
    package_settings: "WOSPackageSetting" = betterproto.message_field(1)
    port: str = betterproto.string_field(2)
    fps: int = betterproto.uint32_field(3)
    beta: bool = betterproto.bool_field(4)
    debug: bool = betterproto.bool_field(5)


@dataclass
class WOSDescription(betterproto.Message):
    packages: "WOSPackageRegistration" = betterproto.message_field(1)
    data_types: "WOSDataTypeDefinition" = betterproto.message_field(2)
    data_enums: "WOSDataTypeEnumDefinition" = betterproto.message_field(3)
    nodes: "WOSNodeDefinition" = betterproto.message_field(4)
    services: "WOSServiceDefinition" = betterproto.message_field(5)
    setting: "WOSSetting" = betterproto.message_field(6)


@dataclass
class WOSDataTypeDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    editor: str = betterproto.string_field(3)
    validator: str = betterproto.string_field(4)
    fields: List["WOSDataFieldDefinition"] = betterproto.message_field(5)


@dataclass
class WOSRequestDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    input: str = betterproto.string_field(2)
    output: str = betterproto.string_field(3)
    description: str = betterproto.string_field(4)


@dataclass
class WOSHeartbeat(betterproto.Message):
    num_nodes_running: int = betterproto.int32_field(1)
    num_nodes: int = betterproto.int32_field(2)
    num_services: int = betterproto.int32_field(3)
    num_goroutines: int = betterproto.int32_field(4)
    num_connections: int = betterproto.int32_field(5)


@dataclass
class WOSDiagnoseInfo(betterproto.Message):
    # The time of the performance info
    time: datetime = betterproto.message_field(1)
    # The CPU usage in percent
    cpu: float = betterproto.double_field(2)
    # The memory usage in mb
    memory: float = betterproto.double_field(3)
    # The total memory in mb
    total_memory: float = betterproto.double_field(4)
    # The memory usage in percent
    num_go_routines: int = betterproto.int32_field(5)
    # The go routine info
    go_routine_info: str = betterproto.string_field(6)


@dataclass
class WOSPackageInfo(betterproto.Message):
    # @scope/pkg-name only use lower char,number, underscore
    name: str = betterproto.string_field(1)
    # any string in markdown [Image in markdown are searched from package path]
    # default to README.md if exists
    description: str = betterproto.string_field(2)
    # semver x.x.x # default to 0.0.0
    version: str = betterproto.string_field(3)
    # path/to/image
    icon: str = betterproto.string_field(4)
    # SPDX syntax https://spdx.dev/use/specifications/
    license: str = betterproto.string_field(5)
    # homepage url
    homepage: str = betterproto.string_field(6)
    # author name:  "name <email> (url)"
    author: str = betterproto.string_field(7)
    # The package definition for available nodes and etc...
    definition: "WOSPackageDefinition" = betterproto.message_field(8)
    # The dev override for the package when run with wos dev
    dev_overwrite: "WOSPackageDefinition" = betterproto.message_field(9)
    # list of cmd to run for "wos build". This will also run when user install
    # your package usually use in source-based release, that requires user to
    # build on their machine should only be used as local docker image builder.
    # Try not to assume user's environment
    build_steps: List[str] = betterproto.string_field(10)


@dataclass
class WOSDataFieldDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    index: int = betterproto.int32_field(3)
    editor: str = betterproto.string_field(4)
    validator: str = betterproto.string_field(5)
    type: str = betterproto.string_field(6)
    collection: "WOSDataFieldCollection" = betterproto.enum_field(7)
    default: bytes = betterproto.bytes_field(8)


@dataclass
class WOSPackageSetting(betterproto.Message):
    parameters: str = betterproto.string_field(1)


@dataclass
class WOSNodeDefinition(betterproto.Message):
    # Unique key for the node (used in key field in WOSNodeConfig)
    name: str = betterproto.string_field(1)
    # additional environment variables to pass to the command for http[s]
    # request, this will be the headers
    env: str = betterproto.string_field(2)
    # arguments to pass to the command this is a string that will be parsed by
    # the command for http[s] request, this will be the request type: GET, POST,
    # PUT, DELETE and etc..
    args: List[str] = betterproto.string_field(3)
    # resource identifier for the node the schema define how to run the node
    # starts with container://  treat this as a docker container run starts with
    # http[s]://    treat this as a http request starts with python://     treat
    # this as a python script starts with service://    treat this as a service
    # request starts with (no schema)  a command starts from the your package
    # root (or workspace root)
    url: str = betterproto.string_field(4)
    # additional information for the node based on the node type (url schema),
    # this can be used to pass additional information container:// NETWORK:
    # "bridge" or "host" VOLUMES: map of volumes in the form of <path in
    # host>:<path in container>,<path in host>:<path in container> PORTS: map of
    # ports in the form of <host>:<container>,<host>:<container> (used in bridge
    # mode) PRESIST: "true" or "false". By default, the container will be deleted
    # after the node is done USER: user to run the container as http[s]:// FILE:
    # file to upload (the value is the path to the file)
    config: str = betterproto.string_field(5)
    # list of tags for the frontend filtering
    tags: List[str] = betterproto.string_field(6)
    # For container & host process, this will be the command to run on prestart
    # stage
    prestart_args: List[str] = betterproto.string_field(7)
    # For container & host process, this will be the command to run on start
    # stage
    onstart_args: List[str] = betterproto.string_field(8)
    # List of the node to run as dependencies before this node
    deps: "WOSStartNodeRequest" = betterproto.message_field(9)
    # List of the shared dependencies for the node
    shared_deps: List[str] = betterproto.string_field(10)
    # Priority of the node This will be used to determine the order of the node
    # to run higher priority will run first
    priority: int = betterproto.uint32_field(11)
    # What will happen when the node is failed IGNORE: ignore the failure
    # RESTART: restart the node EMERGENCY: stop the wos and other running nodes
    # Use Emergency for mission critical nodes
    policy: "WOSNodePolicy" = betterproto.enum_field(12)
    # The package name of the node auto filled by wos during runtime
    package: str = betterproto.string_field(13)
    # will wait until the service is available to announce the node is running
    service: str = betterproto.string_field(14)
    # timeout in seconds for the service to be available or the node will be
    # failed default to 15 seconds
    timeout: int = betterproto.int32_field(15)


@dataclass
class WOSDataTypeEnumValue(betterproto.Message):
    name: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    value: int = betterproto.int32_field(3)


@dataclass
class WOSServiceDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    singleton: bool = betterproto.bool_field(2)
    topics: "WOSTopicDefinition" = betterproto.message_field(3)
    requests: "WOSRequestDefinition" = betterproto.message_field(4)
    actions: "WOSActionDefinition" = betterproto.message_field(5)
    package: str = betterproto.string_field(6)


@dataclass
class WOSDataTypeEnumDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    values: List["WOSDataTypeEnumValue"] = betterproto.message_field(3)


@dataclass
class WOSStartNodeRequest(betterproto.Message):
    # If we want to presist the run info, we can provide the id
    id: str = betterproto.string_field(1)
    # The node to run in node-entity format node-entity format: <package-
    # name>/<node-key>
    name: str = betterproto.string_field(2)
    # The node input
    parameters: str = betterproto.string_field(3)
    instance: str = betterproto.string_field(4)
    # Used by wos internally
    extra: str = betterproto.string_field(5)


@dataclass
class WOSServiceList(betterproto.Message):
    services: "WOSServiceInfo" = betterproto.message_field(1)
