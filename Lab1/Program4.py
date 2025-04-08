import asyncio  # Import asyncio for asynchronous programming.

tasks = {}  # A dictionary to store active tasks, mapping thread_id to the corresponding task.

async def show_letters(thread_id):
    """
    An asynchronous function that prints letters from A to Z with the thread_id.
    It simulates the behavior of a thread-like function by printing one letter every second.
    """
    try:
        for c in range(ord('A'), ord('Z') + 1):  # Loop from 'A' to 'Z'.
            print(f"{chr(c)}{thread_id}")  # Print the letter followed by the thread_id.
            await asyncio.sleep(1)  # Wait for 1 second before printing the next letter.
    except asyncio.CancelledError:
        # If the task is canceled, handle the cancellation gracefully.
        print(f"Task {thread_id} canceled.")
        return

async def user_input_loop():
    """
    An asynchronous loop that listens for user input to cancel tasks or exit the program.
    The user can cancel specific tasks using 'cancel <id>' or exit the program with 'exit'.
    """
    print("Use command 'cancel X' or 'exit' to interact.")
    while True:
        cmd = await asyncio.to_thread(input, ">> ")  # Get user input in a non-blocking way.
        cmd = cmd.strip().lower()  # Clean and normalize input to lowercase.
        if cmd.startswith("cancel"):
            try:
                _, tid = cmd.split()  # Split the command to get the thread ID.
                tid = int(tid)
                if tid in tasks:  # If the task exists, cancel it.
                    tasks[tid].cancel()
            except ValueError:
                print("Incorrect syntax. Use: cancel <number>")  # Inform the user about wrong command syntax.
        elif cmd == "exit":
            for task in tasks.values():  # Cancel all tasks if 'exit' command is given.
                task.cancel()
            break  # Exit the input loop.

async def main():
    """
    The main asynchronous function that creates 10 tasks (threads) to display letters.
    It also starts the user input loop and waits for tasks to finish.
    """
    # Create and start 10 tasks (threads) to show letters A to Z.
    for i in range(1, 11):
        thread_id = i if i < 10 else 0  # Assign thread_id.
        task = asyncio.create_task(show_letters(thread_id))  # Create the task.
        tasks[thread_id] = task  # Store the task in the tasks dictionary.

    await user_input_loop()  # Start the user input loop.
    await asyncio.gather(*tasks.values(), return_exceptions=True)  # Wait for all tasks to finish.

if __name__ == "__main__":
    asyncio.run(main())  # Run the main function using asyncio.
