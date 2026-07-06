import socket
import threading

def load_users():
    users = {}

    with open("users.txt", "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            username, password = line.split(":")
            users[username] = password

    return users

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
        login_data = conn.recv(1024).decode().strip()

        parts = login_data.split("|")

        if len(parts) != 3 or parts[0] != "LOGIN":
            conn.send("AUTH_FAIL".encode())
            conn.close()
            return

        username = parts[1]
        password = parts[2]

        if username not in users or users[username] != password:
            conn.send("AUTH_FAIL".encode())
            conn.close()
            return

        conn.send("AUTH_OK".encode())

        name = username
        clients[conn] = name

        broadcast(f"{name} joined the chat")
        print(f"{name} connected")

        while True:
            msg = conn.recv(1024).decode().strip()

            if not msg:
                break

            if msg == "/users":
                online = "Online users:\n" + "\n".join(clients.values())
                conn.send(online.encode())
                continue

            final_msg = f"{name}: {msg}"
            print(final_msg)
            broadcast(final_msg, conn)

    except Exception as e:
        print(e)

    remove(conn)
    conn.close()

users = load_users()

print(users)

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()