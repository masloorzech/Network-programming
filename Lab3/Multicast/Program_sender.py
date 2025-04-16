import socket   # Import the socket module to enable network communication
import struct   # Import struct for packing TTL value into binary format


def multicast_sender():
    # Ask the user for the multicast address and port
    ip = input("Enter multicast address (e.g., 224.0.0.1): ")
    port = int(input("Enter port: "))

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Set the TTL (Time to Live) for multicast packets
    # TTL = 1 means the message won't leave the local network
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    print("Type your message (Ctrl+C to stop):")
    try:
        while True:
            # Read user input from the terminal
            msg = input("> ")

            # Send the message to the multicast group
            sock.sendto(msg.encode(), (ip, port))
    except KeyboardInterrupt:
        # Gracefully handle interruption (e.g., Ctrl+C)
        print("\nSender stopped.")

if __name__ == "__main__":
    multicast_sender()
