# multicast_sender.py
import socket
import struct

def multicast_sender():
    ip = input("Podaj adres multicast (np. 224.0.0.1): ")
    port = int(input("Podaj port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    print("Wpisz wiadomość (Ctrl+C by zakończyć):")
    try:
        while True:
            msg = input("> ")
            sock.sendto(msg.encode(), (ip, port))
    except KeyboardInterrupt:
        print("\nKoniec wysyłania.")
