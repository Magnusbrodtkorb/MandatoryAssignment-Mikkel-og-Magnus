import pickle
import socket
from pickle import dumps

import team_local_tactics as TLT
from champlistloader import load_some_champs
from core import Match, Team


champions = load_some_champs()


class Server:
    player1 = []
    player2 = []
    SOCKET = socket.socket()
    connections = []


    def __init__(self, PORT) -> None:
        print("Socket created succsessfully")
        self.SOCKET.bind(("localhost", PORT))
        print(f"Socket binded to localhost with port {PORT}")

        self.SOCKET.listen()
        print("Waiting for connections...")
        self.connectionLoop()

    # Connection loop
    def connectionLoop(self):
        while True:
            con, addr = self.SOCKET.accept()
            self.connections.append(con)
            print(f"Got connection from {addr}")

            match len(self.connections):
                case 1:
                    self.connections[0].send("MESSAGE Waiting for another player to join.".encode())

                case 2:
                    print("MESSAGE All players connected starting game.".encode())
                    self.connections[0].send("MESSAGE All players connected starting game.".encode())
                    self.connections[1].send("MESSAGE All players connected starting game.".encode())
                    self.connections[1].send("GAME Recieved STARTGAME command.".encode())
                    self.connections[0].send("GAME FIRST".encode())

                    break

        self.gameLoop()

    def sendToAllClients(self, msg):
        for connect in self.connections:
            connect.send(msg.encode())
            print(f"Sent message: {msg} to connection: {connect.getsockname()}")

    def matchSum(self):
        if len(self.player1) == 2 & len(self.player2) == 2:
            match = Match(
                Team([champions[name] for name in self.player1]),
                Team([champions[name] for name in self.player2])
            )
            match.play()
            self.sendToAllClients("MATCHRESULT Game finished: ")
            send_match = pickle.dumps(match)
            self.connections[0].send(send_match)
            self.connections[1].send(send_match)
            # Print a summary




    def gameLoop(self):
        db = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        db.sendto(" ".encode(), ("localhost", 6966))
        update_champs = db.recv(6966)
        self.champions = pickle.loads(update_champs)
        for i in range(2):
            msg = self.connections[0].recv(6966).decode()
            self.sendToAllClients("Hello")
            msg2 = self.connections[1].recv(6966).decode()
            self.player1.append(msg)
            self.player2.append(msg2)

        print(self.player1)
        self.matchSum()


    def shutdown(self):
        self.SOCKET.close()
        print("Server shutting down")


if __name__ == "__main__":
    PORT = 6966

    client = Server(PORT)
