import threading  # Import the threading module for handling threads.
import time  # Import time module to use sleep function for pauses in the program.

lock = threading.Lock()  # Create a lock object to synchronize access to shared resources.


class SyncThread(threading.Thread):
    # A custom thread class that extends threading.Thread. This class prints letters A to Z along with the thread ID.

    def __init__(self, thread_id):
        # Initialize the thread with a given thread ID.
        super().__init__()
        self.thread_id = thread_id

    def run(self):
        # The main logic of the thread, which prints letters A to Z with the thread ID.
        while True:
            with lock:  # Acquire the lock to ensure that only one thread accesses the code block at a time.
                for c in range(ord('A'), ord('Z') + 1):  # Loop through the alphabet (A to Z).
                    print(f"{chr(c)}{self.thread_id}")  # Print the letter followed by the thread ID.
                    time.sleep(1)  # Sleep for 1 second before printing the next letter.


def main():
    # Main function to create and start threads.

    # Create 10 threads, with thread IDs 1 through 9, and the last one having ID 0.
    threads = [SyncThread(i if i < 10 else 0) for i in range(1, 11)]

    # Start all the threads.
    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
