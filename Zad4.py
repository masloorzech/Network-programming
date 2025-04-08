import asyncio

tasks = {}

async def show_letters(thread_id):
    try:
        for c in range(ord('A'), ord('Z') + 1):
            print(f"{chr(c)}{thread_id}")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print(f"Zadanie {thread_id} anulowane.")
        return

async def user_input_loop():
    print("Użyj komendy 'cancel X' lub 'exit'")
    while True:
        cmd = await asyncio.to_thread(input, ">> ")
        cmd = cmd.strip().lower()
        if cmd.startswith("cancel"):
            try:
                _, tid = cmd.split()
                tid = int(tid)
                if tid in tasks:
                    tasks[tid].cancel()
            except ValueError:
                print("Zła składnia. Użyj: cancel <numer>")
        elif cmd == "exit":
            for task in tasks.values():
                task.cancel()
            break

async def main():
    for i in range(1, 11):
        thread_id = i if i < 10 else 0
        task = asyncio.create_task(show_letters(thread_id))
        tasks[thread_id] = task

    await user_input_loop()
    await asyncio.gather(*tasks.values(), return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())
