import socket
import threading

def recv_data(sock):
    total_received = 0
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[INFO] Połączenie zamknięte przez serwer.")
                break
            total_received += len(data)
            print(f"[RECV {len(data)} B] {data.decode()}")
        except Exception as e:
            print(f"[ERROR] Błąd podczas odbioru: {e}")
            break

def main():
    try:
        ip = input("Podaj adres IP lub nazwę domeny serwera: ")
        port_str = input("Podaj port: ")

        try:
            port = int(port_str)
            assert 0 < port < 65536
        except:
            print("[ERROR] Nieprawidłowy port.")
            return

        print("[INFO] Tworzenie gniazda...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(f"[INFO] Łączenie z {ip}:{port}...")
        sock.connect((ip, port))
        print("[CONNECTED] Połączono z serwerem.")
        print("Wpisuj wiadomości do wysłania. Wpisz 'exit' aby zakończyć.")

        recv_thread = threading.Thread(target=recv_data, args=(sock,), daemon=True)
        recv_thread.start()

        total_sent = 0
        while True:
            msg = input()
            if msg.lower() == 'exit':
                break
            try:
                sent = sock.send(msg.encode())
                total_sent += sent
                print(f"[SENT {sent} B] {msg}")
            except Exception as e:
                print(f"[ERROR] Nie udało się wysłać wiadomości: {e}")
                break

        sock.close()
        print(f"[INFO] Połączenie zakończone. Łącznie wysłano: {total_sent} B.")

    except Exception as e:
        print(f"[ERROR] Błąd ogólny: {e}")

if __name__ == "__main__":
    main()
