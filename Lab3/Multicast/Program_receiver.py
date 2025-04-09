import socket
import struct

def multicast_receiver():
    ip = input("Podaj adres multicast (np. 224.0.0.1): ")
    port = int(input("Podaj port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))

    mreq = struct.pack("4sl", socket.inet_aton(ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Oczekiwanie na wiadomości...")
    while True:
        msg, addr = sock.recvfrom(1024)
        print(f"[{addr}] {msg.decode()}")

if __name__ == "__main__":
  multicast_receiver()
