import pickle
import socket
import team_local_tactics as TLT


class Client:
    SOCKET = socket.socket()
    player1 = []
    player2 = []

    def __init__(self, PORT) -> None:
        self.SOCKET.connect(("localhost", PORT))
        print(f"Connected to port {PORT}")
        self.gameLoop()

    def gameLoop(self):
        while True:
            message = self.SOCKET.recv(1024).decode()

            if not message:
                continue

            match message.split()[0]:
                case "MESSAGE":
                    print(" ".join(message.split()[1:]))

                case "GAME":
                    champ = self.SOCKET.recv(6966)
                    champions = pickle.loads(champ)
                    print(champ)
                    TLT.print_available_champs(champions)


                    if message == "GAME FIRST":

                        for y in range(2):
                            print(f"Pick your {y +1} player")
                            (TLT.input_champion('Player 1', 'red', champions, self.player1, self.player2))
                            self.SOCKET.send(str(self.player1[y]).encode())
                        print("Waiting for other player")

                    else:
                        for y in range(2):
                            print(f"Pick your {y +1} player")
                            (TLT.input_champion('Player 2', 'blue', champions, self.player1, self.player2))
                            self.SOCKET.send(str(self.player2[y]).encode())
                        print("Waiting for other player")

                case "FINISHED":
                    print("GAME OVER")
                    match_results = self.SOCKET.recv(6966)
                    match = pickle.loads(match_results)
                    TLT.print_match_summary(match)
                    self.player1.clear()
                    self.player2.clear()







    def shutdown(self):
        self.SOCKET.close()
        print("Closed connection to server.")


if __name__ == "__main__":
    PORT = 6966
    client = Client(PORT)