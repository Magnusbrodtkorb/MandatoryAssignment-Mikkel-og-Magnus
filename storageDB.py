import socket
import pickle

from champlistloader import load_some_champs


class storageDB:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, PORT):
        print("[DATABASE SERVER IS CREATED]")
        self.sock.bind(("localkost", PORT))
        print(f"[BINDED TO localhost] AT PORT: {PORT}")

        self.process_champions()

    def process_champions(self):
        while 1:
            _, source = self.sock.recvfrom(1)
            print("Sending...")
            load = load_some_champs()
            champs = pickle.dumps(load)
            self.sock.sendto(champs, source)
            print(f"Champions has been transmitted to {source}")


if __name__ == "__main__":
    PORT = 5555
    client = storageDB(PORT)