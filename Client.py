import pickle
import socket
import team_local_tactics as TLT
from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team


class Client:
    SOCKET = socket.socket()

    def __init__(self, PORT) -> None:
        self.SOCKET.connect(("localhost", PORT))
        print(f"Connected to localhost on the port {PORT}")
        self.gameLoop()

    def gameLoop(self):
        while True:
            msg = self.SOCKET.recv(1024).decode()

            if not msg:
                continue

            match msg.split()[0]:
                case "MESSAGE":
                    print(" ".join(msg.split()[1:]))

                case "GAME":
                    print(" ".join(msg.split()[1:]))
                    champions = load_some_champs()
                    TLT.print_available_champs(champions)
                    player1 = []
                    player2 = []

                    if msg == "GAME FIRST":

                        for y in range(2):
                            print(f"Pick your {y +1} player")
                            (TLT.input_champion('Player 1', 'red', champions, player1, player2))
                            self.SOCKET.send(str(player1[y]).encode())
                            print("Waiting for other player")

                    else:
                        for y in range(2):
                            print(f"Pick your {y +1} player")
                            (TLT.input_champion('Player 2', 'blue', champions, player1, player2))
                            self.SOCKET.send(str(player2[y]).encode())
                            print("Waiting for other player")

                case "MATCHRESULT":
                    print(" ".join(msg.split()[1:]))


                    self.shutdown()
                    break
                case _:
                    continue



    def shutdown(self):
        self.SOCKET.close()
        print("Closed connection to server.")


if __name__ == "__main__":
    PORT = 6966
    client = Client(PORT)