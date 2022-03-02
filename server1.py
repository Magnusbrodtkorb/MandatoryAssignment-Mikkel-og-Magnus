from socket import socket, AF_INET, SOCK_DGRAM

address_family = AF_INET
socket_type = SOCK_DGRAM
sock = socket(address_family, socket_type)

# For servers
host = "localhost" # String: Hostname, IP address or ""
port = 5555
socket_address = (host, port)
sock.bind(socket_address)