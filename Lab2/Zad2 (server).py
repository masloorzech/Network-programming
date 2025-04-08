import socket   # Import the socket module to enable network communication
import signal   # Import signal module for handling interruption signals
import sys      # Import sys to handle system-level operations such as exiting the program

DEFAULT_PORT = 7        # Default port number for the server
BUFFER_SIZE = 1024      # Size of the buffer for receiving data
client_counter = 0      # Counter to track the number of connected clients
server_socket = None    # Variable to store the server socket object

# Define error and information signs for clearer messaging
ERROR_SIGN = "❌"        # Error sign, indicates error when it occurs while the program is alive
INFORMATION_SIGN = "ℹ️"  # Information sign, used for general information messages
WARNING_SIGN = "⚠️"      # Warning sign, indicates warnings while the program is alive

# Function to handle cleanup tasks when the server is interrupted
def cleanup(signum=None, frame=None):
    global server_socket
    print(f"\n{INFORMATION_SIGN} Zamykanie serwera...")
    if server_socket:
        server_socket.close() # Close the server socket
    sys.exit(0)  # Exit the program

# Set up the signal handler for SIGINT (Ctrl+C) to invoke cleanup function
signal.signal(signal.SIGINT, cleanup)

def main():
    global server_socket, client_counter

    try:
        # Prompt the user for a port, defaulting to port 7 if not provided
        port_input = input("Podaj port (domyślnie 7): ")
        port = int(port_input) if port_input.strip() else DEFAULT_PORT
    except ValueError:
        # If an invalid port is provided, fall back to the default port
        print(f"{WARNING_SIGN} Błędny port, używam domyślnego (7)")
        port = DEFAULT_PORT

    # Create the server socket for IPv4 and TCP connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of local addresses

    # Bind the server socket to the specified address and port, then start listening
    server_socket.bind(('', port))  # Bind to all available interfaces
    server_socket.listen(5)         # Maximum number of queued connections
    print(f"{INFORMATION_SIGN} Serwer nasłuchuje na porcie {port}...\n")

    # Main server loop to accept and handle client connections
    while True:
        try:
            # Wait for a client connection
            client_socket, client_address = server_socket.accept()
        except OSError as e:
            # Handle errors during the accept() call
            print(f"{ERROR_SIGN} Błąd przy accept(): {e}")
            continue

        # Increment the client counter and print connection details
        client_counter += 1
        print(f"{INFORMATION_SIGN} Połączenie #{client_counter} od {client_address[0]}:{client_address[1]}")

        try:
            # Loop to receive and handle data from the client
            while True:
                # Receive data from the client
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    # If no data is received, the client has disconnected
                    print(f"{INFORMATION_SIGN} Klient #{client_counter} rozłączył się.")
                    break

                # Print received data and echo it back to the client
                print(f"[#%d] Odebrano %d B: \"%s\"" % (client_counter, len(data), data.decode('utf-8', errors='replace')))
                client_socket.sendall(data) # Echo the data back to the client

        except ConnectionError as e:
            # Handle any connection errors
            print(f"{WARNING_SIGN} Błąd połączenia z klientem #{client_counter}: {e}")

        finally:
            # Ensure the client socket is closed when done
            client_socket.close()

# Entry point of the program
if __name__ == "__main__":
    main()
