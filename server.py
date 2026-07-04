import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen()

print("Server is running...")

clients = {}

def broadcast(msg, sender=None):
    for c in clients:
        if c != sender:
            try:
                c.send(msg.encode())
            except:
                c.close()
                remove(c)

def remove(conn):
    if conn in clients:
        name = clients[conn]
        del clients[conn]
        broadcast(f"{name} left the chat")

def handle(conn, addr):
    try:
        name = conn.recv(1024).decode().strip()
        clients[conn] = name

        broadcast(f"{name} joined the chat")
        print(f"{name} connected")

        while True:
            msg = conn.recv(1024).decode().strip()
            if not msg:
                break

            final_msg = f"{name}: {msg}"
            print(final_msg)
            broadcast(final_msg, conn)

    except:
        pass

    remove(conn)
    conn.close()

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()