#!/usr/bin/env python3
import socket
import sys
import threading

# First client will wait until second client come online
def wait():
    host = ''
    port = 2000
    cli.bind((host, port))
    cli.listen(2)
    print("Waiting for connection...")
    while True:
        c, addr = cli.accept()
        threading.Thread(target=listen, args=(c,)).start()
        threading.Thread(target=event, args=(c,)).start()

# Second client will connect using localhost and port #: 2000
def connect():
    host = input("Enter IP address:")
    port = 2000
    cli.connect((host, port))
    threading.Thread(target=listen, args=(cli,)).start()
    threading.Thread(target=event, args=(cli,)).start()


def listen(cli):
    global end

    # Display message when connection is conformed.
    print("Connection conformed!")
    print("Type 'exit' to end conversation")

    while True:
        if end:
            try:        # Display messages from friend
                msg = cli.recv(100).decode()
                print("\rFriend: " + msg  + "\nYou: ", end="", flush=True)
            except:             # End connection if someone disconnect.
                print("Connection closed")
                break
            if msg == "exit":       # break if client send 'exit' message
                end = 0;
                break

    # Disconnect if client end conversation
    print("\nYour are disconnected.")
    cli.close()
    sys.exit()


def event(cli):
    global end
    while True:
        if end:
            msg = input("You: ")        # Message input area
            cli.send(msg.encode())
            if msg == "exit":           # Close chat if 'exit' message is send.
                print("Chat termination signal sent!")
                end = 0;
                cli.close()
                sys.exit()

# socket
cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
end = 1;
# Option to choose for client
option = input("Type 'CONN' to connect or 'WAIT' to wait for peer connection\n>>")

# If client choose to connect
if  option == "CONN":
    connect()
# If client choose to wait
elif option == "WAIT":
    wait()
# If different option was choosed.
else:
    print("Invalid input, bye...")
    cli
