import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(1)

print("Server is running...")

conn, addr = server.accept()
print("Client connected:", addr)

while True:
    data = conn.recv(1024).decode()

    if not data:
        break

    print("Client:", data)

    reply = input("You (server): ")
    conn.send(reply.encode())

conn.close()