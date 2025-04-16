import socket # Import the socket module to enable network
import struct # Import struct for packing TTL value into binary format

def multicast_receiver():
    # Ask the user for multicast group address and port
    ip = input("Enter multicast address (e.g., 224.0.0.1): ")
    port = int(input("Enter port: "))

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Allow multiple programs to bind to the same address and port (useful for multicast)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to all interfaces on the given port
    sock.bind(('', port))

    # Join the multicast group on all interfaces (0.0.0.0)
    mreq = struct.pack("4s4s", socket.inet_aton(ip), socket.inet_aton("0.0.0.0"))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Waiting for messages...")
    try:
        while True:
            # Receive up to 1024 bytes from the socket
            msg, addr = sock.recvfrom(1024)
            # Decode and display the received message along with the sender's address
            print(f"[{addr}] {msg.decode()}")
    except KeyboardInterrupt:
        # Close the socket on user interruption (Ctrl+C)
        print("\nShutting down receiver...")
        sock.close()

if __name__ == "__main__":
    multicast_receiver()
