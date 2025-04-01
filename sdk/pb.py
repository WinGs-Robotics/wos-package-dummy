# Merged imports from all Python files
from . import protobuf
from dataclasses import dataclass
from datetime import datetime
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from typing import List
import betterproto

# =============== Source Code ===============


# Code from: wosdummy.py
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: wosdummy.proto
# plugin: python-betterproto



class PostVisibility(betterproto.Enum):
    """Post visibility"""

    POST_VISIBILITY_UNSPECIFIED = 0
    POST_VISIBILITY_PUBLIC = 1
    POST_VISIBILITY_PRIVATE = 2
    POST_VISIBILITY_FRIENDS_ONLY = 3


class UserStatus(betterproto.Enum):
    """User status"""

    USER_STATUS_UNSPECIFIED = 0
    USER_STATUS_ACTIVE = 1
    USER_STATUS_INACTIVE = 2
    USER_STATUS_BANNED = 3


@dataclass
class CreateUserRequest(betterproto.Message):
    """Create user request"""

    username: str = betterproto.string_field(1)
    email: str = betterproto.string_field(2)
    password: str = betterproto.string_field(3)
    display_name: str = betterproto.string_field(4)
    profile_picture_url: str = betterproto.string_field(5)
    bio: str = betterproto.string_field(6)


@dataclass
class UpdatePostRequest(betterproto.Message):
    """Update post request"""

    id: str = betterproto.string_field(1)
    # Fields to update
    title: str = betterproto.string_field(2)
    content: str = betterproto.string_field(3)
    image_urls: List[str] = betterproto.string_field(4)
    tags: List[str] = betterproto.string_field(5)
    visibility: "PostVisibility" = betterproto.enum_field(6)
    clear_images: bool = betterproto.bool_field(7)
    clear_tags: bool = betterproto.bool_field(8)


@dataclass
class ListPostsRequest(betterproto.Message):
    """List posts request with pagination"""

    page_size: int = betterproto.int32_field(1)
    page_token: str = betterproto.string_field(2)
    visibility_filter: "PostVisibility" = betterproto.enum_field(3)
    tag_filters: List[str] = betterproto.string_field(4)


@dataclass
class ListUsersRequest(betterproto.Message):
    """List users request with pagination"""

    page_size: int = betterproto.int32_field(1)
    page_token: str = betterproto.string_field(2)
    status_filter: "UserStatus" = betterproto.enum_field(3)


@dataclass
class UserDeletedEvent(betterproto.Message):
    user_id: str = betterproto.string_field(1)


@dataclass
class LikePostResponse(betterproto.Message):
    """Like post response"""

    updated_like_count: int = betterproto.int32_field(1)


@dataclass
class ListUsersResponse(betterproto.Message):
    """List users response"""

    users: List["User"] = betterproto.message_field(1)
    next_page_token: str = betterproto.string_field(2)
    total_count: int = betterproto.int32_field(3)


@dataclass
class ListPostsResponse(betterproto.Message):
    """List posts response"""

    posts: List["Post"] = betterproto.message_field(1)
    next_page_token: str = betterproto.string_field(2)
    total_count: int = betterproto.int32_field(3)


@dataclass
class UpdateUserRequest(betterproto.Message):
    """Update user request"""

    id: str = betterproto.string_field(1)
    # Fields to update with optional values
    email: str = betterproto.string_field(2)
    display_name: str = betterproto.string_field(3)
    profile_picture_url: str = betterproto.string_field(4)
    bio: str = betterproto.string_field(5)
    status: "UserStatus" = betterproto.enum_field(6)


@dataclass
class Comment(betterproto.Message):
    """Comment entity"""

    id: str = betterproto.string_field(1)
    post_id: str = betterproto.string_field(2)
    user_id: str = betterproto.string_field(3)
    content: str = betterproto.string_field(4)
    created_at: datetime = betterproto.message_field(5)
    updated_at: datetime = betterproto.message_field(6)


@dataclass
class CreatePostRequest(betterproto.Message):
    """Create post request"""

    user_id: str = betterproto.string_field(1)
    title: str = betterproto.string_field(2)
    content: str = betterproto.string_field(3)
    image_urls: List[str] = betterproto.string_field(4)
    tags: List[str] = betterproto.string_field(5)
    visibility: "PostVisibility" = betterproto.enum_field(6)


@dataclass
class AuthenticateResponse(betterproto.Message):
    """Authentication response"""

    user_id: str = betterproto.string_field(1)
    access_token: str = betterproto.string_field(2)
    refresh_token: str = betterproto.string_field(3)
    expires_in: int = betterproto.int64_field(4)


@dataclass
class AddCommentRequest(betterproto.Message):
    """Add comment request"""

    post_id: str = betterproto.string_field(1)
    user_id: str = betterproto.string_field(2)
    content: str = betterproto.string_field(3)


@dataclass
class ListCommentsResponse(betterproto.Message):
    """List comments response"""

    comments: List["Comment"] = betterproto.message_field(1)
    next_page_token: str = betterproto.string_field(2)
    total_count: int = betterproto.int32_field(3)


@dataclass
class GetUserRequest(betterproto.Message):
    """Get user request"""

    id: str = betterproto.string_field(1)


@dataclass
class AuthenticateRequest(betterproto.Message):
    """Authentication request"""

    username_or_email: str = betterproto.string_field(1)
    password: str = betterproto.string_field(2)


@dataclass
class ListUserPostsRequest(betterproto.Message):
    """List user's posts request"""

    user_id: str = betterproto.string_field(1)
    page_size: int = betterproto.int32_field(2)
    page_token: str = betterproto.string_field(3)
    visibility_filter: "PostVisibility" = betterproto.enum_field(4)


@dataclass
class DeleteUserRequest(betterproto.Message):
    """Delete user request"""

    id: str = betterproto.string_field(1)


@dataclass
class Post(betterproto.Message):
    """Post entity"""

    id: str = betterproto.string_field(1)
    user_id: str = betterproto.string_field(2)
    title: str = betterproto.string_field(3)
    content: str = betterproto.string_field(4)
    image_urls: List[str] = betterproto.string_field(5)
    tags: List[str] = betterproto.string_field(6)
    visibility: "PostVisibility" = betterproto.enum_field(7)
    like_count: int = betterproto.int32_field(8)
    comment_count: int = betterproto.int32_field(9)
    created_at: datetime = betterproto.message_field(10)
    updated_at: datetime = betterproto.message_field(11)


@dataclass
class GetPostRequest(betterproto.Message):
    """Get post request"""

    id: str = betterproto.string_field(1)


@dataclass
class DeletePostRequest(betterproto.Message):
    """Delete post request"""

    id: str = betterproto.string_field(1)
    user_id: str = betterproto.string_field(2)


@dataclass
class LikePostRequest(betterproto.Message):
    """Like post request"""

    post_id: str = betterproto.string_field(1)
    user_id: str = betterproto.string_field(2)


@dataclass
class ListCommentsRequest(betterproto.Message):
    """List comments request"""

    post_id: str = betterproto.string_field(1)
    page_size: int = betterproto.int32_field(2)
    page_token: str = betterproto.string_field(3)


@dataclass
class User(betterproto.Message):
    """User entity"""

    id: str = betterproto.string_field(1)
    username: str = betterproto.string_field(2)
    email: str = betterproto.string_field(3)
    display_name: str = betterproto.string_field(4)
    profile_picture_url: str = betterproto.string_field(5)
    bio: str = betterproto.string_field(6)
    created_at: datetime = betterproto.message_field(7)
    updated_at: datetime = betterproto.message_field(8)
    status: "UserStatus" = betterproto.enum_field(9)


@dataclass
class UnlikePostRequest(betterproto.Message):
    """Unlike post request"""

    post_id: str = betterproto.string_field(1)
    user_id: str = betterproto.string_field(2)


# Code from: __init__.py


# Code from: wos.py
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: wos.proto
# plugin: python-betterproto




class WOSDataFieldCollection(betterproto.Enum):
    COLLECTION_SINGLE = 0
    COLLECTION_LIST = 1
    COLLECTION_MAP = 2


class WOSNodeState(betterproto.Enum):
    SCHEDULED = 0
    PENDING = 1
    STARTED = 2
    RUNNING = 3
    KILLING = 4
    COMPLETED = 5
    FAILED = 6
    RESTARTING = 7


class WOSNodePolicy(betterproto.Enum):
    IGNORE = 0
    RESTART = 1
    EMERGENCY = 2


class WOSIssueSeverity(betterproto.Enum):
    SEVERITY_INFO = 0
    SEVERITY_WARNING = 1
    SEVERITY_ERROR = 2


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


@dataclass
class WOSNodeDefinition(betterproto.Message):
    # Unique key for the node (used in key field in WOSNodeConfig)
    name: str = betterproto.string_field(1)
    # additional environment variables to pass to the command for http[s]
    # request, this will be the headers
    env: Dict[str, str] = betterproto.map_field(
        2, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
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
    config: Dict[str, str] = betterproto.map_field(
        5, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
    # list of tags for the frontend filtering
    tags: List[str] = betterproto.string_field(6)
    # For container & host process, this will be the command to run on prestart
    # stage
    prestart_args: List[str] = betterproto.string_field(7)
    # For container & host process, this will be the command to run on start
    # stage
    onstart_args: List[str] = betterproto.string_field(8)
    # List of the node to run as dependencies before this node
    deps: Dict[str, "WOSStartNodeRequest"] = betterproto.map_field(
        9, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    # List of the shared dependencies for the node
    shared_deps: List[str] = betterproto.string_field(10)
    # Priority of the node This will be used to determine the order of the node
    # to run higher priority will run first
    priority: int = betterproto.int32_field(11)
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
    # image to be used for the container add this to allow wos to automatically
    # pull the image for user
    images: List[str] = betterproto.string_field(16)


@dataclass
class WOSAllBasicTypes(betterproto.Message):
    """A message containing fields of all the basic protobuf types"""

    # Basic scalar types
    bool_value: bool = betterproto.bool_field(1)
    int32_value: int = betterproto.int32_field(2)
    int64_value: int = betterproto.int64_field(3)
    sint32_value: int = betterproto.sint32_field(4)
    sint64_value: int = betterproto.sint64_field(5)
    uint32_value: int = betterproto.uint32_field(6)
    uint64_value: int = betterproto.uint64_field(7)
    fixed32_value: float = betterproto.fixed32_field(8)
    sfixed32_value: float = betterproto.sfixed32_field(9)
    fixed64_value: float = betterproto.fixed64_field(10)
    sfixed64_value: float = betterproto.sfixed64_field(11)
    float_value: float = betterproto.float_field(12)
    double_value: float = betterproto.double_field(13)
    string_value: str = betterproto.string_field(14)
    bytes_value: bytes = betterproto.bytes_field(15)


@dataclass
class WOSIssue(betterproto.Message):
    # The severity of the issue
    severity: "WOSIssueSeverity" = betterproto.enum_field(1)
    # The message of the issue
    message: str = betterproto.string_field(2)
    # The resolution of the issue
    resolution: str = betterproto.string_field(3)


@dataclass
class WOSSetting(betterproto.Message):
    package_settings: Dict[str, "WOSPackageSetting"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    port: str = betterproto.string_field(2)
    fps: int = betterproto.uint32_field(3)
    beta: bool = betterproto.bool_field(4)
    debug: bool = betterproto.bool_field(5)


@dataclass
class WOSActionDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    input: str = betterproto.string_field(2)
    output: str = betterproto.string_field(3)
    singleton: bool = betterproto.bool_field(4)
    description: str = betterproto.string_field(5)


@dataclass
class WOSNodeInfo(betterproto.Message):
    id: str = betterproto.string_field(1)
    definition: "WOSNodeDefinition" = betterproto.message_field(2)
    request: "WOSStartNodeRequest" = betterproto.message_field(3)
    parameters: Dict[str, str] = betterproto.map_field(
        4, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
    state: "WOSNodeState" = betterproto.enum_field(5)
    status: str = betterproto.string_field(6)
    parent: str = betterproto.string_field(7)
    shared: bool = betterproto.bool_field(8)


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
class WOSWaitServiceAvailable(betterproto.Message):
    # The resource to wait for
    resource: str = betterproto.string_field(1)
    # The instance to wait for
    instance: str = betterproto.string_field(2)
    # The timeout in seconds
    timeout: int = betterproto.int32_field(3)


@dataclass
class WOSServiceDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    singleton: bool = betterproto.bool_field(2)
    topics: Dict[str, "WOSTopicDefinition"] = betterproto.map_field(
        3, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    requests: Dict[str, "WOSRequestDefinition"] = betterproto.map_field(
        4, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    actions: Dict[str, "WOSActionDefinition"] = betterproto.map_field(
        5, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    package: str = betterproto.string_field(6)


@dataclass
class WOSDataTypeEnumValue(betterproto.Message):
    name: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    value: int = betterproto.int32_field(3)


@dataclass
class WOSAllWellKnownTypes(betterproto.Message):
    """A message containing all the Google well-known types"""

    # Google well-known types
    timestamp_value: datetime = betterproto.message_field(1)
    duration_value: timedelta = betterproto.message_field(2)
    empty_value: protobuf.Empty = betterproto.message_field(3)
    double_wrapper_value: Optional[float] = betterproto.message_field(
        4, wraps=betterproto.TYPE_DOUBLE
    )
    float_wrapper_value: Optional[float] = betterproto.message_field(
        5, wraps=betterproto.TYPE_FLOAT
    )
    int32_wrapper_value: Optional[int] = betterproto.message_field(
        6, wraps=betterproto.TYPE_INT32
    )
    int64_wrapper_value: Optional[int] = betterproto.message_field(
        7, wraps=betterproto.TYPE_INT64
    )
    uint32_wrapper_value: Optional[int] = betterproto.message_field(
        8, wraps=betterproto.TYPE_UINT32
    )
    uint64_wrapper_value: Optional[int] = betterproto.message_field(
        9, wraps=betterproto.TYPE_UINT64
    )
    bool_wrapper_value: Optional[bool] = betterproto.message_field(
        10, wraps=betterproto.TYPE_BOOL
    )
    string_wrapper_value: Optional[str] = betterproto.message_field(
        11, wraps=betterproto.TYPE_STRING
    )
    bytes_wrapper_value: Optional[bytes] = betterproto.message_field(
        12, wraps=betterproto.TYPE_BYTES
    )
    struct_value: protobuf.Struct = betterproto.message_field(13)
    any_value: protobuf.Any = betterproto.message_field(14)
    field_mask_value: protobuf.FieldMask = betterproto.message_field(15)


@dataclass
class WOSServiceInfo(betterproto.Message):
    resource: str = betterproto.string_field(1)
    instance: str = betterproto.string_field(2)


@dataclass
class WOSPackageRegistration(betterproto.Message):
    name: str = betterproto.string_field(1)
    path: str = betterproto.string_field(2)
    info: "WOSPackageInfo" = betterproto.message_field(3)


@dataclass
class WOSStartNodeRequest(betterproto.Message):
    # If we want to presist the run info, we can provide the id
    id: str = betterproto.string_field(1)
    # The node to run in node-entity format node-entity format: <package-
    # name>/<node-key>
    name: str = betterproto.string_field(2)
    # The node input
    parameters: Dict[str, str] = betterproto.map_field(
        3, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
    instance: str = betterproto.string_field(4)
    # Used by wos internally
    extra: Dict[str, str] = betterproto.map_field(
        5, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )


@dataclass
class WOSPackageDefinition(betterproto.Message):
    # path-regex or path-regex array wos will scan all files under this regex
    # that is a valid proto file
    proto: List[str] = betterproto.string_field(1)
    # The UI definition for the package WOS webapp will pick this up and provide
    # the web rendering
    ui: "WOSPackageUIDefinition" = betterproto.message_field(2)
    # The node to run on "wos start" and "wos dev"
    main: List["WOSStartNodeRequest"] = betterproto.message_field(3)
    # The node to run on "wos start" and "wos dev" as well as "wos serve" Node
    # defines here usually is a daemon node that expose service for managment And
    # is required to power the frontend UI
    daemon: List["WOSStartNodeRequest"] = betterproto.message_field(4)
    # These parameters will be reported to user local config where end user can
    # change the value
    parameters: Dict[str, str] = betterproto.map_field(
        5, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
    # You can also choose to specify the type of the parameters which in turn
    # will be validated And provide approprate UI for the user to change the
    # value
    parameters_type: str = betterproto.string_field(6)
    # Map of the node definitions where key is the node key
    nodes: Dict[str, "WOSNodeDefinition"] = betterproto.map_field(
        7, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    # Map of the services where key is the service name
    services: Dict[str, "WOSServiceDefinition"] = betterproto.map_field(
        8, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    # Map of the dependencies where key is the package name and value is the
    # version constraint Or the path to get the package. Suporrted values are: -
    # git://<url> - git+ssh://<url> - git+https://<url> - git+http://<url> -
    # file://<path> - http[s]://<url> (to download the entire package in zip,
    # tar.gz, or tar.xz. And it should have a wos.json file in its root folder)
    dependencies: Dict[str, str] = betterproto.map_field(
        9, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )


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
class WOSNodeInfoList(betterproto.Message):
    nodes: Dict[str, "WOSNodeInfo"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )


@dataclass
class WOSTopicDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    type: str = betterproto.string_field(2)
    description: str = betterproto.string_field(3)


@dataclass
class WOSPackageUIDefinition(betterproto.Message):
    """
    The UI definition for the package Must provide either www or endpoint or
    node
    """

    # The name to show on the UI
    title: str = betterproto.string_field(1)
    # The icon for the package This should be a path to the image relative to the
    # package root
    icon: str = betterproto.string_field(2)
    # If the package provides static html and assets, this will be the path to
    # the folder relative to the package root The folder should contains an
    # index.html file
    www: str = betterproto.string_field(3)
    # Instead of static html, you can also provide an endpoint to the webapp The
    # endpoint should be a valid http[s] endpoint
    endpoint: str = betterproto.string_field(4)


@dataclass
class WOSRequestDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    input: str = betterproto.string_field(2)
    output: str = betterproto.string_field(3)
    description: str = betterproto.string_field(4)


@dataclass
class WOSDataTypeEnumDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    values: List["WOSDataTypeEnumValue"] = betterproto.message_field(3)


@dataclass
class WOSServiceList(betterproto.Message):
    services: Dict[str, "WOSServiceInfo"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )


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
    # list of folders/files to be included in the package pack/publish
    exports: List[str] = betterproto.string_field(11)


@dataclass
class WOSDescription(betterproto.Message):
    packages: Dict[str, "WOSPackageRegistration"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    data_types: Dict[str, "WOSDataTypeDefinition"] = betterproto.map_field(
        2, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    data_enums: Dict[str, "WOSDataTypeEnumDefinition"] = betterproto.map_field(
        3, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    nodes: Dict[str, "WOSNodeDefinition"] = betterproto.map_field(
        4, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    services: Dict[str, "WOSServiceDefinition"] = betterproto.map_field(
        5, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    setting: "WOSSetting" = betterproto.message_field(6)
    version: str = betterproto.string_field(7)
    workspace: str = betterproto.string_field(8)


@dataclass
class WOSHeartbeat(betterproto.Message):
    num_nodes_running: int = betterproto.int32_field(1)
    num_nodes: int = betterproto.int32_field(2)
    num_services: int = betterproto.int32_field(3)
    num_goroutines: int = betterproto.int32_field(4)
    num_connections: int = betterproto.int32_field(5)
    num_messages_per_sec: float = betterproto.float_field(6)


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
class WOSDataTypeDefinition(betterproto.Message):
    name: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    editor: str = betterproto.string_field(3)
    validator: str = betterproto.string_field(4)
    fields: List["WOSDataFieldDefinition"] = betterproto.message_field(5)


@dataclass
class WOSAPIFeedback(betterproto.Message):
    """Use for Op = OP_FEEDBACK"""

    # from zero to one
    progress: float = betterproto.float_field(1)
    # a status message provided by service handler
    status: str = betterproto.string_field(2)


@dataclass
class WOSPackageSetting(betterproto.Message):
    parameters: Dict[str, str] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
