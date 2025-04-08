import threading  # Import the threading module to handle threads in Python.
import time  # Import time module to use sleep function for pauses in the program.


class ControlledThread(threading.Thread):
    # A custom thread class that extends the Thread class and provides methods for pausing, resuming, and stopping the thread.

    def __init__(self, thread_id):
        # Initialize the thread with a given thread_id and create events for pausing and stopping.
        super().__init__()
        self.thread_id = thread_id
        self.paused = threading.Event()  # This event controls whether the thread is paused or running.
        self.paused.set()  # By default, the thread is running.
        self.stopped = threading.Event()  # This event controls when the thread should stop.

    def run(self):
        # The main logic of the thread, which runs in a loop until the thread is stopped.
        while not self.stopped.is_set():
            self.paused.wait()  # Wait here until the thread is unpaused (if paused).
            for c in range(ord('A'), ord('Z') + 1):
                # Print the alphabet letter followed by the thread_id (which identifies the thread).
                print(f"{chr(c)}{self.thread_id}")
                time.sleep(1)  # Sleep for 1 second before printing the next letter.
                if not self.paused.is_set():
                    break  # If paused, exit the loop and stop printing characters.

    def stop(self):
        # Stop the thread by clearing the paused event, causing it to halt.
        self.paused.clear()

    def resume(self):
        # Resume the thread by setting the paused event, allowing it to run again.
        self.paused.set()

    def terminate(self):
        # Set the stopped event, which will stop the thread when checked in the run method.
        self.stopped.set()


def main():
    # Main function to handle user input and control the threads.

    # Create 10 threads, with thread IDs 1 through 9, and the last one having ID 0.
    threads = [ControlledThread(i if i < 10 else 0) for i in range(1, 11)]
    for t in threads:
        t.start()  # Start each thread.

    print("Enter 'start X', 'stop X' or 'exit' to control the threads.")

    while True:
        # Main loop to handle user commands.
        cmd = input(">> ").strip().lower()  # Get user input and convert it to lowercase.

        if cmd.startswith("start") and len(cmd) == 2:
            # Command to start/resume a thread. It starts with 'start' followed by the thread ID.
            _, tid = cmd.split()
            threads[int(tid) - 1].resume()  # Resume the thread corresponding to the ID.

        elif cmd.startswith("stop") and len(cmd) == 2:
            # Command to stop a thread. It starts with 'stop' followed by the thread ID.
            _, tid = cmd.split()
            threads[int(tid) - 1].stop()  # Stop the thread corresponding to the ID.

        elif cmd == "exit":
            # Command to stop all threads and exit the program.
            for t in threads:
                t.terminate()  # Terminate each thread.
            break  # Exit the loop and end the program.


if __name__ == "__main__":
    main()  # Run the main function to start the program.
