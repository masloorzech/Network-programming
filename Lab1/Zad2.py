import threading
import time

class ControlledThread(threading.Thread):
    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id
        self.paused = threading.Event()
        self.paused.set()
        self.stopped = threading.Event()

    def run(self):
        while not self.stopped.is_set():
            self.paused.wait()
            for c in range(ord('A'), ord('Z') + 1):
                print(f"{chr(c)}{self.thread_id}")
                time.sleep(1)
                if not self.paused.is_set():
                    break

    def stop(self):
        self.paused.clear()

    def resume(self):
        self.paused.set()

    def terminate(self):
        self.stopped.set()

def main():
    threads = [ControlledThread(i if i < 10 else 0) for i in range(1, 11)]
    for t in threads:
        t.start()

    print("Wpisz 'start X', 'stop X' lub 'exit'")
    while True:
        cmd = input(">> ").strip().lower()
        if cmd.startswith("start") and len(cmd) == 2:
            _, tid = cmd.split()
            threads[int(tid) - 1].resume()
        elif cmd.startswith("stop")and len(cmd) == 2:
            _, tid = cmd.split()
            threads[int(tid) - 1].stop()
        elif cmd == "exit":
            for t in threads:
                t.terminate()
            break

if __name__ == "__main__":
    main()
