import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

while True:
    msg = input("You (client): سلام")

    client.send(msg.encode())

    reply = client.recv(1024).decode()
    print("Server:", reply)
