import socket       # Import the socket module to enable network communication
import threading    # Import threading to handle receiving messages in parallel


# Define error and information signs for clearer messaging
ERROR_SIGN = "❌"  # Error sign, indicates error when it occurs while the program is alive
INFORMATION_SIGN = "ℹ️"  # Information sign, used for general information messages

# Function responsible for receiving data from the server
def recv_data(sock):
    total_received = 0 # Track the total number of bytes received
    while True:
        try:
            # Attempt to receive up to 1024 bytes of data
            data = sock.recv(1024)
            if not data:
                # If no data is received, the server has closed the connection
                print(f"\n{INFORMATION_SIGN} Połączenie zamknięte przez serwer.")
                break
            total_received += len(data) # Add the number of bytes received to the total
            print(f"[RECV {len(data)} B] {data.decode()}") # Decode and print the message
        except Exception as e:
            # If an error occurs while receiving, print an error message and exit the loop
            print(f"{ERROR_SIGN} Błąd podczas odbioru: {e}")
            break

# Main function which handles user input, connection setup, sending, and receiving data
def main():
    try:
        # Prompt user to enter server IP address or domain name
        ip = input("Podaj adres IP lub nazwę domeny serwera: ")
        port_str = input("Podaj port: ")

        try:
            # Convert port to integer and validate its range
            port = int(port_str)
            assert 0 < port < 65536
        except:
            print(f"{ERROR_SIGN} Nieprawidłowy port.")
            return

        print(f"{INFORMATION_SIGN} Tworzenie gniazda...")

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(f"{INFORMATION_SIGN} Łączenie z {ip}:{port}...")

        # Connect to the specified server and port
        sock.connect((ip, port))
        print("[CONNECTED] Połączono z serwerem.")
        print("Wpisuj wiadomości do wysłania. Wpisz 'exit' aby zakończyć.")

        # Start a separate thread to handle receiving messages from the server
        recv_thread = threading.Thread(target=recv_data, args=(sock,), daemon=True)
        recv_thread.start()

        total_sent = 0  # Track the total number of bytes sent
        while True:
            # Read user input from the console
            msg = input()
            if msg.lower() == 'exit':
                # If the user types 'exit', break the loop and end the connection
                break
            try:
                # Encode and send the message
                sent = sock.send(msg.encode())
                total_sent += sent # Add sent byte count to the total
                print(f"[SENT {sent} B] {msg}")
            except Exception as e:
                # If sending fails, show an error and break the loop
                print(f"{ERROR_SIGN} Nie udało się wysłać wiadomości: {e}")
                break

        # Close the socket after exiting the loop
        sock.close()
        print(f"{INFORMATION_SIGN} Połączenie zakończone. Łącznie wysłano: {total_sent} B.")

    except Exception as e:
        # Catch any unexpected exceptions during execution
        print(f"{ERROR_SIGN} Błąd ogólny: {e}")

# Entry point of the program
if __name__ == "__main__":
    main()
