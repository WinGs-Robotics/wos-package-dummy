from sdk import WOSSDK
import time

if __name__ == "__main__":
    print("Dummy Post started...")
    client = WOSSDK()
    client.connect()

    def service_handle(msg):
        print(f"Service message: {msg}")

        return "Service result".encode(), None

    client.serve("wos/dummy/post", service_handle)
    while True:
        print("post is running...")
        time.sleep(5)
