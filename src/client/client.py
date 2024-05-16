import socket

client = None

def write_to_server(message):
    byte_message = message.encode()
    client.send(byte_message)

def read_from_server():
    byte_message = client.recv(10000)
    return byte_message.decode()

def connect(host, port):
    global client
    client = socket.socket()
    client.connect((host, int(port)))
