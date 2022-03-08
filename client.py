from socket import socket, AF_INET, SOCK_STREAM
sock = socket(AF_INET, SOCK_STREAM)  # Omit AF_INET and SOCK_STREAM
sock.connect(("localhost", 5550))
