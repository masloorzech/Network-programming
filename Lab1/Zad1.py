import threading

def hello_world():
    print("Hello World!!")

if __name__ == "__main__":
    thread = threading.Thread(target=hello_world)
    thread.start()
    thread.join()
    print("Główna funkcja zakończona.")
