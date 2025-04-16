import socket

def broadcast_sender():
    try:
        port = int(input("Enter port to send to: "))
        if not (0 < port < 65536):
            raise ValueError("Port must be between 1 and 65535")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
        return

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable broadcasting mode
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print("Type your message (Ctrl+C to stop):")
    try:
        while True:
            msg = input("> ")
            sock.sendto(msg.encode(), ('255.255.255.255', port))
    except KeyboardInterrupt:
        print("\nSender stopped.")
    finally:
        sock.close()


if __name__ == "__main__":
    broadcast_sender()
