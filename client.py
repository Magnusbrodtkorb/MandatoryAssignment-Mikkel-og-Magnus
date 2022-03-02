from socket import socket
sock = socket() # Omit AF_INET and SOCK_STREAM
sock.connect(("localhost", 5550))
