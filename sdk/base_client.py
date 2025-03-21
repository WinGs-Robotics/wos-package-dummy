"""
WOS Python SDK - Base Client

Auto-generated Python SDK for WOS
"""

from typing import Any, Callable, Dict, List, Optional, Union
import datetime
import os
import threading
import time
import uuid
import queue
import websocket
import re
import requests

from .pb import wos as wos

import datetime
from typing import Optional


class WOSAPIError(Exception):
    pass


MAX_MESSAGE_ID = 2**31


def convert_base_type_to_bytes(value, type_name):
    """
    Convert a Python value to bytes based on protobuf type.

    Args:
            value: The Python value to convert
            type_name: The protobuf type name (string, int32, etc.)

    Returns:
            bytes representation of the value

    Raises:
            TypeError: If the value type doesn't match the expected protobuf type
    """
    import struct

    if type_name == "string":
        if not isinstance(value, str):
            raise TypeError(f"Expected str for string type, got {type(value)}")
        return value.encode("utf-8")

    elif type_name == "bytes":
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError(f"Expected bytes for bytes type, got {type(value)}")
        return bytes(value)

    elif type_name in ("int32", "sint32", "sfixed32"):
        if not isinstance(value, int):
            raise TypeError(f"Expected int for {type_name} type, got {type(value)}")
        return struct.pack("<i", value)

    elif type_name in ("uint32", "fixed32"):
        if not isinstance(value, int):
            raise TypeError(f"Expected int for {type_name} type, got {type(value)}")
        return struct.pack("<I", value)

    elif type_name in ("int64", "sint64", "sfixed64"):
        if not isinstance(value, int):
            raise TypeError(f"Expected int for {type_name} type, got {type(value)}")
        return struct.pack("<q", value)

    elif type_name in ("uint64", "fixed64"):
        if not isinstance(value, int):
            raise TypeError(f"Expected int for {type_name} type, got {type(value)}")
        return struct.pack("<Q", value)

    elif type_name == "float":
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected float for float type, got {type(value)}")
        return struct.pack("<f", float(value))

    elif type_name == "double":
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected float for double type, got {type(value)}")
        return struct.pack("<d", float(value))

    elif type_name == "bool":
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool for bool type, got {type(value)}")
        return struct.pack("?", value)

    else:
        raise ValueError(f"Unsupported protobuf type: {type_name}")


def convert_base_type_from_bytes(value, type_name):
    """
    Convert bytes to a Python value based on protobuf type.

    Args:
            value: The bytes to convert
            type_name: The protobuf type name (string, int32, etc.)

    Returns:
            Python value corresponding to the protobuf type

    Raises:
            ValueError: If the bytes cannot be converted to the specified type
    """
    import struct

    if not isinstance(value, bytes):
        raise TypeError(f"Expected bytes, got {type(value)}")

    if type_name == "string":
        return value.decode("utf-8")

    elif type_name == "bytes":
        return value

    elif type_name in ("int32", "sint32", "sfixed32"):
        return struct.unpack("<i", value)[0]

    elif type_name in ("uint32", "fixed32"):
        return struct.unpack("<I", value)[0]

    elif type_name in ("int64", "sint64", "sfixed64"):
        return struct.unpack("<q", value)[0]

    elif type_name in ("uint64", "fixed64"):
        return struct.unpack("<Q", value)[0]

    elif type_name == "float":
        return struct.unpack("<f", value)[0]

    elif type_name == "double":
        return struct.unpack("<d", value)[0]

    elif type_name == "bool":
        return struct.unpack("?", value)[0]

    else:
        raise ValueError(f"Unsupported protobuf type: {type_name}")


class RequestHandler:
    def __init__(self, feedback_callback=None):
        self._queue = queue.Queue[(bool, bytes)]()
        self._feedback_callback = feedback_callback
        self._is_done = False

    def on_message(self, msg: wos.WOSAPIMessage) -> bool:
        if msg.op == wos.WOSAPIOperation.OP_FEEDBACK and self._feedback_callback:
            feedback = wos.WOSAPIFeedback().parse(msg.payload)
            self._feedback_callback(feedback)
            return False

        if msg.op == wos.WOSAPIOperation.OP_ERROR:
            error_msg = msg.payload.decode("utf-8")
            self._queue.put((False, error_msg))

        elif msg.op == wos.WOSAPIOperation.OP_RESULT:
            self._queue.put((True, msg.payload))
        else:
            print(f"Unexpected message: {msg.op} for handler")

        self._is_done = True
        return True

    def get_result(self, timeout=None) -> bytes:
        try:
            success, result = self._queue.get(timeout=timeout)
            if not success:
                raise WOSAPIError(result)
            return result
        except queue.Empty:
            raise TimeoutError("Request timed out")


class ServiceHandler:
    def __init__(
        self,
        client: "WOSBaseClient",
        handle: Callable[
            [wos.WOSAPIMessage, Optional[Callable[[wos.WOSAPIFeedback], None]]], Any
        ],
        resource: str,
        id: int,
        instance: str = "",
    ):
        self._client = client
        self.resource = resource
        self.instance = instance
        self.handle = handle
        self.id = id
        self.queue = queue.Queue()

    def wait_result(self):
        res: wos.WOSAPIMessage = self.queue.get(timeout=10)
        if res.op == wos.WOSAPIOperation.OP_ACK:
            return True
        elif res.op == wos.WOSAPIOperation.OP_ERROR:
            raise WOSAPIError(res.payload.decode("utf-8"))

    def on_message(self, msg: wos.WOSAPIMessage):
        if msg.op == wos.WOSAPIOperation.OP_ACK:
            self.queue.put(msg)
        elif msg.op == wos.WOSAPIOperation.OP_ERROR:
            self.queue.put(msg)
        elif msg.op == wos.WOSAPIOperation.OP_CANCEL:
            self.handle(msg)
            self._client._send_api_message(
                id=msg.id,
                op=wos.WOSAPIOperation.OP_ACK,
                resource=self.resource,
                topic=msg.topic,
                instance=self.instance,
            )
        elif msg.op == wos.WOSAPIOperation.OP_REQUEST:
            try:
                result, error = self.handle(
                    msg,
                )
                if error:
                    raise Exception(error)
                self._client._send_api_message(
                    id=msg.id,
                    op=wos.WOSAPIOperation.OP_RESULT,
                    resource=self.resource,
                    topic=msg.topic,
                    instance=self.instance,
                    payload=result,
                )
            except Exception as e:
                self._client._send_api_message(
                    id=msg.id,
                    op=wos.WOSAPIOperation.OP_ERROR,
                    resource=self.resource,
                    topic=msg.topic,
                    instance=self.instance,
                    payload=str(e).encode("utf-8"),
                )
        elif msg.op == wos.WOSAPIOperation.OP_ACTION:
            try:
                result, error = self.handle(
                    msg,
                    lambda feedback: self._client._send_api_message(
                        id=msg.id,
                        op=wos.WOSAPIOperation.OP_FEEDBACK,
                        resource=self.resource,
                        topic=msg.topic,
                        instance=self.instance,
                        payload=feedback.SerializeToString(),
                    ),
                )
                if error:
                    raise Exception(error)
                self._client._send_api_message(
                    id=msg.id,
                    op=wos.WOSAPIOperation.OP_RESULT,
                    resource=self.resource,
                    topic=msg.topic,
                    instance=self.instance,
                    payload=result,
                )
            except Exception as e:
                self._client._send_api_message(
                    id=msg.id,
                    op=wos.WOSAPIOperation.OP_ERROR,
                    resource=self.resource,
                    topic=msg.topic,
                    instance=self.instance,
                    payload=str(e).encode("utf-8"),
                )


class WOSBaseClient:
    def __init__(self, endpoint: str = ""):
        """
        Initialize the WOS client.

        Args:
                endpoint: The server endpoint in format "host:port"
        """
        # Strip protocol if present
        if endpoint == "":
            endpoint = os.getenv("WOS_ENDPOINT", "localhost:15117")

        self.endpoint = re.sub(r"^(https?://|wss?://)", "", endpoint)
        self.ws = None
        self.subscriptions: Dict[
            str, Dict[str, Callable[[wos.WOSAPIMessage], None]]
        ] = {}  # topic -> dict of callbacks
        self.callbacks: Dict[int, RequestHandler] = {}  # id -> RequestHandler
        self.ws_thread = None
        self.running = False
        self.message_queue = queue.Queue()
        self.id = 0
        self.service_handler: ServiceHandler = None
        self.serve_request_id = 0

    def _generate_id(self):
        self.id += 1
        if self.id > MAX_MESSAGE_ID:
            self.id = 1
        return self.id

    def _subscription_key(self, resource: str, topic: str, instance: str):
        return f"{resource}/{topic}/{instance}"

    def connect(self, timeout=10):
        """
        Connect to the WOS server.

        Args:
                timeout: Connection timeout in seconds

        Returns:
                True if connection successful, False otherwise
        """
        if self.ws is not None:
            return True

        try:
            ws_endpoint = f"ws://{self.endpoint}/api/ws"
            self.ws = websocket.create_connection(ws_endpoint, timeout=timeout)
            self.running = True

            # Start the message handling thread
            self.ws_thread = threading.Thread(target=self._message_loop)
            self.ws_thread.daemon = True
            self.ws_thread.start()

            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.ws = None
            return False

    def disconnect(self):
        """Disconnect from the WOS server."""
        self.running = False
        if self.ws:
            self.ws.close()
            self.ws = None

        if self.ws_thread:
            self.ws_thread.join(timeout=1)
            self.ws_thread = None

    def _message_loop(self):
        """Background thread to handle incoming WebSocket messages."""
        last_ping_time = time.time()
        ping_interval = 30  # seconds

        while self.running and self.ws:
            try:
                self.ws.settimeout(ping_interval + 5)

                # Check if connection is still open
                if not self.ws.connected:
                    print("Connection lost")
                    self.running = False
                    break

                # Send ping periodically
                current_time = time.time()
                if current_time - last_ping_time > ping_interval:
                    self.ws.ping()
                    last_ping_time = current_time

                binary_data = self.ws.recv()
                if binary_data:
                    msg = wos.WOSAPIMessage().parse(binary_data)
                    self._handle_message(msg)

            except (
                websocket.WebSocketTimeoutException,
                websocket.WebSocketConnectionClosedException,
            ):
                # Check if connection is still alive with a ping
                try:
                    self.ws.ping()
                    last_ping_time = time.time()
                except:
                    print("Server disconnected")
                    self.running = False
                    break

            except Exception as e:
                print(f"Error in message loop: {e}")
                self.running = False
                break

    def _handle_message(self, msg: wos.WOSAPIMessage):
        """Handle received WebSocket messages."""
        if (
            msg.op == wos.WOSAPIOperation.OP_ACK
            or msg.op == wos.WOSAPIOperation.OP_ERROR
        ) and msg.id == self.serve_request_id:

            if self.service_handler:
                self.service_handler.on_message(msg)
        elif (
            msg.op == wos.WOSAPIOperation.OP_REQUEST
            or msg.op == wos.WOSAPIOperation.OP_ACTION
            or msg.op == wos.WOSAPIOperation.OP_CANCEL
        ):
            if self.service_handler:
                self.service_handler.on_message(msg)
            else:
                print(f"No service handler registered for request: {msg.op}")

        elif msg.op in [
            wos.WOSAPIOperation.OP_RESULT,
            wos.WOSAPIOperation.OP_ERROR,
            wos.WOSAPIOperation.OP_FEEDBACK,
        ]:
            handler = self.callbacks.get(msg.id)
            if handler:
                if handler.on_message(msg):
                    del self.callbacks[msg.id]
            else:
                print(f"No handler registered for id: {msg.id}, op: {msg.op}")

        elif msg.op == wos.WOSAPIOperation.OP_PUBLISH:
            sub_topic = self._subscription_key(msg.resource, msg.topic, msg.instance)
            for topic, callbacks in self.subscriptions.items():
                if sub_topic == topic:
                    for callback in callbacks.values():
                        try:
                            callback(msg)
                        except Exception as e:
                            print(f"Error in subscription callback: {e}")

    def _send_api_message(
        self,
        id: int,
        op: wos.WOSAPIOperation,
        resource: str,
        topic: str,
        payload: bytes = b"",
        instance: str = "",
    ):
        """Send an API message to the server."""
        if not self.ws:
            raise ConnectionError("Not connected to WOS server")

        # Create a timestamp
        timestamp = datetime.datetime.now()

        # Create the API message
        api_message = wos.WOSAPIMessage(
            id=id,
            op=op,
            topic=topic,
            payload=payload,
            resource=resource,
            instance=instance,
            timestamp=timestamp,
        )

        self.ws.send_binary(api_message.SerializeToString())

    def publish(self, resource: str, topic: str, payload: bytes, instance: str = ""):
        self._send_api_message(
            0, wos.WOSAPIOperation.OP_PUBLISH, resource, topic, payload, instance
        )

    def subscribe(
        self,
        resource: str,
        topic: str,
        callback: Callable[[wos.WOSAPIMessage], None],
        instance: str = "",
    ):

        sub_topic = self._subscription_key(resource, topic, instance)
        sub_key = uuid.uuid4().hex
        if sub_topic not in self.subscriptions:
            self.subscriptions[sub_topic] = {}
            self._send_api_message(
                id=0,
                op=wos.WOSAPIOperation.OP_SUBSCRIBE,
                resource=resource,
                topic=topic,
                instance=instance,
            )

        self.subscriptions[sub_topic][sub_key] = callback
        return sub_key

    def unsubscribe(self, key: str):

        sub_topic = None

        for sub_key, subs in self.subscriptions.items():
            if key in subs:
                sub_topic = sub_key
                del subs[key]

        if len(self.subscriptions[sub_topic]) == 0:
            del self.subscriptions[sub_topic]
            resource, topic, instance = sub_topic.split("/")
            self._send_api_message(
                id=0,
                op=wos.WOSAPIOperation.OP_UNSUBSCRIBE,
                resource=resource,
                topic=topic,
                instance=instance,
            )

    def request(
        self,
        resource: str,
        topic: str,
        payload: bytes = b"",
        instance: str = "",
        timeout: float = None,
    ):
        """
        Send a request and wait for a response.

        Args:
                topic: The request topic
                payload: The request payload
                timeout: Timeout in seconds

        Returns:
                bytes: The response payload

        Raises:
                WOSAPIError: If the server returns an error
                TimeoutError: If the request times out
        """
        id = self._generate_id()
        handler = RequestHandler()
        self.callbacks[id] = handler
        self._send_api_message(
            id,
            wos.WOSAPIOperation.OP_REQUEST,
            resource=resource,
            instance=instance,
            topic=topic,
            payload=payload,
        )
        return handler.get_result(timeout)

    def action(
        self,
        resource: str,
        topic: str,
        payload: bytes = b"",
        instance: str = "",
        feedback_callback: Callable[[wos.WOSAPIFeedback], None] = None,
        timeout: float = None,
    ):
        id = self._generate_id()
        handler = RequestHandler(feedback_callback)
        self.callbacks[id] = handler
        self._send_api_message(
            id,
            wos.WOSAPIOperation.OP_ACTION,
            resource=resource,
            topic=topic,
            instance=instance,
            payload=payload,
        )
        return handler.get_result(timeout)

    def cancel(self, resource: str, topic: str, instance: str):
        self._send_api_message(
            0,
            wos.WOSAPIOperation.OP_CANCEL,
            resource=resource,
            topic=topic,
            instance=instance,
        )

    def serve(
        self,
        resource: str,
        service_handler: Callable[[wos.WOSAPIMessage], wos.WOSAPIMessage],
        instance: str = "",
    ):
        if self.service_handler:
            raise ValueError(
                "Service handler already registered. You can only register one service for each client."
            )
        self.service_handler = ServiceHandler(self, service_handler, resource, instance)
        self.serve_request_id = self._generate_id()

        self._send_api_message(
            self.serve_request_id,
            wos.WOSAPIOperation.OP_REGISTER_SERVICE,
            resource=resource,
            topic="",
            instance=instance,
        )

        return self.service_handler.wait_result()

    def unserve(self):
        if not self.service_handler:
            return
        self.service_handler = None
        self._send_api_message(
            0,
            wos.WOSAPIOperation.OP_REMOVE_SERVICE,
            resource=self.service_handler.resource,
            instance=self.service_handler.instance,
        )

    # Utility methods
    def get_env(self):
        response = requests.get(f"http://{self.endpoint}/api/env")
        return response.json()

    def get_wos_description(self):
        response = requests.get(f"http://{self.endpoint}/api/desc")
        return response.json()

    def get_endpoints(self):
        response = requests.get(f"http://{self.endpoint}/api/endpoints")
        return response.json().get("endpoints", [])

    def fetch_node_log(self, id_str: str):
        response = requests.get(f"http://{self.endpoint}/logs/{id_str}.log")
        return response.text

    def get_health(self):
        response = requests.get(f"http://{self.endpoint}/api/health")
        return response.json()

    def get_runtime(self):
        response = requests.get(f"http://{self.endpoint}/api/runtime")
        return response.json()

    def get_diagnose(self):
        response = requests.get(f"http://{self.endpoint}/api/diagonse")
        return response.json()

    def get_context(self):
        response = requests.get(f"http://{self.endpoint}/api/go")
        return response.text
