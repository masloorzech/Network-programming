# Broadcast Sender & Receiver (Python)

This project contains two simple Python scripts demonstrating how to send and receive messages using **UDP broadcast**. It can be used to experiment with broadcast communication within a local network (LAN).

## 📄 Files

- `broadcast_receiver.py` – Receives messages sent to a broadcast address.
- `broadcast_sender.py` – Sends messages using broadcast to all devices in the subnet.

## 🧰 Requirements

- Python 3.x  
- Works on Linux, macOS, and Windows  

No external libraries are required – only Python's standard library modules (`socket`, `signal`).

## ▶️ How to Run

### 1. Run the Receiver

```bash
python3 broadcast_receiver.py
```
### 2. Run the Sender
```bash
python3 broadcast_sender.py
```
🛑 To stop the sender or receiver Press Ctrl+C in the terminal window.

## 💡 Example
### 1.Start the receiver:
```bash
Enter port to listen on: 5007
Listening for broadcast messages on port 5007...
```
### 2.Start the sender:
```bash
Enter port to send to: 5007
Type your message (Ctrl+C to stop):
```
## 📡 Notes
- The sender uses the universal broadcast address 255.255.255.255 to send packets to all hosts on the subnet.
- The receiver uses SO_REUSEADDR, so multiple receivers can run on the same machine or port.
- Both scripts handle basic input validation and display helpful errors when needed.
- Works best when sender and receiver are on the same local network.
