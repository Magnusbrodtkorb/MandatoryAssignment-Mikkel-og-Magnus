from socket import socket, AF_INET, SOCK_DGRAM

address_family = AF_INET
socket_type = SOCK_DGRAM
sock = socket(address_family, socket_type)