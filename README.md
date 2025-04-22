# Network Programming Labs

This repository contains solutions to practical tasks from the *Network Programming* course. Each lab demonstrates different networking and concurrency concepts in Python.

## Lab Descriptions

### 🟢 Lab 1 – Threading and Asyncio
Demonstrates various concurrency techniques in Python:
- Creating and managing threads with `threading`
- Controlling thread execution (pause, resume, stop)
- Using `Lock` for synchronization
- Asynchronous task handling with `asyncio`

---

### 🟡 Lab 2 – TCP Echo Server and Client
Implements a multi-client TCP echo service:
- A server that handles multiple clients concurrently
- Clients that connect, send messages, and receive echoes
- Uses `socket` and `threading` or `asyncio`

---

### 🟣 Lab 3 – UDP Multicast/Broadcast
Demonstrates how to send and receive multicast/Broadcast messages over UDP:
- Multicast sender that broadcasts messages to a group
- Multicast receiver that listens to a specific group and port

---

### 🔵 Lab 4 – HTTP Server
Implements a basic HTTP server:
- Accepts HTTP GET requests
- Serves static content or simple responses
- Uses `http.server` module

---

## Requirements
- Python 3.8+
- Specification written in separated readme

## Usage
Each lab can be run independently.
