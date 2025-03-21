"""
WOS Python SDK

Auto-generated Python SDK for WOS
"""

from typing import Any, Callable, Dict, List, Optional, Union, Tuple
from .base_client import (
    WOSBaseClient,
    WOSAPIError,
    convert_base_type_from_bytes,
    convert_base_type_to_bytes,
)
from .pb import wos

from . import pb
import datetime
from typing import Optional, Dict, List, Any, Callable, Union
from .pb.wos import (
    WOSNodePolicy,
    WOSIssueSeverity,
    WOSAPIOperation,
    WOSDataFieldCollection,
    WOSNodeState,
    WOSServiceList,
    WOSPackageRegistration,
    WOSDataFieldDefinition,
    WOSActionDefinition,
    WOSServiceInfo,
    WOSDataTypeEnumValue,
    WOSDescription,
    WOSNodeDefinition,
    WOSAPIMessage,
    WOSSetting,
    WOSStartNodeRequest,
    WOSNodeInfoList,
    WOSHeartbeat,
    WOSAPIFeedback,
    WOSNodeInfo,
    WOSTopicDefinition,
    WOSRequestDefinition,
    WOSPackageInfo,
    WOSServiceDefinition,
    WOSDataTypeEnumDefinition,
    WOSPackageSetting,
    WOSPackageDefinition,
    WOSDiagnoseInfo,
    WOSDataTypeDefinition,
    WOSIssue,
)
from .pb.wosdummy import (
    PostVisibility,
    UserStatus,
    UpdateUserRequest,
    Comment,
    DeletePostRequest,
    LikePostResponse,
    UnlikePostRequest,
    ListUsersRequest,
    AddCommentRequest,
    ListPostsRequest,
    ListUserPostsRequest,
    UpdatePostRequest,
    ListCommentsResponse,
    ListCommentsRequest,
    GetUserRequest,
    CreateUserRequest,
    GetPostRequest,
    User,
    CreatePostRequest,
    ListPostsResponse,
    AuthenticateResponse,
    DeleteUserRequest,
    AuthenticateRequest,
    LikePostRequest,
    Post,
    ListUsersResponse,
)


# Main Module
class MainModule:
    """
    Module for main services
    """

    def __init__(self, client: "WOSBaseClient"):
        """
        Initialize the module

        Args:
            client: WOSBaseClient instance
        """
        self._client = client
        self.node = NodeService(client)
        self.core = CoreService(client)


class NodeService:
    """
    Service for main/node
    """

    def __init__(self, client: "WOSBaseClient"):
        """
        Initialize the service

        Args:
            client: WOSBaseClient instance
        """
        self._client = client

    def publish_node_state_update(self, payload: WOSNodeInfo, instance: str = ""):
        """
        Publish when a node state is updated

                Args:
                    payload: The message payload
                    instance: Optional service instance identifier
        """
        serialized = payload.SerializeToString()
        self._client.publish("main/node", "node_state_update", serialized, instance)

    def subscribe_node_state_update(
        self, callback: Callable[[WOSNodeInfo], None], instance: str = ""
    ) -> str:
        """
        Publish when a node state is updated

                Args:
                    instance: Optional service instance identifier
                    callback: Function to call when a message is received

                Returns:
                    Subscription key that can be used to unsubscribe
        """

        # Create wrapped callback for type conversion
        def wrapped_callback(msg: WOSAPIMessage):
            # Convert bytes to the expected type
            if msg.payload is not None:
                payload = WOSNodeInfo().parse(msg.payload)
            else:
                payload = None
            callback(payload)

        return self._client.subscribe(
            "main/node", "node_state_update", wrapped_callback, instance
        )

    def unsubscribe_node_state_update(self, subscription_key: str):
        """
        Publish when a node state is updated

                Args:
                    subscription_key: The key returned from the subscribe method
        """
        self._client.unsubscribe(subscription_key)

    def request_list_node(self, instance: str = "", timeout: float = None) -> bytes:
        """
        List all nodes in the system

                Args:
                    instance: Optional service instance identifier
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = None

        result = self._client.request(
            "main/node", "list_node", serialized, instance, timeout
        )

        # Convert result to expected type
        if result is not None:
            return bytes().parse(result)
        return None

    def request_launch_node(
        self, payload: WOSStartNodeRequest, instance: str = "", timeout: float = None
    ) -> WOSNodeInfo:
        """
        Launch a new node, this will return without waiting for the node to be fully started

                Args:
                    payload: The message payload
                    instance: Optional service instance identifier
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "main/node", "launch_node", serialized, instance, timeout
        )

        # Convert result to expected type
        if result is not None:
            return WOSNodeInfo().parse(result)
        return None

    def request_stop_node(
        self, payload: str, instance: str = "", timeout: float = None
    ):
        """
        Stop a node by id

                Args:
                    payload: The message payload
                    instance: Optional service instance identifier
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = convert_base_type_to_bytes(payload, "string")
        result = self._client.request(
            "main/node", "stop_node", serialized, instance, timeout
        )
        return result

    def action_run_node(
        self,
        payload: WOSStartNodeRequest,
        instance: str = "",
        feedback_callback: Callable[[wos.WOSAPIFeedback], None] = None,
        timeout: float = None,
    ) -> WOSNodeInfo:
        """
        Run a node and hold for it to completed

                Args:
                    payload: The message payload
                    instance: Optional service instance identifier
                    feedback_callback: Function to call when progress updates are received
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.action(
            "main/node", "run_node", serialized, instance, feedback_callback, timeout
        )

        # Convert result to expected type
        if result is not None:
            return WOSNodeInfo().parse(result)
        return None

    def serve(self, service_handler: Any, instance: str):
        """
        Register this service with the WOS system.

        Args:
            service_handler: An object that implements the service interface methods
            instance: Service instance identifier
        """
        # Validate the service handler has the required methods
        self._validate_service_handler(service_handler)

        # Create a wrapper for the service handler
        wrapped_handler = self._create_service_handler_wrapper(service_handler)

        return self._client.serve("main/node", wrapped_handler, instance)

    def _validate_service_handler(self, service_handler: Any):
        """
        Validate that the service handler implements the required methods.

        Args:
            service_handler: An object that implements the service interface methods
        """
        # Check for required methods
        if not hasattr(service_handler, "req_list_node") or not callable(
            getattr(service_handler, "req_list_node")
        ):
            raise ValueError("Service handler must implement req_list_node method")
        if not hasattr(service_handler, "req_launch_node") or not callable(
            getattr(service_handler, "req_launch_node")
        ):
            raise ValueError("Service handler must implement req_launch_node method")
        if not hasattr(service_handler, "req_stop_node") or not callable(
            getattr(service_handler, "req_stop_node")
        ):
            raise ValueError("Service handler must implement req_stop_node method")
        if not hasattr(service_handler, "act_run_node") or not callable(
            getattr(service_handler, "act_run_node")
        ):
            raise ValueError("Service handler must implement act_run_node method")
        if not hasattr(service_handler, "cancel_run_node") or not callable(
            getattr(service_handler, "cancel_run_node")
        ):
            raise ValueError(
                "Service handler must implement cancel_run_node method for cancellable actions"
            )

    def _create_service_handler_wrapper(self, service_handler: Any):
        """
        Create a wrapper for the service handler that converts messages to/from the appropriate types.

        Args:
            service_handler: An object that implements the service interface methods

        Returns:
            A function that can be passed to the client's serve method
        """

        def wrapper(
            message: wos.WOSAPIMessage, feedback_handler: wos.WOSAPIFeedback = None
        ) -> Tuple[bytes, str]:
            # Route the message based on operation type and topic
            topic = message.topic
            error = None

            # Handle cancel operation for actions
            if message.op == wos.WOSAPIOperation.OP_CANCEL:
                if topic == "run_node":
                    try:
                        service_handler.cancel_["run", "node"]()
                        return None, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown topic for cancel: {topic}"

            # Handle request operations
            if message.op == wos.WOSAPIOperation.OP_REQUEST:
                if topic == "list_node":
                    try:
                        result = service_handler.req_list_node()
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "launch_node":
                    # Parse input message
                    input_data = WOSStartNodeRequest().parse(message.payload)
                    try:
                        result = service_handler.req_launch_node(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "stop_node":
                    # Convert input bytes to string
                    input_data = convert_base_type_from_bytes(message.payload, "string")
                    try:
                        result = service_handler.req_stop_node(input_data)
                        return None, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown request topic: {topic}"

            # Handle action operations
            elif message.op == wos.WOSAPIOperation.OP_ACTION:
                if topic == "run_node":
                    # Parse input message
                    input_data = WOSStartNodeRequest().parse(message.payload)
                    try:
                        result = service_handler.act_run_node(
                            input_data, feedback_handler
                        )
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown action topic: {topic}"
            else:
                return None, f"Unsupported operation type: {message.op}"

        return wrapper


class CoreService:
    """
    Service for main/core
    """

    def __init__(self, client: "WOSBaseClient"):
        """
        Initialize the service

        Args:
            client: WOSBaseClient instance
        """
        self._client = client

    def publish_heartbeat(self, payload: WOSHeartbeat):
        """
        Heartbeat topic will be published by core service every 20 seconds

                Args:
                    payload: The message payload
        """
        serialized = payload.SerializeToString()
        self._client.publish("main/core", "heartbeat", serialized)

    def subscribe_heartbeat(self, callback: Callable[[WOSHeartbeat], None]) -> str:
        """
        Heartbeat topic will be published by core service every 20 seconds

                Args:
                    callback: Function to call when a message is received

                Returns:
                    Subscription key that can be used to unsubscribe
        """

        # Create wrapped callback for type conversion
        def wrapped_callback(msg: WOSAPIMessage):
            # Convert bytes to the expected type
            if msg.payload is not None:
                payload = WOSHeartbeat().parse(msg.payload)
            else:
                payload = None
            callback(payload)

        return self._client.subscribe("main/core", "heartbeat", wrapped_callback)

    def unsubscribe_heartbeat(self, subscription_key: str):
        """
        Heartbeat topic will be published by core service every 20 seconds

                Args:
                    subscription_key: The key returned from the subscribe method
        """
        self._client.unsubscribe(subscription_key)

    def publish_message_service_available(self, payload: str):
        """
        Publish when a new service is available

                Args:
                    payload: The message payload
        """
        serialized = convert_base_type_to_bytes(payload, "string")
        self._client.publish("main/core", "message_service_available", serialized)

    def subscribe_message_service_available(
        self, callback: Callable[[str], None]
    ) -> str:
        """
        Publish when a new service is available

                Args:
                    callback: Function to call when a message is received

                Returns:
                    Subscription key that can be used to unsubscribe
        """

        # Create wrapped callback for type conversion
        def wrapped_callback(msg: WOSAPIMessage):
            # Convert bytes to the expected type
            if msg.payload is not None:
                payload = convert_base_type_from_bytes(msg.payload, "string")
            else:
                payload = None
            callback(payload)

        return self._client.subscribe(
            "main/core", "message_service_available", wrapped_callback
        )

    def unsubscribe_message_service_available(self, subscription_key: str):
        """
        Publish when a new service is available

                Args:
                    subscription_key: The key returned from the subscribe method
        """
        self._client.unsubscribe(subscription_key)

    def request_get_service_list(self, timeout: float = None) -> WOSServiceList:
        """
        Get the list of services available in the system

                Args:
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = None

        result = self._client.request(
            "main/core", "get_service_list", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return WOSServiceList().parse(result)
        return None

    def request_get_wos_description(self, timeout: float = None) -> WOSDescription:
        """
        Get the description of the whole system

                Args:
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = None

        result = self._client.request(
            "main/core", "get_wos_description", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return WOSDescription().parse(result)
        return None

    def request_list_service_instance(
        self, payload: str, timeout: float = None
    ) -> WOSServiceList:
        """
        List all the instances of a service

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = convert_base_type_to_bytes(payload, "string")
        result = self._client.request(
            "main/core", "list_service_instance", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return WOSServiceList().parse(result)
        return None

    def request_get_diagnose_info(self, timeout: float = None) -> WOSDiagnoseInfo:
        """
        Get the diagnose information of the system

                Args:
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = None

        result = self._client.request(
            "main/core", "get_diagnose_info", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return WOSDiagnoseInfo().parse(result)
        return None

    def request_get_go_routine_info(self, timeout: float = None) -> str:
        """
        Get the go routine information of the system

                Args:
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = None

        result = self._client.request(
            "main/core", "get_go_routine_info", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return convert_base_type_from_bytes(result, "string")
        return None

    def request_get_heartbeat(self, timeout: float = None) -> WOSHeartbeat:
        """
        Get the current heartbeat of the system

                Args:
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = None

        result = self._client.request(
            "main/core", "get_heartbeat", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return WOSHeartbeat().parse(result)
        return None

    def serve(self, service_handler: Any):
        """
        Register this service with the WOS system.

        Args:
            service_handler: An object that implements the service interface methods
        """
        # Validate the service handler has the required methods
        self._validate_service_handler(service_handler)

        # Create a wrapper for the service handler
        wrapped_handler = self._create_service_handler_wrapper(service_handler)

        return self._client.serve("main/core", wrapped_handler)

    def _validate_service_handler(self, service_handler: Any):
        """
        Validate that the service handler implements the required methods.

        Args:
            service_handler: An object that implements the service interface methods
        """
        # Check for required methods
        if not hasattr(service_handler, "req_get_service_list") or not callable(
            getattr(service_handler, "req_get_service_list")
        ):
            raise ValueError(
                "Service handler must implement req_get_service_list method"
            )
        if not hasattr(service_handler, "req_get_wos_description") or not callable(
            getattr(service_handler, "req_get_wos_description")
        ):
            raise ValueError(
                "Service handler must implement req_get_wos_description method"
            )
        if not hasattr(service_handler, "req_list_service_instance") or not callable(
            getattr(service_handler, "req_list_service_instance")
        ):
            raise ValueError(
                "Service handler must implement req_list_service_instance method"
            )
        if not hasattr(service_handler, "req_get_diagnose_info") or not callable(
            getattr(service_handler, "req_get_diagnose_info")
        ):
            raise ValueError(
                "Service handler must implement req_get_diagnose_info method"
            )
        if not hasattr(service_handler, "req_get_go_routine_info") or not callable(
            getattr(service_handler, "req_get_go_routine_info")
        ):
            raise ValueError(
                "Service handler must implement req_get_go_routine_info method"
            )
        if not hasattr(service_handler, "req_get_heartbeat") or not callable(
            getattr(service_handler, "req_get_heartbeat")
        ):
            raise ValueError("Service handler must implement req_get_heartbeat method")

    def _create_service_handler_wrapper(self, service_handler: Any):
        """
        Create a wrapper for the service handler that converts messages to/from the appropriate types.

        Args:
            service_handler: An object that implements the service interface methods

        Returns:
            A function that can be passed to the client's serve method
        """

        def wrapper(
            message: wos.WOSAPIMessage, feedback_handler: wos.WOSAPIFeedback = None
        ) -> Tuple[bytes, str]:
            # Route the message based on operation type and topic
            topic = message.topic
            error = None

            # Handle cancel operation for actions
            if message.op == wos.WOSAPIOperation.OP_CANCEL:
                return None, "No cancellable actions defined"

            # Handle request operations
            if message.op == wos.WOSAPIOperation.OP_REQUEST:
                if topic == "get_service_list":
                    try:
                        result = service_handler.req_get_service_list()
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "get_wos_description":
                    try:
                        result = service_handler.req_get_wos_description()
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "list_service_instance":
                    # Convert input bytes to string
                    input_data = convert_base_type_from_bytes(message.payload, "string")
                    try:
                        result = service_handler.req_list_service_instance(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "get_diagnose_info":
                    try:
                        result = service_handler.req_get_diagnose_info()
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "get_go_routine_info":
                    try:
                        result = service_handler.req_get_go_routine_info()
                        # Convert result to bytes
                        output_bytes = convert_base_type_to_bytes(result, "string")
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "get_heartbeat":
                    try:
                        result = service_handler.req_get_heartbeat()
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown request topic: {topic}"

            # Handle action operations
            elif message.op == wos.WOSAPIOperation.OP_ACTION:
                return None, "No action operations defined"
            else:
                return None, f"Unsupported operation type: {message.op}"

        return wrapper


# WosDummy Module
class WosDummyModule:
    """
    Module for @wos/dummy services
    """

    def __init__(self, client: "WOSBaseClient"):
        """
        Initialize the module

        Args:
            client: WOSBaseClient instance
        """
        self._client = client
        self.post = PostService(client)
        self.user = UserService(client)


class PostService:
    """
    Service for @wos/dummy/post
    """

    def __init__(self, client: "WOSBaseClient"):
        """
        Initialize the service

        Args:
            client: WOSBaseClient instance
        """
        self._client = client

    def publish_comment_updates(self, payload: Comment):
        """
        Stream of comment updates

                Args:
                    payload: The message payload
        """
        serialized = payload.SerializeToString()
        self._client.publish("@wos/dummy/post", "comment_updates", serialized)

    def subscribe_comment_updates(self, callback: Callable[[Comment], None]) -> str:
        """
        Stream of comment updates

                Args:
                    callback: Function to call when a message is received

                Returns:
                    Subscription key that can be used to unsubscribe
        """

        # Create wrapped callback for type conversion
        def wrapped_callback(msg: WOSAPIMessage):
            # Convert bytes to the expected type
            if msg.payload is not None:
                payload = Comment().parse(msg.payload)
            else:
                payload = None
            callback(payload)

        return self._client.subscribe(
            "@wos/dummy/post", "comment_updates", wrapped_callback
        )

    def unsubscribe_comment_updates(self, subscription_key: str):
        """
        Stream of comment updates

                Args:
                    subscription_key: The key returned from the subscribe method
        """
        self._client.unsubscribe(subscription_key)

    def publish_post_updates(self, payload: Post):
        """
        Stream of post updates

                Args:
                    payload: The message payload
        """
        serialized = payload.SerializeToString()
        self._client.publish("@wos/dummy/post", "post_updates", serialized)

    def subscribe_post_updates(self, callback: Callable[[Post], None]) -> str:
        """
        Stream of post updates

                Args:
                    callback: Function to call when a message is received

                Returns:
                    Subscription key that can be used to unsubscribe
        """

        # Create wrapped callback for type conversion
        def wrapped_callback(msg: WOSAPIMessage):
            # Convert bytes to the expected type
            if msg.payload is not None:
                payload = Post().parse(msg.payload)
            else:
                payload = None
            callback(payload)

        return self._client.subscribe(
            "@wos/dummy/post", "post_updates", wrapped_callback
        )

    def unsubscribe_post_updates(self, subscription_key: str):
        """
        Stream of post updates

                Args:
                    subscription_key: The key returned from the subscribe method
        """
        self._client.unsubscribe(subscription_key)

    def request_create_post(
        self, payload: CreatePostRequest, timeout: float = None
    ) -> Post:
        """
        Create a new post

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/post", "create_post", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return Post().parse(result)
        return None

    def request_get_post(self, payload: GetPostRequest, timeout: float = None) -> Post:
        """
        Get a post by ID

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/post", "get_post", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return Post().parse(result)
        return None

    def request_list_comments(
        self, payload: ListCommentsRequest, timeout: float = None
    ) -> ListCommentsResponse:
        """
        List comments for a post

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/post", "list_comments", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return ListCommentsResponse().parse(result)
        return None

    def request_list_posts(
        self, payload: ListPostsRequest, timeout: float = None
    ) -> ListPostsResponse:
        """
        List posts with pagination

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/post", "list_posts", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return ListPostsResponse().parse(result)
        return None

    def request_list_user_posts(
        self, payload: ListUserPostsRequest, timeout: float = None
    ) -> ListPostsResponse:
        """
        List posts by user ID

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/post", "list_user_posts", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return ListPostsResponse().parse(result)
        return None

    def request_update_post(
        self, payload: UpdatePostRequest, timeout: float = None
    ) -> Post:
        """
        Update a post

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/post", "update_post", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return Post().parse(result)
        return None

    def action_add_comment(
        self,
        payload: AddCommentRequest,
        feedback_callback: Callable[[wos.WOSAPIFeedback], None] = None,
        timeout: float = None,
    ) -> Comment:
        """
        Add a comment to a post

                Args:
                    payload: The message payload
                    feedback_callback: Function to call when progress updates are received
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.action(
            "@wos/dummy/post", "add_comment", serialized, "", feedback_callback, timeout
        )

        # Convert result to expected type
        if result is not None:
            return Comment().parse(result)
        return None

    def action_delete_post(
        self,
        payload: DeletePostRequest,
        feedback_callback: Callable[[wos.WOSAPIFeedback], None] = None,
        timeout: float = None,
    ) -> bytes:
        """
        Delete a post

                Args:
                    payload: The message payload
                    feedback_callback: Function to call when progress updates are received
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.action(
            "@wos/dummy/post", "delete_post", serialized, "", feedback_callback, timeout
        )

        # Convert result to expected type
        if result is not None:
            return bytes().parse(result)
        return None

    def action_like_post(
        self,
        payload: LikePostRequest,
        feedback_callback: Callable[[wos.WOSAPIFeedback], None] = None,
        timeout: float = None,
    ) -> LikePostResponse:
        """
        Like a post

                Args:
                    payload: The message payload
                    feedback_callback: Function to call when progress updates are received
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.action(
            "@wos/dummy/post", "like_post", serialized, "", feedback_callback, timeout
        )

        # Convert result to expected type
        if result is not None:
            return LikePostResponse().parse(result)
        return None

    def action_unlike_post(
        self,
        payload: UnlikePostRequest,
        feedback_callback: Callable[[wos.WOSAPIFeedback], None] = None,
        timeout: float = None,
    ) -> bytes:
        """
        Unlike a post

                Args:
                    payload: The message payload
                    feedback_callback: Function to call when progress updates are received
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.action(
            "@wos/dummy/post", "unlike_post", serialized, "", feedback_callback, timeout
        )

        # Convert result to expected type
        if result is not None:
            return bytes().parse(result)
        return None

    def serve(self, service_handler: Any):
        """
        Register this service with the WOS system.

        Args:
            service_handler: An object that implements the service interface methods
        """
        # Validate the service handler has the required methods
        self._validate_service_handler(service_handler)

        # Create a wrapper for the service handler
        wrapped_handler = self._create_service_handler_wrapper(service_handler)

        return self._client.serve("@wos/dummy/post", wrapped_handler)

    def _validate_service_handler(self, service_handler: Any):
        """
        Validate that the service handler implements the required methods.

        Args:
            service_handler: An object that implements the service interface methods
        """
        # Check for required methods
        if not hasattr(service_handler, "req_create_post") or not callable(
            getattr(service_handler, "req_create_post")
        ):
            raise ValueError("Service handler must implement req_create_post method")
        if not hasattr(service_handler, "req_get_post") or not callable(
            getattr(service_handler, "req_get_post")
        ):
            raise ValueError("Service handler must implement req_get_post method")
        if not hasattr(service_handler, "req_list_comments") or not callable(
            getattr(service_handler, "req_list_comments")
        ):
            raise ValueError("Service handler must implement req_list_comments method")
        if not hasattr(service_handler, "req_list_posts") or not callable(
            getattr(service_handler, "req_list_posts")
        ):
            raise ValueError("Service handler must implement req_list_posts method")
        if not hasattr(service_handler, "req_list_user_posts") or not callable(
            getattr(service_handler, "req_list_user_posts")
        ):
            raise ValueError(
                "Service handler must implement req_list_user_posts method"
            )
        if not hasattr(service_handler, "req_update_post") or not callable(
            getattr(service_handler, "req_update_post")
        ):
            raise ValueError("Service handler must implement req_update_post method")
        if not hasattr(service_handler, "act_add_comment") or not callable(
            getattr(service_handler, "act_add_comment")
        ):
            raise ValueError("Service handler must implement act_add_comment method")
        if not hasattr(service_handler, "cancel_add_comment") or not callable(
            getattr(service_handler, "cancel_add_comment")
        ):
            raise ValueError(
                "Service handler must implement cancel_add_comment method for cancellable actions"
            )
        if not hasattr(service_handler, "act_delete_post") or not callable(
            getattr(service_handler, "act_delete_post")
        ):
            raise ValueError("Service handler must implement act_delete_post method")
        if not hasattr(service_handler, "cancel_delete_post") or not callable(
            getattr(service_handler, "cancel_delete_post")
        ):
            raise ValueError(
                "Service handler must implement cancel_delete_post method for cancellable actions"
            )
        if not hasattr(service_handler, "act_like_post") or not callable(
            getattr(service_handler, "act_like_post")
        ):
            raise ValueError("Service handler must implement act_like_post method")
        if not hasattr(service_handler, "cancel_like_post") or not callable(
            getattr(service_handler, "cancel_like_post")
        ):
            raise ValueError(
                "Service handler must implement cancel_like_post method for cancellable actions"
            )
        if not hasattr(service_handler, "act_unlike_post") or not callable(
            getattr(service_handler, "act_unlike_post")
        ):
            raise ValueError("Service handler must implement act_unlike_post method")
        if not hasattr(service_handler, "cancel_unlike_post") or not callable(
            getattr(service_handler, "cancel_unlike_post")
        ):
            raise ValueError(
                "Service handler must implement cancel_unlike_post method for cancellable actions"
            )

    def _create_service_handler_wrapper(self, service_handler: Any):
        """
        Create a wrapper for the service handler that converts messages to/from the appropriate types.

        Args:
            service_handler: An object that implements the service interface methods

        Returns:
            A function that can be passed to the client's serve method
        """

        def wrapper(
            message: wos.WOSAPIMessage, feedback_handler: wos.WOSAPIFeedback = None
        ) -> Tuple[bytes, str]:
            # Route the message based on operation type and topic
            topic = message.topic
            error = None

            # Handle cancel operation for actions
            if message.op == wos.WOSAPIOperation.OP_CANCEL:
                if topic == "add_comment":
                    try:
                        service_handler.cancel_["add", "comment"]()
                        return None, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "delete_post":
                    try:
                        service_handler.cancel_["delete", "post"]()
                        return None, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "like_post":
                    try:
                        service_handler.cancel_["like", "post"]()
                        return None, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "unlike_post":
                    try:
                        service_handler.cancel_["unlike", "post"]()
                        return None, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown topic for cancel: {topic}"

            # Handle request operations
            if message.op == wos.WOSAPIOperation.OP_REQUEST:
                if topic == "create_post":
                    # Parse input message
                    input_data = CreatePostRequest().parse(message.payload)
                    try:
                        result = service_handler.req_create_post(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "get_post":
                    # Parse input message
                    input_data = GetPostRequest().parse(message.payload)
                    try:
                        result = service_handler.req_get_post(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "list_comments":
                    # Parse input message
                    input_data = ListCommentsRequest().parse(message.payload)
                    try:
                        result = service_handler.req_list_comments(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "list_posts":
                    # Parse input message
                    input_data = ListPostsRequest().parse(message.payload)
                    try:
                        result = service_handler.req_list_posts(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "list_user_posts":
                    # Parse input message
                    input_data = ListUserPostsRequest().parse(message.payload)
                    try:
                        result = service_handler.req_list_user_posts(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "update_post":
                    # Parse input message
                    input_data = UpdatePostRequest().parse(message.payload)
                    try:
                        result = service_handler.req_update_post(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown request topic: {topic}"

            # Handle action operations
            elif message.op == wos.WOSAPIOperation.OP_ACTION:
                if topic == "add_comment":
                    # Parse input message
                    input_data = AddCommentRequest().parse(message.payload)
                    try:
                        result = service_handler.act_add_comment(
                            input_data, feedback_handler
                        )
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "delete_post":
                    # Parse input message
                    input_data = DeletePostRequest().parse(message.payload)
                    try:
                        result = service_handler.act_delete_post(
                            input_data, feedback_handler
                        )
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "like_post":
                    # Parse input message
                    input_data = LikePostRequest().parse(message.payload)
                    try:
                        result = service_handler.act_like_post(
                            input_data, feedback_handler
                        )
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "unlike_post":
                    # Parse input message
                    input_data = UnlikePostRequest().parse(message.payload)
                    try:
                        result = service_handler.act_unlike_post(
                            input_data, feedback_handler
                        )
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown action topic: {topic}"
            else:
                return None, f"Unsupported operation type: {message.op}"

        return wrapper


class UserService:
    """
    Service for @wos/dummy/user
    """

    def __init__(self, client: "WOSBaseClient"):
        """
        Initialize the service

        Args:
            client: WOSBaseClient instance
        """
        self._client = client

    def publish_user_deleted(self, payload: bytes):
        """
        Event when a user is deleted

                Args:
                    payload: The message payload
        """
        serialized = payload.SerializeToString()
        self._client.publish("@wos/dummy/user", "user_deleted", serialized)

    def subscribe_user_deleted(self, callback: Callable[[bytes], None]) -> str:
        """
        Event when a user is deleted

                Args:
                    callback: Function to call when a message is received

                Returns:
                    Subscription key that can be used to unsubscribe
        """

        # Create wrapped callback for type conversion
        def wrapped_callback(msg: WOSAPIMessage):
            # Convert bytes to the expected type
            if msg.payload is not None:
                payload = bytes().parse(msg.payload)
            else:
                payload = None
            callback(payload)

        return self._client.subscribe(
            "@wos/dummy/user", "user_deleted", wrapped_callback
        )

    def unsubscribe_user_deleted(self, subscription_key: str):
        """
        Event when a user is deleted

                Args:
                    subscription_key: The key returned from the subscribe method
        """
        self._client.unsubscribe(subscription_key)

    def publish_user_updates(self, payload: User):
        """
        Stream of user updates

                Args:
                    payload: The message payload
        """
        serialized = payload.SerializeToString()
        self._client.publish("@wos/dummy/user", "user_updates", serialized)

    def subscribe_user_updates(self, callback: Callable[[User], None]) -> str:
        """
        Stream of user updates

                Args:
                    callback: Function to call when a message is received

                Returns:
                    Subscription key that can be used to unsubscribe
        """

        # Create wrapped callback for type conversion
        def wrapped_callback(msg: WOSAPIMessage):
            # Convert bytes to the expected type
            if msg.payload is not None:
                payload = User().parse(msg.payload)
            else:
                payload = None
            callback(payload)

        return self._client.subscribe(
            "@wos/dummy/user", "user_updates", wrapped_callback
        )

    def unsubscribe_user_updates(self, subscription_key: str):
        """
        Stream of user updates

                Args:
                    subscription_key: The key returned from the subscribe method
        """
        self._client.unsubscribe(subscription_key)

    def request_create_user(
        self, payload: CreateUserRequest, timeout: float = None
    ) -> User:
        """
        Create a new user

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/user", "create_user", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return User().parse(result)
        return None

    def request_get_user(self, payload: GetUserRequest, timeout: float = None) -> User:
        """
        Get a user by ID

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/user", "get_user", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return User().parse(result)
        return None

    def request_list_users(
        self, payload: ListUsersRequest, timeout: float = None
    ) -> ListUsersResponse:
        """
        List users with pagination

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/user", "list_users", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return ListUsersResponse().parse(result)
        return None

    def request_update_user(
        self, payload: UpdateUserRequest, timeout: float = None
    ) -> User:
        """
        Update a user

                Args:
                    payload: The message payload
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.request(
            "@wos/dummy/user", "update_user", serialized, "", timeout
        )

        # Convert result to expected type
        if result is not None:
            return User().parse(result)
        return None

    def action_authenticate(
        self,
        payload: AuthenticateRequest,
        feedback_callback: Callable[[wos.WOSAPIFeedback], None] = None,
        timeout: float = None,
    ) -> AuthenticateResponse:
        """
        Authenticate a user

                Args:
                    payload: The message payload
                    feedback_callback: Function to call when progress updates are received
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.action(
            "@wos/dummy/user",
            "authenticate",
            serialized,
            "",
            feedback_callback,
            timeout,
        )

        # Convert result to expected type
        if result is not None:
            return AuthenticateResponse().parse(result)
        return None

    def action_delete_user(
        self,
        payload: DeleteUserRequest,
        feedback_callback: Callable[[wos.WOSAPIFeedback], None] = None,
        timeout: float = None,
    ) -> bytes:
        """
        Delete a user

                Args:
                    payload: The message payload
                    feedback_callback: Function to call when progress updates are received
                    timeout: Optional timeout in seconds

                Returns:
                    The result from the server

                Raises:
                    WOSAPIError: If the server returns an error
                    TimeoutError: If the operation times out
        """
        serialized = payload.SerializeToString()
        result = self._client.action(
            "@wos/dummy/user", "delete_user", serialized, "", feedback_callback, timeout
        )

        # Convert result to expected type
        if result is not None:
            return bytes().parse(result)
        return None

    def serve(self, service_handler: Any):
        """
        Register this service with the WOS system.

        Args:
            service_handler: An object that implements the service interface methods
        """
        # Validate the service handler has the required methods
        self._validate_service_handler(service_handler)

        # Create a wrapper for the service handler
        wrapped_handler = self._create_service_handler_wrapper(service_handler)

        return self._client.serve("@wos/dummy/user", wrapped_handler)

    def _validate_service_handler(self, service_handler: Any):
        """
        Validate that the service handler implements the required methods.

        Args:
            service_handler: An object that implements the service interface methods
        """
        # Check for required methods
        if not hasattr(service_handler, "req_create_user") or not callable(
            getattr(service_handler, "req_create_user")
        ):
            raise ValueError("Service handler must implement req_create_user method")
        if not hasattr(service_handler, "req_get_user") or not callable(
            getattr(service_handler, "req_get_user")
        ):
            raise ValueError("Service handler must implement req_get_user method")
        if not hasattr(service_handler, "req_list_users") or not callable(
            getattr(service_handler, "req_list_users")
        ):
            raise ValueError("Service handler must implement req_list_users method")
        if not hasattr(service_handler, "req_update_user") or not callable(
            getattr(service_handler, "req_update_user")
        ):
            raise ValueError("Service handler must implement req_update_user method")
        if not hasattr(service_handler, "act_authenticate") or not callable(
            getattr(service_handler, "act_authenticate")
        ):
            raise ValueError("Service handler must implement act_authenticate method")
        if not hasattr(service_handler, "cancel_authenticate") or not callable(
            getattr(service_handler, "cancel_authenticate")
        ):
            raise ValueError(
                "Service handler must implement cancel_authenticate method for cancellable actions"
            )
        if not hasattr(service_handler, "act_delete_user") or not callable(
            getattr(service_handler, "act_delete_user")
        ):
            raise ValueError("Service handler must implement act_delete_user method")
        if not hasattr(service_handler, "cancel_delete_user") or not callable(
            getattr(service_handler, "cancel_delete_user")
        ):
            raise ValueError(
                "Service handler must implement cancel_delete_user method for cancellable actions"
            )

    def _create_service_handler_wrapper(self, service_handler: Any):
        """
        Create a wrapper for the service handler that converts messages to/from the appropriate types.

        Args:
            service_handler: An object that implements the service interface methods

        Returns:
            A function that can be passed to the client's serve method
        """

        def wrapper(
            message: wos.WOSAPIMessage, feedback_handler: wos.WOSAPIFeedback = None
        ) -> Tuple[bytes, str]:
            # Route the message based on operation type and topic
            topic = message.topic
            error = None

            # Handle cancel operation for actions
            if message.op == wos.WOSAPIOperation.OP_CANCEL:
                if topic == "authenticate":
                    try:
                        service_handler.cancel_["authenticate"]()
                        return None, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "delete_user":
                    try:
                        service_handler.cancel_["delete", "user"]()
                        return None, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown topic for cancel: {topic}"

            # Handle request operations
            if message.op == wos.WOSAPIOperation.OP_REQUEST:
                if topic == "create_user":
                    # Parse input message
                    input_data = CreateUserRequest().parse(message.payload)
                    try:
                        result = service_handler.req_create_user(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "get_user":
                    # Parse input message
                    input_data = GetUserRequest().parse(message.payload)
                    try:
                        result = service_handler.req_get_user(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "list_users":
                    # Parse input message
                    input_data = ListUsersRequest().parse(message.payload)
                    try:
                        result = service_handler.req_list_users(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "update_user":
                    # Parse input message
                    input_data = UpdateUserRequest().parse(message.payload)
                    try:
                        result = service_handler.req_update_user(input_data)
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown request topic: {topic}"

            # Handle action operations
            elif message.op == wos.WOSAPIOperation.OP_ACTION:
                if topic == "authenticate":
                    # Parse input message
                    input_data = AuthenticateRequest().parse(message.payload)
                    try:
                        result = service_handler.act_authenticate(
                            input_data, feedback_handler
                        )
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                elif topic == "delete_user":
                    # Parse input message
                    input_data = DeleteUserRequest().parse(message.payload)
                    try:
                        result = service_handler.act_delete_user(
                            input_data, feedback_handler
                        )
                        # Serialize result to bytes
                        output_bytes = result.SerializeToString()
                        return output_bytes, None
                    except Exception as e:
                        return None, str(e)
                else:
                    return None, f"Unknown action topic: {topic}"
            else:
                return None, f"Unsupported operation type: {message.op}"

        return wrapper


class WOSClient(WOSBaseClient):

    def __init__(self, endpoint: str = ""):
        super().__init__(endpoint)
        self.main = MainModule(self)
        self._wos_dummy = WosDummyModule(self)
