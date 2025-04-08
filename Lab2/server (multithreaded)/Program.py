import socket     # Import the socket module for network communication
import threading  # Import threading to handle multiple clients concurrently
import sys        # Import sys to handle system-level operations such as command-line arguments

# Maximum number of allowed clients
MAX_CLIENTS = 3
PORT = 7  # Default port, can be changed via command-line arguments

active_clients = {}     # Dictionary to store active clients with their client number as the key (client_number: (ip, port))
client_counter = 1      # Counter to assign a unique client number to each new connection
lock = threading.Lock() # Lock to ensure thread-safe operations on the active_clients dictionary

# Function to handle communication with a single client
def handle_client(conn, addr, client_id):
    print(f"[#{client_id}] Connected: {addr[0]}:{addr[1]}") # Print client connection details
    try:
        while True:
            data = conn.recv(1024)  # Receive up to 1024 bytes of data from the client
            if not data:
                break # If no data, the client has disconnected
            message = data.decode('utf-8', errors='ignore') # Decode the received message
            print(f"[#{client_id}] Received ({len(data)} bytes): {message}") # Print the received message
            conn.sendall(data)  # Echo the received message back to the client
    except Exception as e:
        print(f"[#{client_id}] Error: {e}") # Print any error that occurs during communication
    finally:
        # Usage of "with" provides multithreading safety
        with lock:
            del active_clients[client_id] # Remove the client from the active_clients dictionary
        print(f"[#{client_id}] Disconnected.")
        conn.close()  # Close the connection to the client

# Function to accept new client connections
def accept_clients(server_socket):
    global client_counter
    while True:
        try:
            conn, addr = server_socket.accept() # Accept a new client connection
            #Usage of "with" provides multithreading safety
            with lock:
                # If the maximum number of clients is reached, reject the connection
                if len(active_clients) >= MAX_CLIENTS:
                    print(f"[!] Too many connections. Rejecting {addr}.")
                    conn.sendall(b"SERVER BUSY\n") # Send a busy message to the client
                    conn.close()  # Close the rejected connection
                    continue
                client_id = client_counter  # Assign a unique client ID
                client_counter += 1  # Increment the client counter for the next client
                active_clients[client_id] = addr  # Store the client's information in active_clients
            # Start a new thread to handle the client's communication
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
            client_thread.daemon = True # Mark the thread as a daemon thread to allow automatic shutdown
            client_thread.start()
            show_active_clients()  # Display the list of active clients
        except Exception as e:
            print(f"[!] Accept error: {e}")  # Print any error that occurs during the accept process
            break

# Function to display the list of active clients
def show_active_clients():
    with lock:
        print("\n--- Active Clients ---")
        for cid, (ip, port) in active_clients.items():
            print(f"[#{cid}] {ip}:{port}")
        print("----------------------\n")

# Function to start the server and listen for client connections
def start_server(host='0.0.0.0', port=PORT):
    try:
        # Create a socket for the server and bind it to the specified host and port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen() # Start listening for incoming connections
        print(f"[i] Server listening on {host}:{port}")
    except Exception as e:
        print(f"[!] Failed to start server: {e}")
        sys.exit(1)  # Exit the program if server setup fails

    try:
        # Start a thread to handle client connections
        accept_thread = threading.Thread(target=accept_clients, args=(server_socket,))
        accept_thread.daemon = True # Mark the thread as a daemon thread
        accept_thread.start()

        # Main loop to handle server shutdown
        while True:
            cmd = input("Type 'exit' to shut down: ").strip()  # Wait for user input to shut down the server
            if cmd.lower() == "exit":
                break # Exit the loop and shut down the server
    except KeyboardInterrupt:
        print("\n[i] Shutting down server...") # Handle KeyboardInterrupt (Ctrl+C) gracefully
    finally:
        server_socket.close() # Close the server socket

if __name__ == "__main__":
    port = PORT
    # Check for a command-line argument to override the default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])  # Use the port provided as a command-line argument
        except ValueError:
            print("[!] Invalid port number. Using default port 7.") # Handle invalid port argument
    start_server(port=port)  # Start the server
