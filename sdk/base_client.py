"""
WOS Python SDK - Base Client

Auto-generated Python SDK for WOS
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import datetime
import os
import threading
import time
import uuid
import queue
import websocket
import re
import requests

from .pb import *

import datetime
from typing import Optional


class WOSAPIError(Exception):
    pass


MAX_MESSAGE_ID = 2**31


class RequestHandler:
    def __init__(self, feedback_callback=None):
        self._queue = queue.Queue[Tuple[bool, bytes]]()
        self._feedback_callback = feedback_callback
        self._is_done = False

    def on_message(self, msg: WOSAPIMessage) -> bool:

        if msg.op == WOSAPIOperation.OP_FEEDBACK:
            if self._feedback_callback:
                feedback = WOSAPIFeedback().parse(msg.payload)
                self._feedback_callback(feedback)
            return False
        if msg.op == WOSAPIOperation.OP_ACK:
            self._queue.put((True, b""))
            return True

        if msg.op == WOSAPIOperation.OP_ERROR:
            self._queue.put((False, msg.payload))

        elif msg.op == WOSAPIOperation.OP_RESULT:
            self._queue.put((True, msg.payload))
        else:
            print(f"Unexpected message: {msg.op} for handler")

        self._is_done = True
        return True

    def get_result(self, timeout=None) -> bytes:
        try:
            success, result = self._queue.get(timeout=timeout)
            if not success:
                raise WOSAPIError(result.decode("utf-8"))
            return result
        except queue.Empty:
            raise TimeoutError("Request timed out")


class ServiceHandler:
    resource: str
    instance: str

    def __init__(
        self,
        client: "WOSBaseClient",
        handle: Callable[
            [WOSAPIMessage, Optional[Callable[[WOSAPIFeedback], None]]], bytes
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
        res: WOSAPIMessage = self.queue.get(timeout=10)
        if res.op == WOSAPIOperation.OP_ACK:
            return True
        elif res.op == WOSAPIOperation.OP_ERROR:
            raise WOSAPIError(res.payload.decode("utf-8"))

    def on_message(self, msg: WOSAPIMessage):
        if msg.op == WOSAPIOperation.OP_ACK:
            self.queue.put(msg)
        elif msg.op == WOSAPIOperation.OP_ERROR:
            self.queue.put(msg)
        elif msg.op == WOSAPIOperation.OP_CANCEL:
            self.handle(msg, None)
            self._client._send_api_message(
                id=msg.id,
                op=WOSAPIOperation.OP_ACK,
                resource=self.resource,
                topic=msg.topic,
                instance=self.instance,
            )
        elif msg.op == WOSAPIOperation.OP_REQUEST:
            try:
                result = self.handle(msg, None)
                self._client._send_api_message(
                    id=msg.id,
                    op=WOSAPIOperation.OP_RESULT,
                    resource=self.resource,
                    topic=msg.topic,
                    instance=self.instance,
                    payload=result,
                )
            except Exception as e:
                self._client._send_api_message(
                    id=msg.id,
                    op=WOSAPIOperation.OP_ERROR,
                    resource=self.resource,
                    topic=msg.topic,
                    instance=self.instance,
                    payload=str(e).encode("utf-8"),
                )
        elif msg.op == WOSAPIOperation.OP_ACTION:
            try:
                result = self.handle(
                    msg,
                    lambda feedback: self._client._send_api_message(
                        id=msg.id,
                        op=WOSAPIOperation.OP_FEEDBACK,
                        resource=self.resource,
                        topic=msg.topic,
                        instance=self.instance,
                        payload=feedback.SerializeToString(),
                    ),
                )
                self._client._send_api_message(
                    id=msg.id,
                    op=WOSAPIOperation.OP_RESULT,
                    resource=self.resource,
                    topic=msg.topic,
                    instance=self.instance,
                    payload=result,
                )
            except Exception as e:
                self._client._send_api_message(
                    id=msg.id,
                    op=WOSAPIOperation.OP_ERROR,
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
        self.subscriptions: Dict[str, Dict[str, Callable[[WOSAPIMessage], None]]] = (
            {}
        )  # topic -> dict of callbacks
        self.callbacks: Dict[int, RequestHandler] = {}  # id -> RequestHandler
        self.ws_thread = None
        self.running = False
        self.message_queue = queue.Queue()
        self.id = 0
        self.service_handler: Optional[ServiceHandler] = None
        self.serve_request_id = 0
        self.done_queue = queue.Queue()

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
                    msg = WOSAPIMessage().parse(binary_data)  # type: ignore
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

    def _handle_message(self, msg: WOSAPIMessage):
        """Handle received WebSocket messages."""
        if (
            msg.op == WOSAPIOperation.OP_ACK or msg.op == WOSAPIOperation.OP_ERROR
        ) and msg.id == self.serve_request_id:

            if self.service_handler:
                self.service_handler.on_message(msg)
        elif (
            msg.op == WOSAPIOperation.OP_REQUEST
            or msg.op == WOSAPIOperation.OP_ACTION
            or msg.op == WOSAPIOperation.OP_CANCEL
        ):
            if self.service_handler:
                self.service_handler.on_message(msg)
            else:
                print(f"No service handler registered for request: {msg.op}")

        elif msg.op in [
            WOSAPIOperation.OP_RESULT,
            WOSAPIOperation.OP_ERROR,
            WOSAPIOperation.OP_FEEDBACK,
        ]:
            handler = self.callbacks.get(msg.id)
            if handler:
                if handler.on_message(msg):
                    del self.callbacks[msg.id]
            else:
                print(f"No handler registered for id: {msg.id}, op: {msg.op}")

        if msg.op == WOSAPIOperation.OP_PUBLISH:
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
        op: WOSAPIOperation,
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
        api_message = WOSAPIMessage(
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
            0, WOSAPIOperation.OP_PUBLISH, resource, topic, payload, instance
        )

    def subscribe(
        self,
        resource: str,
        topic: str,
        callback: Callable[[WOSAPIMessage], None],
        instance: str = "",
    ):

        sub_topic = self._subscription_key(resource, topic, instance)
        sub_key = uuid.uuid4().hex
        if sub_topic not in self.subscriptions:
            self.subscriptions[sub_topic] = {}
            self._send_api_message(
                id=0,
                op=WOSAPIOperation.OP_SUBSCRIBE,
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
        if sub_topic:
            if len(self.subscriptions[sub_topic]) == 0:
                del self.subscriptions[sub_topic]
                resource, topic, instance = sub_topic.split("/")
                self._send_api_message(
                    id=0,
                    op=WOSAPIOperation.OP_UNSUBSCRIBE,
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
        timeout: Optional[float] = None,
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
            WOSAPIOperation.OP_REQUEST,
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
        feedback_callback: Optional[Callable[[WOSAPIFeedback], None]] = None,
        timeout: Optional[float] = None,
    ):
        id = self._generate_id()
        handler = RequestHandler(feedback_callback)
        self.callbacks[id] = handler
        self._send_api_message(
            id,
            WOSAPIOperation.OP_ACTION,
            resource=resource,
            topic=topic,
            instance=instance,
            payload=payload,
        )
        return handler.get_result(timeout)

    def cancel(self, resource: str, topic: str, instance: str = ""):

        id = self._generate_id()
        handler = RequestHandler()
        self.callbacks[id] = handler
        self._send_api_message(
            id,
            WOSAPIOperation.OP_CANCEL,
            resource=resource,
            topic=topic,
            instance=instance,
        )
        return handler.get_result()

    def serve(
        self,
        resource: str,
        service_handler: Callable[
            [WOSAPIMessage, Optional[Callable[[WOSAPIFeedback], None]]], bytes
        ],
        instance: str = "",
    ):
        if self.service_handler:
            raise ValueError(
                "Service handler already registered. You can only register one service for each client."
            )
        self.serve_request_id = self._generate_id()
        self.service_handler = ServiceHandler(
            self, service_handler, resource, self.serve_request_id, instance
        )

        self._send_api_message(
            self.serve_request_id,
            WOSAPIOperation.OP_REGISTER_SERVICE,
            resource=resource,
            topic="",
            instance=instance,
        )

        return self.service_handler.wait_result()

    def unserve(self):
        if not self.service_handler:
            return

        self._send_api_message(
            0,
            WOSAPIOperation.OP_REMOVE_SERVICE,
            resource=self.service_handler.resource,
            topic="",
            instance=self.service_handler.instance,
        )

        self.service_handler = None

    def spin(self, timeout=None):
        """
        Block until the message connection is done or timeout occurs.

        This function will return once the message connection is done
        or when the specified timeout is reached.

        Args:
            timeout: Maximum time to wait in seconds. None means wait indefinitely.

        Returns:
            True if the connection ended normally, False if timed out.
        """
        if not self.ws_thread:
            return True

        # Join the thread with timeout
        self.ws_thread.join(timeout=timeout)

        # Return True if the thread is no longer alive (joined successfully)
        # Return False if it's still running (timeout occurred)
        return not self.ws_thread.is_alive()

    # Utility methods
    def get_env(self):
        response = requests.get(f"http://{self.endpoint}/api/env")
        return response.json()

    def get_wos_description(self):
        response = requests.get(f"http://{self.endpoint}/api/desc")
        return WOSDescription().from_dict(response.json())

    def get_endpoints(self) -> List[str]:
        response = requests.get(f"http://{self.endpoint}/api/endpoints")
        return response.json().get("endpoints", [])

    def fetch_node_log(self, id_str: str) -> str:
        response = requests.get(f"http://{self.endpoint}/logs/{id_str}.log")
        return response.text

    def get_health(self):
        response = requests.get(f"http://{self.endpoint}/api/health")
        return WOSHeartbeat().from_dict(response.json())

    def get_runtime(self) -> Union[WOSNodeInfoList, WOSServiceList]:
        response = requests.get(f"http://{self.endpoint}/api/runtime")
        return response.json()

    def get_diagnose(self):
        response = requests.get(f"http://{self.endpoint}/api/diagonse")
        return WOSDiagnoseInfo().from_dict(response.json())

    def get_context(self) -> str:
        response = requests.get(f"http://{self.endpoint}/api/go")
        return response.text
