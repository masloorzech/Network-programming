# Multicast Sender & Receiver (Python)

This project contains two simple Python scripts demonstrating how to send and receive messages using **UDP multicast**. It can be used to experiment with multicast communication in a local network.

## 📄 Files

- `Program_receiver.py` – Receives messages sent to a multicast group.
- `Program_sender.py` – Sends messages to a multicast group.

## 🧰 Requirements
- Python 3.x
- Works on Linux, macOS, and Windows

No external libraries are required – only Python's standard library modules (`socket`, `struct`, `signal`).

## ▶️ How to Run

### 1. Run the Receiver

```bash
python3 Program_receiver.py
```
### 2. Run the sender
```bash
python3 Program_sender.py
```
🛑 To stop the sender or receiver
Press Ctrl+C in the terminal window.

## 💡 Example
### Start the receiver:
```bash
Enter multicast address (e.g., 224.0.0.1): 224.0.0.1
Enter port: 5007
Waiting for messages...
```
### Start the sender:
```bash
Enter multicast address (e.g., 224.0.0.1): 224.0.0.1
Enter port: 5007
Type your message (Ctrl+C to stop):
```

### 📡 Notes
- The sender sets TTL = 1, which means packets will not leave the local network.
- Both programs support multiple receivers connected to the same multicast group.
- Works best when sender and receiver are on the same local network.