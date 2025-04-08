import socket
import threading
import sys

MAX_CLIENTS = 3
PORT = 7  # domyślny port, może być zmieniony przez argumenty

active_clients = {}  # client_number: (ip, port)
client_counter = 1
lock = threading.Lock()

def handle_client(conn, addr, client_id):
    print(f"[#{client_id}] Connected: {addr[0]}:{addr[1]}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode('utf-8', errors='ignore')
            print(f"[#{client_id}] Received ({len(data)} bytes): {message}")
            conn.sendall(data)  # ECHO
    except Exception as e:
        print(f"[#{client_id}] Error: {e}")
    finally:
        with lock:
            del active_clients[client_id]
        print(f"[#{client_id}] Disconnected.")
        conn.close()

def accept_clients(server_socket):
    global client_counter
    while True:
        try:
            conn, addr = server_socket.accept()
            with lock:
                if len(active_clients) >= MAX_CLIENTS:
                    print(f"[!] Too many connections. Rejecting {addr}.")
                    conn.sendall(b"SERVER BUSY\n")
                    conn.close()
                    continue
                client_id = client_counter
                client_counter += 1
                active_clients[client_id] = addr
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
            client_thread.daemon = True
            client_thread.start()
            show_active_clients()
        except Exception as e:
            print(f"[!] Accept error: {e}")
            break

def show_active_clients():
    with lock:
        print("\n--- Active Clients ---")
        for cid, (ip, port) in active_clients.items():
            print(f"[#{cid}] {ip}:{port}")
        print("----------------------\n")

def start_server(host='0.0.0.0', port=PORT):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"[i] Server listening on {host}:{port}")
    except Exception as e:
        print(f"[!] Failed to start server: {e}")
        sys.exit(1)

    try:
        accept_thread = threading.Thread(target=accept_clients, args=(server_socket,))
        accept_thread.daemon = True
        accept_thread.start()

        while True:
            cmd = input("Type 'exit' to shut down: ").strip()
            if cmd.lower() == "exit":
                break
    except KeyboardInterrupt:
        print("\n[i] Shutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("[!] Invalid port number. Using default port 7.")
    start_server(port=port)
