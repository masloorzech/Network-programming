import threading
import time

lock = threading.Lock()

class SyncThread(threading.Thread):
    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id

    def run(self):
        while True:
            with lock:
                for c in range(ord('A'), ord('Z') + 1):
                    print(f"{chr(c)}{self.thread_id}")
                    time.sleep(1)

def main():
    threads = [SyncThread(i if i < 10 else 0) for i in range(1, 11)]
    for t in threads:
        t.start()

if __name__ == "__main__":
    main()
