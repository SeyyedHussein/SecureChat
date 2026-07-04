import socket
import threading
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

username = input("Enter username: ")
password = input("Enter password: ")

client.send(f"LOGIN|{username}|{password}".encode())

response = client.recv(1024).decode()

if response == "AUTH_FAIL":
    print("Login failed!")
    client.close()
    sys.exit()

print("Login successful!")

name = username


def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            print("\r" + msg)
            print(f"{name}: ", end="", flush=True)
        except:
            break


threading.Thread(target=receive, daemon=True).start()

while True:
    try:
        msg = input(f"{name}: ")
        client.send(msg.encode())
    except:
        print("Disconnected")
        client.close()
        sys.exit()