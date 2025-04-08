import socket
import signal
import sys

DEFAULT_PORT = 7
BUFFER_SIZE = 1024
client_counter = 0
server_socket = None

def cleanup(signum=None, frame=None):
    global server_socket
    print("\n[INFO] Zamykanie serwera...")
    if server_socket:
        server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

def main():
    global server_socket, client_counter

    try:
        port_input = input("Podaj port (domyślnie 7): ")
        port = int(port_input) if port_input.strip() else DEFAULT_PORT
    except ValueError:
        print("[WARN] Błędny port, używam domyślnego (7)")
        port = DEFAULT_PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"[INFO] Serwer nasłuchuje na porcie {port}...\n")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
        except OSError as e:
            print(f"[ERROR] Błąd przy accept(): {e}")
            continue

        client_counter += 1
        print(f"[INFO] Połączenie #{client_counter} od {client_address[0]}:{client_address[1]}")

        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    print(f"[INFO] Klient #{client_counter} rozłączył się.")
                    break

                print(f"[#%d] Odebrano %d B: \"%s\"" % (client_counter, len(data), data.decode('utf-8', errors='replace')))
                client_socket.sendall(data)

        except ConnectionError as e:
            print(f"[WARN] Błąd połączenia z klientem #{client_counter}: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
