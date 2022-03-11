from socket import socket, AF_INET, SOCK_DGRAM
import pickle

from champlistloader import load_some_champs


class storageDB:
    address_family = AF_INET
    socket_type = SOCK_DGRAM
    sock = socket(address_family, socket_type)

    def __init__(self, PORT):
        print("[A DATABASE SERVER HAS BEEN CREATED]")
        self.sock.bind(("localhost", PORT))
        print(f"[BINDED TO localhost] AT PORT: {PORT}")

        self.process_champions()

    def process_champions(self):

        while 1:
            _, origin = self.sock.recvfrom(6966)
            print("Sending champs...")

            load = load_some_champs()
            champs = pickle.dumps(load)
            self.sock.sendto(champs, origin)
            print(f"Champions has been transmitted to {origin}")


if __name__ == "__main__":
    PORT = 6966
    client = storageDB(PORT)