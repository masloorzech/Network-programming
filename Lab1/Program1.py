import threading  # Import the threading module, which allows creating and managing threads in Python.

def hello_world():
    # A function that simply prints "Hello World!!"
    print("Hello World!!")

if __name__ == "__main__":  # Check if the script is being run directly (not imported).
    thread = threading.Thread(target=hello_world)  # Create a new thread that will execute the hello_world function.
    thread.start()  # Start the thread. The hello_world function will run in a separate thread.
    thread.join()  # Wait for the thread to finish. The main program will pause here until the thread completes.
    print("Main function finished.")  # After the thread finishes, print that the main function is done.

