from sdk import WOSClient
import time

if __name__ == "__main__":
    print("Dummy User start...")
    client = WOSClient()
    client.connect()

    def service_handle(msg):
        print(f"Service message: {msg}")

        return "Service result".encode(), None

    client.serve("@wos/dummy/user", service_handle)
    while True:
        print("user is running...")
        time.sleep(5)
