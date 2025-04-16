import socket


def broadcast_receiver():
    try:
        port = int(input("Enter port to listen on: "))
        if not (0 < port < 65536):
            raise ValueError("Port must be between 1 and 65535")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
        return

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Allow reuse of address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to all interfaces on the given port
    try:
        sock.bind(('', port))
    except Exception as e:
        print(f"Failed to bind socket: {e}")
        return

    print(f"Listening for broadcast messages on port {port}...")

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"[{addr}] {data.decode()}")
    except KeyboardInterrupt:
        print("\nReceiver stopped.")
    finally:
        sock.close()


if __name__ == "__main__":
    broadcast_receiver()
