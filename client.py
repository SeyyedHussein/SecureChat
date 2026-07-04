import socket
import threading
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

name = input("Enter username: ")
client.send(name.encode())

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