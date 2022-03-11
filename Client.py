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
            # Recieve message from server
            message = self.SOCKET.recv(6966).decode()

            if not message:
                continue

            match message.split()[0]:
                # Print message to Client
                case "MESSAGE":
                    print(" ".join(message.split()[1:]))
                # Recieve Start Game Command from server
                case "GAME":
                    champ = self.SOCKET.recv(4000)
                    # Load champions from DB and print available champions to Client
                    champions = pickle.loads(champ)
                    print(champ)
                    TLT.print_available_champs(champions)

                    # First player to Connect = Player 1
                    if message == "GAME FIRST":
                        #Send input from clients to server
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
                # When game is finished recieve match result from server and print summary to clients
                case "FINISHED":
                    print("GAME OVER")
                    match_results = self.SOCKET.recv(4000)
                    match = pickle.loads(match_results)
                    TLT.print_match_summary(match)
        self.shutdown()


    # Close socket when game is over
    def shutdown(self):
        self.SOCKET.close()
        print("Closed connection to server.")


if __name__ == "__main__":
    PORT = 4000
    client = Client(PORT)